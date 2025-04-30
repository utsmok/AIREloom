# aireloom/client.py
import ssl
from collections.abc import Mapping
from typing import Any, Self

import certifi
import httpx
import tenacity
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    RetryError,
    stop_after_attempt,
    wait_exponential,
)

from .auth import (
    AuthStrategy,
    ClientCredentialsAuth,
    NoAuth,
    StaticTokenAuth,
)
from .config import ApiSettings, get_settings
from .constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
)
from .exceptions import (
    AireloomError,
    APIError,
    AuthError,
    NetworkError,
    RateLimitError,
    TimeoutError,
)
from .log_config import logger
from .types import RequestData


class AireloomClient:
    """Asynchronous HTTP client for interacting with OpenAIRE APIs."""

    DEFAULT_RETRYABLE_STATUS_CODES = frozenset([429, 500, 502, 503, 504])

    def __init__(
        self,
        settings: ApiSettings | None = None,
        auth_strategy: AuthStrategy | None = None,
        *,
        # Allow direct override for testing/specific cases, but prefer settings
        api_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = OPENAIRE_GRAPH_API_BASE_URL,  # Default to Graph API
        http_client: httpx.AsyncClient | None = None,
        retryable_status_codes: frozenset[int] = DEFAULT_RETRYABLE_STATUS_CODES,
    ):
        """
        Initializes the AireloomClient.

        Authentication is determined automatically based on settings unless an
        explicit `auth_strategy` is provided.

        Order of precedence for automatic auth determination:
        1. Client Credentials (if client_id & client_secret are configured)
        2. Static Token (if api_token is configured)
        3. No Authentication

        Args:
            settings: Optional ApiSettings instance. If None, loads global settings.
            auth_strategy: Optional explicit authentication strategy instance.
            api_token: Optional static API token (overrides settings if provided).
            client_id: Optional client ID (overrides settings if provided).
            client_secret: Optional client secret (overrides settings if provided).
            base_url: The base URL for the API (defaults to Graph API).
            http_client: Optional pre-configured httpx.AsyncClient instance.
            retryable_status_codes: Set of HTTP status codes to retry on.
        """
        self._settings = settings or get_settings()
        self._base_url = base_url.rstrip("/")
        self._retryable_status_codes = retryable_status_codes

        # Determine Authentication Strategy
        self._auth_strategy: AuthStrategy
        if auth_strategy:
            logger.info("Using explicitly provided authentication strategy.")
            self._auth_strategy = auth_strategy
        else:
            # Use overrides if provided, otherwise use settings
            _client_id = client_id or self._settings.openaire_client_id
            _client_secret = client_secret or self._settings.openaire_client_secret
            _api_token = api_token or self._settings.openaire_api_token
            _token_url = self._settings.openaire_token_url

            if _client_id and _client_secret:
                logger.info("Using Client Credentials authentication.")
                self._auth_strategy = ClientCredentialsAuth(
                    client_id=_client_id,
                    client_secret=_client_secret,
                    token_url=_token_url,
                )
            elif _api_token:
                logger.info("Using Static Token authentication.")
                self._auth_strategy = StaticTokenAuth(token=_api_token)
            else:
                logger.info("No authentication credentials found, using NoAuth.")
                self._auth_strategy = NoAuth()

        # Initialize HTTP Client
        self._should_close_client = http_client is None  # Close only if we created it
        self._http_client = http_client or self._create_default_http_client()

        logger.debug("AireloomClient initialized.")

    def _create_default_http_client(self) -> httpx.AsyncClient:
        """Creates a default httpx.AsyncClient with configured settings."""
        try:
            # Use certifi for SSL certificates if available
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            verify_ssl = ssl_context
            logger.debug("Using certifi SSL context.")
        except Exception:
            # Fallback to default httpx verification
            verify_ssl = True
            logger.warning(
                "certifi not found or failed to load. Using default SSL verification."
            )

        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._settings.request_timeout,
            verify=verify_ssl,
            headers={"User-Agent": self._settings.user_agent},
            # Add transport/proxy settings from config if needed later
        )

    async def _execute_single_request(
        self, request_data: RequestData
    ) -> httpx.Response:
        """Executes a single HTTP request attempt."""
        request = request_data.build_request()
        try:
            # Apply authentication just before sending
            await self._auth_strategy.async_authenticate(request)

            logger.debug(f"Sending request: {request.method} {request.url}")
            logger.trace(f"Request Headers: {request.headers}")
            if request.content:
                # Avoid logging potentially large/sensitive bodies unless debugging heavily
                logger.trace(f"Request Body: {request.content.decode()}")

            response = await self._http_client.send(request)

            logger.debug(f"Received response: {response.status_code} for {request.url}")
            logger.trace(f"Response Headers: {response.headers}")
            # Optionally log response body excerpts for debugging
            # logger.trace(f"Response Body Excerpt: {response.text[:200]}")

            # Raise APIError for non-success status codes *after* logging
            if response.status_code >= 400:
                # Raise specific error for rate limit
                if response.status_code == 429:
                    raise RateLimitError("API rate limit exceeded.", response=response)
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    response=response,
                )
            return response

        except httpx.HTTPStatusError as e:
            # Handle 4xx/5xx errors after successful connection
            logger.error(
                f"Request failed with status {e.response.status_code}: {e.request.url}"
            )
            # Raise specific error for rate limiting
            if e.response.status_code == 429:
                raise RateLimitError("API rate limit exceeded.", response=e.response, request=e.request) from e
            # General API error for others
            raise APIError(
                f"API request failed with status {e.response.status_code}",
                response=e.response,
                request=e.request,
            ) from e
        except Exception as e:  # Catch unexpected errors
            logger.exception(f"Unexpected error during request to {request.url}: {e}")
            raise AireloomError(f"An unexpected error occurred: {e}") from e

    def _should_retry_request(self, retry_state: tenacity.RetryCallState) -> bool:
        """Predicate for tenacity: should we retry this request?"""
        outcome = retry_state.outcome
        if not outcome: # Should not happen with reraise=True, but defensive check
             return False

        if outcome.failed:
            exc = outcome.exception()
            if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
                url = getattr(getattr(exc, 'request', None), 'url', 'N/A')
                logger.warning(f"Retrying due to {type(exc).__name__} for {url}")
                return True  # Retry on timeout or network errors
            if isinstance(exc, httpx.HTTPStatusError):
                status_code = exc.response.status_code
                # Retry on 5xx server errors or 429 Rate Limit
                if status_code >= 500 or status_code == 429:
                    logger.warning(
                        f"Retrying due to status code {status_code} for {exc.request.url}"
                    )
                    return True
        # Do not retry otherwise (successful response or non-retryable error like 404)
        return False

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        data: Mapping[str, Any] | None = None,
        base_url_override: str | None = None,
    ) -> httpx.Response:
        """Makes an HTTP request with configured retries for transient errors."""
        base_url = (base_url_override or self._base_url).rstrip("/")
        full_url = f"{base_url}/{path.lstrip('/')}"

        request_data = RequestData(
            method=method,
            url=full_url,
            params=params,
            json_data=json_data,
            data=data,
            # Headers are added during _execute_single_request after auth
        )

        auth_header: dict[str, str] | None = None
        if self._auth_strategy:
            try:
                auth_header = await self._auth_strategy.async_authenticate(request_data)
            except AuthError as e:
                logger.error(f"Authentication failed: {e}")
                # Wrap AuthError for consistent API
                raise AireloomError(f"Authentication failed: {e}") from e

        headers = {"User-Agent": self._settings.user_agent}
        if auth_header:
            headers.update(auth_header)

        request_data.headers = headers

        # Prepare retry strategy
        retry_strategy = AsyncRetrying(
            stop=stop_after_attempt(self._settings.max_retries + 1),
            wait=wait_exponential(
                multiplier=self._settings.backoff_factor, min=0.1, max=10
            ),
            retry=self._should_retry_request,
            reraise=True,
        )

        try:
            # Call the function with retry logic
            response = await retry_strategy(self._execute_single_request, request_data)
            return response

        # Handle exceptions *after* retries are exhausted or if a non-retryable error occurs
        except httpx.TimeoutException as e:
            logger.warning(f"Request timed out after retries: {e}")
            raise TimeoutError("Request timed out", request=getattr(e, "request", None)) from e

        except httpx.NetworkError as e:
            logger.warning(f"Network error after retries: {e}")
            raise NetworkError("Connection failed", request=getattr(e, "request", None)) from e

        except httpx.HTTPStatusError as e:
            logger.warning(
                f"HTTP error after retries: Status {e.response.status_code}, Response: {e.response.text[:100]}"
            )
            if e.response.status_code == 429:
                raise RateLimitError(
                    "API rate limit exceeded.",
                    response=e.response,
                    request=e.request,
                ) from e
            else:
                # General API error for other HTTP issues
                raise APIError(
                    f"API request failed with status {e.response.status_code}",
                    response=e.response,
                    request=e.request,
                ) from e

        except Exception as e:
            # Catch truly unexpected errors outside the retry/http logic
            logger.exception(f"Unexpected error during request processing: {e}")
            # Attempt to get request info if available, otherwise None
            request_info = getattr(e, "request", None)
            # Ensure it's actually an httpx.Request or None
            if not isinstance(request_info, (httpx.Request, type(None))):
                request_info = None # Default to None if it's something else unexpected
            raise AireloomError(f"An unexpected error occurred: {e}", request=request_info) from e

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        data: Mapping[str, Any] | None = None,
        expected_model: type[Any] | None = None,  # For potential future validation
        base_url_override: str | None = None,
    ) -> httpx.Response | Any:
        """
        Performs an asynchronous HTTP request to the specified API path with retries.

        Args:
            method: HTTP method (e.g., "GET", "POST").
            path: API endpoint path (relative to base_url).
            params: URL query parameters.
            json_data: Data to send as JSON in the request body.
            data: Data to send form-encoded in the request body.
            expected_model: Pydantic model to validate the response against (optional).
            base_url_override: Use a different base URL for this specific request.

        Returns:
            The httpx.Response object, or a parsed Pydantic model if expected_model is provided.

        Raises:
            APIError: If the API returns an error status code (4xx, 5xx) after retries.
            TimeoutError: If the request times out after retries.
            NetworkError: If a network-level error occurs.
            AireloomError: For other unexpected client-side errors.
            AuthError: If authentication fails.
            ValidationError: If response parsing/validation fails (when using expected_model).
        """
        response = await self._request_with_retry(
            method=method,
            path=path,
            params=params,
            json_data=json_data,
            data=data,
            base_url_override=base_url_override,
        )

        if expected_model:
            # Placeholder for future response validation using the model
            # try:
            #     return expected_model.model_validate(response.json())
            # except Exception as e:
            #     raise ValidationError(f"Failed to parse/validate response: {e}", response=response) from e
            logger.warning("Response model validation not yet implemented.")
            return response  # Return raw response for now
        return response

    async def aclose(self) -> None:
        """Closes the underlying HTTP client and any auth-specific clients."""
        if self._should_close_client and self._http_client:
            await self._http_client.aclose()
            logger.info("AireloomClient internal HTTP client closed.")
        # Close auth strategy client if it has a close method
        if hasattr(self._auth_strategy, "close") and callable(
            self._auth_strategy.close
        ):
            await self._auth_strategy.close()  # type: ignore

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()
