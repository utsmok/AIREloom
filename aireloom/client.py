import asyncio
import ssl
import time
from collections.abc import Mapping
from datetime import UTC, datetime as dt
from email.utils import parsedate_to_datetime
from http import HTTPStatus
from typing import Any, Self

import certifi
import httpx
import tenacity
from cachetools import TTLCache  # Added for caching
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
    OPENAIRE_SCHOLIX_API_BASE_URL,  # Added for ScholixClient default
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
from .resources import (  # Import resource clients
    DataSourcesClient,
    OrganizationsClient,
    ProjectsClient,
    ResearchProductsClient,
    ScholixClient,
)
from .types import RequestData

# Define constants for HTTP status codes
# HTTP_BAD_REQUEST = 400 # Replaced by HTTPStatus.BAD_REQUEST
# HTTP_TOO_MANY_REQUESTS = 429 # Replaced by HTTPStatus.TOO_MANY_REQUESTS


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
        scholix_base_url: str = OPENAIRE_SCHOLIX_API_BASE_URL,  # Added Scholix base URL
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
            scholix_base_url: The base URL for the Scholix API.
            http_client: Optional pre-configured httpx.AsyncClient instance.
            retryable_status_codes: Set of HTTP status codes to retry on.
        """
        self._settings = settings or get_settings()
        logger.debug(
            f"AireloomClient.__init__ self._settings at LINE 100: id={id(self._settings)}, client_id={self._settings.openaire_client_id}, token={self._settings.openaire_api_token}, timeout={self._settings.request_timeout}"
        )
        self._base_url = base_url.rstrip("/")
        self._scholix_base_url = scholix_base_url.rstrip("/")  # Store Scholix base URL
        self._retryable_status_codes = retryable_status_codes

        # Initialize cache
        self._cache: TTLCache | None = None
        if self._settings.enable_caching:
            logger.info(
                f"Client-side caching enabled. Max size: {self._settings.cache_max_size}, "
                f"TTL: {self._settings.cache_ttl_seconds}s"
            )
            self._cache = TTLCache(
                maxsize=self._settings.cache_max_size,
                ttl=self._settings.cache_ttl_seconds,
            )

        self._auth_strategy: AuthStrategy
        if auth_strategy:
            logger.info(
                f"Using explicitly provided authentication strategy: {type(auth_strategy).__name__}"
            )
            self._auth_strategy = auth_strategy
        else:
            # Use overrides if provided, otherwise use settings
            logger.debug(
                f"Auth decision: client_id_param={client_id}, "
                f"settings_client_id={self._settings.openaire_client_id}, "
                f"api_token_param={api_token}, "
                f"settings_api_token={self._settings.openaire_api_token}"
            )
            logger.info(
                "Did not receive an explicit auth_strategy, determining auth type based on provided parameters or settings."
            )
            _client_id = client_id or self._settings.openaire_client_id
            _client_secret = client_secret or self._settings.openaire_client_secret
            _api_token = api_token or self._settings.openaire_api_token
            _token_url = self._settings.openaire_token_url

            if _client_id and _client_secret:
                logger.info(
                    "_client_id and _client_secret available. Using Client Credentials authentication."
                )
                if client_id and client_secret:
                    logger.info("id and secret were directly passed as parameters.")
                else:
                    logger.info(
                        "id and secret were loaded from settings or environment variables."
                    )
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

        # Rate limiting state
        self._rate_limit_limit: int | None = None
        self._rate_limit_remaining: int | None = None
        self._rate_limit_reset_timestamp: float | None = None  # Unix timestamp
        self._rate_limit_lock = asyncio.Lock()

        # Initialize resource clients
        self._research_products = ResearchProductsClient(api_client=self)
        self._organizations = OrganizationsClient(api_client=self)
        self._projects = ProjectsClient(api_client=self)
        self._data_sources = DataSourcesClient(api_client=self)
        self._scholix = ScholixClient(
            api_client=self, scholix_base_url=self._scholix_base_url
        )

        logger.debug("AireloomClient initialized.")

    @property
    def research_products(self) -> ResearchProductsClient:
        """Access ResearchProductsClient."""
        return self._research_products

    @property
    def organizations(self) -> OrganizationsClient:
        """Access OrganizationsClient."""
        return self._organizations

    @property
    def projects(self) -> ProjectsClient:
        """Access ProjectsClient."""
        return self._projects

    @property
    def data_sources(self) -> DataSourcesClient:
        """Access DataSourcesClient."""
        return self._data_sources

    @property
    def scholix(self) -> ScholixClient:
        """Access ScholixClient."""
        return self._scholix

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
            base_url=self._base_url,  # Default base_url for most requests
            timeout=self._settings.request_timeout,
            verify=verify_ssl,
            headers={"User-Agent": self._settings.user_agent},
            # Add transport/proxy settings from config if needed later
        )

    async def _parse_rate_limit_headers(self, response: httpx.Response) -> float | None:
        """
        Parses rate limit headers from the response and updates client state.
        Returns the 'Retry-After' duration in seconds, if present.
        """
        retry_after_seconds: float | None = None
        async with self._rate_limit_lock:
            try:
                limit_str = response.headers.get("X-RateLimit-Limit")
                if limit_str and limit_str.isdigit():
                    self._rate_limit_limit = int(limit_str)
                    logger.debug(f"Parsed X-RateLimit-Limit: {self._rate_limit_limit}")

                remaining_str = response.headers.get("X-RateLimit-Remaining")
                if remaining_str and remaining_str.isdigit():
                    self._rate_limit_remaining = int(remaining_str)
                    logger.debug(
                        f"Parsed X-RateLimit-Remaining: {self._rate_limit_remaining}"
                    )

                reset_str = response.headers.get("X-RateLimit-Reset")
                if reset_str and reset_str.isdigit():
                    self._rate_limit_reset_timestamp = float(reset_str)
                    logger.debug(
                        f"Parsed X-RateLimit-Reset: {self._rate_limit_reset_timestamp}"
                    )
                elif reset_str:  # Could be an HTTP date
                    try:
                        dt_reset_obj = parsedate_to_datetime(
                            reset_str
                        )  # Renamed variable
                        self._rate_limit_reset_timestamp = (
                            dt_reset_obj.timestamp()
                        )  # Used renamed variable
                        logger.debug(
                            f"Parsed X-RateLimit-Reset (HTTP date): {self._rate_limit_reset_timestamp}"
                        )
                    except Exception:
                        logger.warning(
                            f"Could not parse X-RateLimit-Reset HTTP date: {reset_str}"
                        )

                retry_after_header = response.headers.get("Retry-After")
                if retry_after_header:
                    if retry_after_header.isdigit():
                        retry_after_seconds = float(retry_after_header)
                        logger.debug(
                            f"Parsed Retry-After (seconds): {retry_after_seconds}"
                        )
                    else:
                        try:
                            # Attempt to parse as HTTP-date
                            retry_dt_obj = parsedate_to_datetime(
                                retry_after_header
                            )  # Renamed variable
                            # Ensure it's timezone-aware for correct comparison
                            if (
                                retry_dt_obj.tzinfo is None  # Used renamed variable
                                or retry_dt_obj.tzinfo.utcoffset(retry_dt_obj)
                                is None  # Used renamed variable
                            ):
                                logger.warning(
                                    f"Retry-After date '{retry_after_header}' is naive, assuming UTC."
                                )
                                retry_dt_obj = retry_dt_obj.replace(
                                    tzinfo=UTC
                                )  # Used renamed variable

                            now_dt_obj = dt.now(
                                UTC
                            )  # Used aliased dt and renamed variable
                            delta = retry_dt_obj - now_dt_obj  # Used renamed variables
                            retry_after_seconds = max(0, delta.total_seconds())
                            logger.debug(
                                f"Parsed Retry-After (HTTP date): {retry_after_header}, calculated seconds: {retry_after_seconds}"
                            )
                        except Exception as e:
                            logger.warning(
                                f"Could not parse Retry-After HTTP date '{retry_after_header}': {e}"
                            )
            except Exception as e:
                logger.exception(f"Error parsing rate limit headers: {e}")
        return retry_after_seconds

    async def _execute_single_request(
        self, request_data: RequestData, expected_model: type[Any] | None = None
    ) -> tuple[httpx.Response, Any | None]:
        """
        Executes a single HTTP request attempt, runs hooks, and parses if model provided.
        """
        # --- Pre-Request Hooks ---
        # Prepare mutable versions of params and headers for hooks
        hook_params: dict[str, Any] | None = (
            dict(request_data.params) if request_data.params is not None else None
        )
        hook_headers: httpx.Headers = httpx.Headers(request_data.headers)

        if self._settings.pre_request_hooks:
            logger.debug(
                f"Executing {len(self._settings.pre_request_hooks)} pre-request hooks "
                f"for {request_data.method} {request_data.url}"
            )
            for hook in self._settings.pre_request_hooks:
                try:
                    hook(
                        request_data.method,
                        request_data.url,
                        hook_params,
                        hook_headers,
                    )
                except Exception as e:
                    logger.error(
                        f"Error executing pre-request hook {getattr(hook, '__name__', str(hook))}: {e}",
                        exc_info=True,
                    )

            # Update request_data from potentially modified hook_params and hook_headers
            request_data.params = hook_params
            # Convert modified hook_headers (httpx.Headers) back to a dict for request_data.headers
            # httpx.Headers.items() gives (name, value) for the first value of each header.
            request_data.headers = {k: v for k, v in hook_headers.items()}

        request = request_data.build_request()
        response: httpx.Response | None = None
        parsed_model: Any | None = None
        retry_after_from_headers: float | None = None
        try:
            # Apply authentication just before sending
            await self._auth_strategy.async_authenticate(request)

            # Ensure User-Agent is set
            if "User-Agent" not in request.headers or not request.headers["User-Agent"]:
                request.headers["User-Agent"] = self._settings.user_agent

            logger.debug(f"Sending request: {request.method} {request.url}")
            logger.trace(f"Request Headers: {request.headers}")
            if request.content:
                logger.trace(f"Request Body: {request.content.decode()}")

            response = await self._http_client.send(request)
            retry_after_from_headers = await self._parse_rate_limit_headers(response)

            logger.debug(f"Received response: {response.status_code} for {request.url}")
            logger.trace(f"Response Headers: {response.headers}")

            if response.status_code >= HTTPStatus.BAD_REQUEST:
                if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                    if self._settings.enable_rate_limiting:
                        wait_duration = (
                            retry_after_from_headers
                            or self._settings.rate_limit_retry_after_default
                        )
                        logger.info(
                            f"Rate limit hit (429). Raising RateLimitError. Retry will be handled by tenacity with appropriate wait. Wait duration hint from server: {wait_duration:.2f}s. Client open: {not self._http_client.is_closed if self._http_client else 'N/A'}"
                        )
                        # Removed direct asyncio.sleep(wait_duration) here.
                        # Tenacity will handle retries and waiting for RateLimitError.
                    logger.error(
                        f"Raising RateLimitError after 429. Client open: {not self._http_client.is_closed if self._http_client else 'N/A'}"
                    )
                    raise RateLimitError("API rate limit exceeded.", response=response)
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    response=response,
                )

            # Successful response, try parsing if expected_model is provided
            if expected_model:
                try:
                    parsed_model = expected_model.model_validate(response.json())
                except Exception as e:
                    logger.warning(
                        f"Response model validation failed for {request.url}: {e}. "
                        "Parsed model will be None."
                    )
                    # parsed_model remains None

            # --- Post-Request Hooks ---
            if self._settings.post_request_hooks:
                logger.debug(
                    f"Executing {len(self._settings.post_request_hooks)} post-request hooks "
                    f"for {request.method} {request.url}"
                )
                for hook in self._settings.post_request_hooks:
                    try:
                        hook(response, parsed_model)  # parsed_model can be None
                    except Exception as e:
                        logger.error(
                            f"Error executing post-request hook {getattr(hook, '__name__', str(hook))}: {e}",
                            exc_info=True,
                        )

            return response, parsed_model

        except httpx.HTTPStatusError as e:
            # This block might be hit if httpx raises before our status check,
            # e.g., if using response.raise_for_status() internally somewhere (not currently).
            # Ensure headers are parsed if a response object is available.
            if e.response:
                retry_after_from_headers = await self._parse_rate_limit_headers(
                    e.response
                )

            logger.error(
                f"Request failed with status {e.response.status_code}: {e.request.url}"
            )
            if e.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                if self._settings.enable_rate_limiting:
                    wait_duration = (
                        retry_after_from_headers
                        or self._settings.rate_limit_retry_after_default
                    )
                    logger.info(
                        f"Rate limit hit (429) in HTTPStatusError. Waiting for {wait_duration:.2f}s."
                    )
                    await asyncio.sleep(wait_duration)
                raise RateLimitError(
                    "API rate limit exceeded.", response=e.response, request=e.request
                ) from e
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
            # If response was received before another exception, parse its headers.
            if response:  # Check if response object exists
                await self._parse_rate_limit_headers(response)

            logger.exception(
                f"Unexpected error during single request execution to {request.url}: {e}"
            )
            if isinstance(e, AireloomError):  # If it's already our error, re-raise
                # If it's a RateLimitError, we might have already slept.
                # However, the sleep logic is tied to the initial 429 detection.
                # If another error happens *after* a 429 but before tenacity retries,
                # this path is complex. For now, assume tenacity handles retries post-sleep.
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
        expected_model: type[Any] | None = None,  # Added expected_model
    ) -> tuple[httpx.Response, Any | None]:  # Returns a tuple
        """Makes an HTTP request with configured retries for transient errors."""
        # Determine the correct base URL for this request
        # If base_url_override is provided, use it. Otherwise, use the client's default.
        # The default httpx.AsyncClient is initialized with self._base_url.
        # If base_url_override is different, we need to construct the full URL manually
        # or ensure the httpx.Request object uses the override.
        # For simplicity, if base_url_override is given, we form the full URL here.
        # Otherwise, the path will be relative to self._http_client.base_url.

        _target_base_url = (base_url_override or self._base_url).rstrip("/")
        full_url = f"{_target_base_url}/{path.lstrip('/')}"

        request_data = RequestData(
            method=method,
            url=full_url,  # Pass the full URL
            params=params,
            json_data=json_data,
            data=data,
            # Headers will be populated by auth strategy and pre-request hooks
        )

        # Pre-request rate limit check
        if self._settings.enable_rate_limiting:
            async with self._rate_limit_lock:
                # Check if we have rate limit information
                if (
                    self._rate_limit_remaining is not None
                    and self._rate_limit_limit is not None
                    and self._rate_limit_limit > 0
                ):
                    # Check if remaining requests are below the buffer or zero
                    buffer_threshold = (
                        self._rate_limit_limit
                        * self._settings.rate_limit_buffer_percentage
                    )
                    if (
                        self._rate_limit_remaining <= buffer_threshold
                        or self._rate_limit_remaining == 0
                    ):
                        if self._rate_limit_reset_timestamp is not None:
                            current_time = time.time()
                            wait_time = self._rate_limit_reset_timestamp - current_time
                            if wait_time > 0:
                                logger.info(
                                    f"Rate limit approaching/reached. "
                                    f"Remaining: {self._rate_limit_remaining}/{self._rate_limit_limit}. "
                                    f"Waiting for {wait_time:.2f}s until reset."
                                )
                                await asyncio.sleep(wait_time)
                        elif (
                            self._rate_limit_remaining == 0
                        ):  # Reset time is past but remaining is 0
                            logger.warning(
                                f"Rate limit reset time {self._rate_limit_reset_timestamp} is past "
                                f"but remaining requests is {self._rate_limit_remaining}. "
                                f"Waiting for default: {self._settings.rate_limit_retry_after_default}s."
                            )
                            await asyncio.sleep(
                                self._settings.rate_limit_retry_after_default
                            )
                        elif (
                            self._rate_limit_remaining == 0
                        ):  # No reset time, but remaining is 0
                            logger.warning(
                                f"Rate limit remaining is {self._rate_limit_remaining} and no reset time known. "
                                f"Waiting for default: {self._settings.rate_limit_retry_after_default}s."
                            )
                            await asyncio.sleep(
                                self._settings.rate_limit_retry_after_default
                            )
                elif self._rate_limit_remaining == 0 and self._rate_limit_limit is None:
                    # If remaining is 0 (e.g. from a 429) but we never got a limit header
                    logger.warning(
                        f"Rate limit remaining is 0 (likely from a 429) but no limit/reset headers were ever parsed. "
                        f"Waiting for default: {self._settings.rate_limit_retry_after_default}s as a precaution."
                    )
                    await asyncio.sleep(self._settings.rate_limit_retry_after_default)

        # Apply authentication *before* retry loop setup, fail fast on auth issues
        # This also populates initial headers in request_data
        try:
            # Build a temporary request to apply auth and get initial headers
            temp_request_for_auth = request_data.build_request()
            await self._auth_strategy.async_authenticate(temp_request_for_auth)
            # Update request_data.headers with those from the auth strategy
            request_data.headers = dict(temp_request_for_auth.headers)
        except AuthError as e:
            logger.error(f"Authentication failed before request: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during pre-request authentication: {e}")
            raise AireloomError(f"Unexpected authentication error: {e}") from e

        # Prepare retry strategy
        retry_strategy = AsyncRetrying(
            stop=stop_after_attempt(
                self._settings.max_retries + 1
            ),  # +1 for initial attempt
            wait=wait_exponential(
                multiplier=self._settings.backoff_factor,
            ),
            retry=self._should_retry_request,
            reraise=True,  # Reraise the exception if all retries fail
            before_sleep=self._before_retry_sleep,  # Log before sleeping
        )
        try:
            return await retry_strategy.__call__(
                self._execute_single_request, request_data, expected_model
            )
        except RetryError as e:  # This catches tenacity's RetryError
            logger.error(
                f"All retries failed for {request_data.url}. Last exception: {e.last_attempt.exception() if e.last_attempt else 'Unknown'}"
            )
            # Re-raise the original exception that caused the retries to fail
            if e.last_attempt and e.last_attempt.failed:
                original_exception = e.last_attempt.exception()
                if original_exception:
                    raise original_exception from e
            # Fallback if for some reason last_attempt is not available
            raise AireloomError(
                f"All retries failed for {request_data.url}. No specific last exception captured."
            ) from e

    async def _before_retry_sleep(self, retry_state: tenacity.RetryCallState) -> None:
        """Log details before tenacity sleeps between retries."""
        if not retry_state.outcome:  # Should not happen
            return

        exc = retry_state.outcome.exception()
        url = "N/A"
        request_info = ""
        if exc and hasattr(exc, "request") and getattr(exc, "request", None):
            request = getattr(exc, "request", None)
            if request:
                url = str(getattr(request, "url", "N/A"))
                method = str(getattr(request, "method", "N/A"))
                request_info = f"for {method} {url}"

        sleep_time = (
            getattr(retry_state.next_action, "sleep", 0)
            if retry_state.next_action
            else 0
        )
        logger.info(
            f"Retrying request {request_info} in {sleep_time:.2f} seconds "
            f"after {retry_state.attempt_number} attempt(s) due to: {type(exc).__name__} - {exc}"
        )

    def _generate_cache_key(
        self, method: str, url: str, params: Mapping[str, Any] | None = None
    ) -> str:
        """
        Generate a cache key from the request method, URL, and parameters.

        Args:
            method: HTTP method (e.g., 'GET', 'POST')
            url: Full URL for the request
            params: Query parameters dict

        Returns:
            A unique cache key string
        """
        import hashlib
        import json

        # Start with method and URL
        key_parts = [method.upper(), url]

        # Add sorted parameters if they exist
        if params:
            # Sort parameters to ensure consistent cache keys
            sorted_params = json.dumps(params, sort_keys=True, separators=(",", ":"))
            key_parts.append(sorted_params)

        # Create a hash of the combined key parts
        cache_key_string = "|".join(key_parts)
        return hashlib.md5(cache_key_string.encode("utf-8")).hexdigest()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,  # Added alias for json_data
        json_data: Any | None = None,
        data: Mapping[str, Any] | None = None,
        expected_model: type[Any] | None = None,
        base_url_override: str | None = None,
    ) -> httpx.Response | Any:
        """
        Performs an asynchronous HTTP request to the specified API path with retries,
        with optional client-side caching for GET requests.
        Hooks are executed within the retry mechanism for the actual request.
        """
        actual_json_data = json_data if json_data is not None else json
        if json is not None and json_data is not None:
            logger.warning(
                "Both 'json' and 'json_data' provided to request; using 'json_data'."
            )

        cache_key: str | None = None

        # --- Cache Check (for GET requests) ---
        if self._cache is not None and method.upper() == "GET":
            _target_base_url = (base_url_override or self._base_url).rstrip("/")
            full_url = f"{_target_base_url}/{path.lstrip('/')}"
            cache_key = self._generate_cache_key(method, full_url, params)

            cached_item = self._cache.get(cache_key)
            if cached_item is not None:
                # Assuming the cached item is the already parsed Pydantic model
                logger.debug(f"Cache hit for key: {cache_key}")
                if expected_model and not isinstance(cached_item, expected_model):
                    logger.warning(
                        f"Cache hit for {cache_key}, but type mismatch. "
                        f"Expected {expected_model}, got {type(cached_item)}. Discarding cache."
                    )
                    self._cache.pop(cache_key, None)  # Treat as cache miss
                else:
                    logger.debug(f"Returning cached parsed model for key: {cache_key}")
                    return cached_item  # cached_item is the parsed_model

        # --- Execute Request (if not a cache hit or not cacheable) ---
        # _request_with_retry now returns (httpx.Response, ParsedModel | None)
        # Hooks are executed within _execute_single_request, called by _request_with_retry
        response, parsed_model = await self._request_with_retry(
            method=method,
            path=path,
            params=params,
            json_data=actual_json_data,
            data=data,
            base_url_override=base_url_override,
            expected_model=expected_model,
        )

        # --- Cache Store (for successful GET requests with a successfully parsed model) ---
        if (
            self._cache is not None
            and cache_key is not None  # Implies GET and cache enabled
            and method.upper() == "GET"
            and HTTPStatus.OK
            <= response.status_code
            < HTTPStatus.MULTIPLE_CHOICES  # 2xx
        ):
            if expected_model and parsed_model is not None:
                # Ensure what we are caching is indeed of the expected_model type
                if isinstance(parsed_model, expected_model):
                    self._cache[cache_key] = (
                        parsed_model  # Store the already parsed model
                    )
                    logger.debug(f"Cached parsed model for key: {cache_key}")
                else:
                    # This case should ideally not happen if parsing was successful
                    # and parsed_model is not None. But as a safeguard:
                    logger.warning(
                        f"Attempted to cache for key {cache_key}, but parsed_model type "
                        f"{type(parsed_model)} does not match expected_model {expected_model}. Not caching."
                    )
            elif expected_model and parsed_model is None:
                logger.debug(  # Changed from warning to debug as this is an expected path if parsing fails
                    f"GET request for {cache_key} successful, but model parsing failed or no model to parse. Not caching."
                )
            # If no expected_model, parsed_model is None, nothing to cache here.

        # --- Standard Response Handling ---
        if expected_model:
            if parsed_model is not None and isinstance(parsed_model, expected_model):
                return parsed_model  # Return the successfully parsed model
            # Parsing failed inside _execute_single_request (parsed_model is None)
            # or it's not of the expected type (should be rare if parsing succeeded).
            logger.warning(
                f"Expected model {expected_model.__name__} but parsing failed, model was None, "
                f"or type mismatch for {method} {path}. Returning raw response."
            )
            return response  # Fallback to raw response

        return response  # Default: return raw response if no expected_model

    async def aclose(self) -> None:
        """Closes the underlying HTTP client and any auth-specific clients."""
        logger.info(
            f"AireloomClient.aclose() called. Client ID: {id(self)}. HTTP client to close: {self._should_close_client and self._http_client is not None}. HTTP client closed: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
        if (
            self._should_close_client
            and self._http_client
            and not self._http_client.is_closed
        ):
            await self._http_client.aclose()
            logger.info(
                f"AireloomClient internal HTTP client closed. Client ID: {id(self)}."
            )
        elif self._http_client and self._http_client.is_closed:
            logger.info(
                f"AireloomClient.aclose(): HTTP client was already closed. Client ID: {id(self)}"
            )
        # Close auth strategy client if it has an async_close method
        if hasattr(self._auth_strategy, "async_close") and callable(
            self._auth_strategy.async_close
        ):
            await self._auth_strategy.async_close()  # type: ignore

    async def __aenter__(self) -> Self:
        logger.info(
            f"AireloomClient.__aenter__() called. Client ID: {id(self)}. HTTP client closed: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.info(
            f"AireloomClient.__aexit__() called. Client ID: {id(self)}. HTTP client closed before aclose: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
        await self.aclose()
        logger.info(
            f"AireloomClient.__aexit__() finished. Client ID: {id(self)}. HTTP client closed after aclose: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
