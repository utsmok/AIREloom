from dataclasses import dataclass, Field
from datetime import datetime, timedelta
import logging
import warnings
import httpx
from typing import LiteralString
from aireloom.constants import AIRELOOM_VERSION

@dataclass
class Client:
    refresh_token: str | None = Field(default=None)
    access_token: str | None = Field(default=None)

    _token_expires_at: datetime = Field(default=datetime.now()-timedelta(hours=1), init=False)

    max_retries: int = Field(default=3, metadata={"help": "Maximum number of retries for HTTP requests"})
    timeout: int = Field(default=10, metadata={"help": "Timeout in seconds for HTTP requests"})

    _client: httpx.Client | None = Field(default=None, init=False) # set by init_client

    GET_ACCESS_TOKEN_URL: LiteralString = "https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken="

    def __post_init__(self):
        self._init_client()
        if not self.access_token:
            self.get_token()

    @property
    def client(self):
        if not self._client:
            self._init_client()
        return self._client

    def _init_client(self):
        if not self._client:
            self._client = httpx.Client(
                headers={},
                transport=httpx.HTTPTransport(retries=self.max_retries),
                timeout=self.timeout
            )
            self._client.headers['accept'] = 'application/json'
            self._client.headers['User-Agent'] = f'aireloom/{AIRELOOM_VERSION}'

    def get_token(self):

        if self._token_expires_at >= datetime.now()+timedelta(minutes=5):
            logging.debug("Token still valid, skipping refresh")
            return

        if not self.refresh_token:
            logging.error("No refresh token found")
            warnings.warn("No refresh token added to settings, cannot retrieve access token.")
            return

        if not self.client:
            self._init_client()

        try:
            r = self.client.get(self.GET_ACCESS_TOKEN_URL, headers={"Authorization": f"Bearer {self.refresh_token}"})
            r.raise_for_status()
        except Exception as e:
            logging.error(f"Error getting access token: {e}")
            return

        raw_token = r.json()

        self.access_token = raw_token["access_token"]
        self._token_expires_at = datetime.now()+timedelta(seconds=raw_token["expires_in"])
        self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        logging.debug(f"Got access token. Experires at {self._token_expires_at}.")
