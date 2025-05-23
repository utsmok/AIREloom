import ssl
from collections.abc import Mapping
from typing import Any, Self

import certifi
import httpx
import tenacity
from tenacity import (
    AsyncRetrying,
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
    # Add ConfigurationError if needed, though not directly used here
)
from .log_config import logger
from .types import RequestData

# Define constants for HTTP status codes
HTTP_BAD_REQUEST = 400
HTTP_TOO_MANY_REQUESTS = 429


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

        self._should_close_client = http_client is None  # Close only if we created it
        self._http_client = http_client or self._create_default_http_client()

        logger.debug("AireloomClient initialized.")

    def _create_default_http_client(self) -> httpx.AsyncClient:
        """Creates a default httpx.AsyncClient with configured settings."""
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            verify_ssl = ssl_context
            logger.debug("Using certifi SSL context.")
        except Exception:
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

            # Ensure User-Agent is set
            if "User-Agent" not in request.headers or not request.headers["User-Agent"]:
                request.headers["User-Agent"] = self._settings.user_agent

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
            if response.status_code >= HTTP_BAD_REQUEST:
                if response.status_code == HTTP_TOO_MANY_REQUESTS:
                    raise RateLimitError("API rate limit exceeded.", response=response)
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    response=response,
                )
            return response

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Request failed with status {e.response.status_code}: {e.request.url}"
            )
            if e.response.status_code == HTTP_TOO_MANY_REQUESTS:
                raise RateLimitError(
                    "API rate limit exceeded.", response=e.response, request=e.request
                ) from e
            # No else needed after raise
            raise APIError(
                f"API request failed with status {e.response.status_code}",
                response=e.response,
                request=e.request,
            ) from e
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {request.url}")
            raise TimeoutError("Request timed out", request=request) from e
        except httpx.NetworkError as e:
            logger.error(f"Network error occurred: {request.url}")
            raise NetworkError("Network error occurred", request=request) from e
        except Exception as e:
            logger.exception(
                f"Unexpected error during single request execution to {request.url}: {e}"
            )
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(
                f"An unexpected error occurred during request execution: {e}",
                request=request,
            ) from e

    def _should_retry_request(self, retry_state: tenacity.RetryCallState) -> bool:
        """Predicate for tenacity: should we retry this request?"""
        outcome = retry_state.outcome
        if not outcome:  # Should not happen with reraise=True, but defensive check
            return False

        if outcome.failed:
            exc = outcome.exception()
            url = "N/A"
            request = getattr(exc, "request", None)  # Use double quotes
            if request:
                url = getattr(request, "url", "N/A")  # Use double quotes

            # Use | for isinstance check
            if isinstance(exc, TimeoutError | NetworkError | RateLimitError):
                logger.warning(f"Retrying due to {type(exc).__name__} for {url}")
                return True
            # Use | for isinstance check
            if isinstance(exc, httpx.TimeoutException | httpx.NetworkError):
                logger.warning(
                    f"Retrying due to {type(exc).__name__} (httpx) for {url}"
                )
                return True

            status_code: int | None = None
            if isinstance(exc, APIError):
                if exc.response is not None:
                    status_code = exc.response.status_code
            elif isinstance(exc, httpx.HTTPStatusError):
                status_code = exc.response.status_code

            if status_code is not None and status_code in self._retryable_status_codes:
                logger.warning(f"Retrying due to status code {status_code} for {url}")
                return True

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
        )

        # Apply authentication *before* retry loop setup, fail fast on auth issues
        try:
            # Build a temporary request just for authentication purposes
            temp_request = request_data.build_request()
            await self._auth_strategy.async_authenticate(temp_request)
            # Update request_data headers if auth added/modified them
            request_data.headers = temp_request.headers
        except AuthError as e:
            logger.error(f"Authentication failed before request: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during pre-request authentication: {e}")
            raise AireloomError(f"Unexpected authentication error: {e}") from e

        # Prepare retry strategy
        retry_strategy = AsyncRetrying(
            stop=stop_after_attempt(self._settings.max_retries + 1),
            wait=wait_exponential(
                multiplier=self._settings.backoff_factor, min=0.1, max=10
            ),
            retry=self._should_retry_request,
            reraise=True,  # Reraise the last exception if all retries fail
        )

        try:
            response = await retry_strategy(self._execute_single_request, request_data)
            return response

        except AuthError as e:
            logger.error(f"Authentication error during request execution: {e}")
            raise e
        except TimeoutError as e:
            logger.warning(
                f"Request timed out after retries: {e.request.url if e.request else 'N/A'}"
            )
            raise e
        except NetworkError as e:
            logger.warning(
                f"Network error after retries: {e.request.url if e.request else 'N/A'}"
            )
            raise e

        except RateLimitError as e:
            logger.warning(
                f"Rate limit error after retries: {e.request.url if e.request else 'N/A'}"
            )
            raise e

        except APIError as e:
            logger.warning(
                f"API error {e.response.status_code if e.response else 'N/A'} after retries: {e.request.url if e.request else 'N/A'}"
            )
            raise e

        except httpx.TimeoutException as e:
            logger.warning(
                f"Request timed out after retries (httpx): {getattr(e.request, 'url', 'N/A')}"
            )
            raise TimeoutError("Request timed out", request=e.request) from e

        except httpx.NetworkError as e:
            logger.warning(
                f"Network error after retries (httpx): {getattr(e.request, 'url', 'N/A')}"
            )
            raise NetworkError("Connection failed", request=e.request) from e

        except httpx.HTTPStatusError as e:
            logger.warning(
                f"HTTP error after retries (httpx): Status {e.response.status_code}, URL: {e.request.url}"
            )
            if e.response.status_code == HTTP_TOO_MANY_REQUESTS:
                raise RateLimitError(
                    "API rate limit exceeded.", response=e.response, request=e.request
                ) from e
            # No else needed after raise
            raise APIError(
                f"API request failed with status {e.response.status_code}",
                response=e.response,
                request=e.request,
            ) from e

        except RetryError as e:
            logger.error(f"Request failed after multiple retries: {e}")
            raise AireloomError("Request failed after multiple retries") from e

        except AireloomError as e:
            raise e  # Re-raise without further wrapping

        except Exception as e:
            logger.exception(f"Unexpected error during request processing: {e}")
            request_info = getattr(e, "request", None)
            # Use | for isinstance check
            if not isinstance(request_info, httpx.Request | type(None)):
                request_info = None
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(
                f"An unexpected error occurred: {e}", request=request_info
            ) from e

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,  # Added alias for json_data
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
            json: Data to send as JSON in the request body (alias for json_data).
            json_data: Data to send as JSON in the request body.
            data: Data to send form-encoded in the request body.
            expected_model: Pydantic model to validate the response against (optional).
            base_url_override: Use a different base URL for this specific request.

        Returns:
            The httpx.Response object, or a parsed Pydantic model if expected_model is provided.

        Raises:
            APIError: If the API returns an error status code (4xx, 5xx) after retries.
            RateLimitError: If the API returns a 429 status code after retries.
            TimeoutError: If the request times out after retries.
            NetworkError: If a network-level error occurs.
            AuthError: If authentication fails.
            AireloomError: For other unexpected client-side errors.
            ValidationError: If response parsing/validation fails (when using expected_model).
        """
        # Allow using 'json' as an alias for 'json_data'
        actual_json_data = json_data if json_data is not None else json
        if json is not None and json_data is not None:
            logger.warning(
                "Both 'json' and 'json_data' provided to request; using 'json_data'."
            )

        response = await self._request_with_retry(
            method=method,
            path=path,
            params=params,
            json_data=actual_json_data,  # Use the determined json data
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
