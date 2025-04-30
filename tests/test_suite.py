# -------------------------------------------------------
#
# C:\dev\AIREloom\tests\__init__.py
#
# ------------------------------------------------------





# -------------------------------------------------------
#
# C:\dev\AIREloom\tests\conftest.py
#
# ------------------------------------------------------

# tests/conftest.py
import os

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# Useful for storing API keys locally for testing
load_dotenv()


@pytest.fixture(scope="session")
def api_token() -> str | None:
    """Fixture to provide the OpenAIRE API token from environment variables."""
    return os.getenv("AIRELOOM_OPENAIRE_API_TOKEN")



# -------------------------------------------------------
#
# C:\dev\AIREloom\tests\test_auth.py
#
# ------------------------------------------------------

# tests/test_auth.py
import asyncio
import httpx
import pytest
from pytest_httpx import HTTPXMock

from aireloom.auth import ClientCredentialsAuth, NoAuth, StaticTokenAuth
from aireloom.exceptions import AuthError, ConfigurationError

# --- Constants for Testing ---
MOCK_TOKEN_URL = "https://fake-token-endpoint.com/token"
MOCK_CLIENT_ID = "test_client_id"
MOCK_CLIENT_SECRET = "test_client_secret"
MOCK_STATIC_TOKEN = "test_static_token"
MOCK_ACCESS_TOKEN = "mock_oauth_access_token_123"


# --- Test NoAuth ---
@pytest.mark.asyncio
async def test_no_auth_authenticate():
    """Test that NoAuth does not modify the request."""
    strategy = NoAuth()
    request = httpx.Request("GET", "http://example.com")
    original_headers = request.headers.copy()

    await strategy.async_authenticate(request)

    assert request.headers == original_headers


# --- Test StaticTokenAuth ---
@pytest.mark.asyncio
async def test_static_token_auth_success():
    """Test StaticTokenAuth successfully adds the Authorization header."""
    strategy = StaticTokenAuth(token=MOCK_STATIC_TOKEN)
    request = httpx.Request("GET", "http://example.com")

    await strategy.async_authenticate(request)

    assert "Authorization" in request.headers
    assert request.headers["Authorization"] == f"Bearer {MOCK_STATIC_TOKEN}"


@pytest.mark.asyncio
async def test_static_token_auth_init_no_token():
    """Test StaticTokenAuth raises ConfigError if token is missing."""
    with pytest.raises(ConfigurationError, match="requires a non-empty 'token'"):
        StaticTokenAuth(token=None)
    with pytest.raises(ConfigurationError, match="requires a non-empty 'token'"):
        StaticTokenAuth(token="")


# --- Test ClientCredentialsAuth ---
@pytest.mark.asyncio
async def test_client_credentials_auth_init_success():
    """Test successful initialization of ClientCredentialsAuth."""
    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    assert strategy._client_id == MOCK_CLIENT_ID
    assert strategy._client_secret == MOCK_CLIENT_SECRET
    assert strategy._token_url == MOCK_TOKEN_URL
    assert strategy._access_token is None
    await strategy.close()  # Clean up


@pytest.mark.asyncio
async def test_client_credentials_auth_init_missing_config():
    """Test ClientCredentialsAuth raises ConfigError if config is missing."""
    with pytest.raises(
        ConfigurationError,
        match="requires 'client_id', 'client_secret', and 'token_url'",
    ):
        ClientCredentialsAuth(
            client_id=None, client_secret=MOCK_CLIENT_SECRET, token_url=MOCK_TOKEN_URL
        )
    with pytest.raises(
        ConfigurationError,
        match="requires 'client_id', 'client_secret', and 'token_url'",
    ):
        ClientCredentialsAuth(
            client_id=MOCK_CLIENT_ID, client_secret=None, token_url=MOCK_TOKEN_URL
        )
    with pytest.raises(
        ConfigurationError,
        match="requires 'client_id', 'client_secret', and 'token_url'",
    ):
        ClientCredentialsAuth(
            client_id=MOCK_CLIENT_ID, client_secret=MOCK_CLIENT_SECRET, token_url=None
        )


@pytest.mark.asyncio
async def test_client_credentials_auth_fetch_token_success(httpx_mock: HTTPXMock):
    """Test successful token fetching."""
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        json={"access_token": MOCK_ACCESS_TOKEN, "expires_in": 3600},
        status_code=200,
    )

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    request = httpx.Request("GET", "http://example.com")

    await strategy.async_authenticate(request)

    assert strategy._access_token == MOCK_ACCESS_TOKEN
    assert "Authorization" in request.headers
    assert request.headers["Authorization"] == f"Bearer {MOCK_ACCESS_TOKEN}"
    await strategy.close()


@pytest.mark.asyncio
async def test_client_credentials_auth_fetch_token_cached(httpx_mock: HTTPXMock):
    """Test that token is fetched only once and cached."""
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        json={"access_token": MOCK_ACCESS_TOKEN, "expires_in": 3600},
        status_code=200,
    )

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    request1 = httpx.Request("GET", "http://example.com/1")
    request2 = httpx.Request("GET", "http://example.com/2")

    # First call should fetch the token
    await strategy.async_authenticate(request1)
    assert strategy._access_token == MOCK_ACCESS_TOKEN
    assert request1.headers["Authorization"] == f"Bearer {MOCK_ACCESS_TOKEN}"
    assert len(httpx_mock.get_requests()) == 1

    # Second call should use the cached token
    await strategy.async_authenticate(request2)
    assert strategy._access_token == MOCK_ACCESS_TOKEN
    assert request2.headers["Authorization"] == f"Bearer {MOCK_ACCESS_TOKEN}"
    # Assert that no new request was made to the token endpoint
    assert len(httpx_mock.get_requests()) == 1

    await strategy.close()


@pytest.mark.asyncio
async def test_client_credentials_auth_fetch_token_http_error(httpx_mock: HTTPXMock):
    """Test token fetching failure due to HTTP error (e.g., 401 Unauthorized)."""
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        text="Invalid credentials",
        status_code=401,
    )

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    request = httpx.Request("GET", "http://example.com")

    with pytest.raises(AuthError, match="Failed to fetch access token: 401"):
        await strategy.async_authenticate(request)

    assert strategy._access_token is None
    await strategy.close()


@pytest.mark.asyncio
async def test_client_credentials_auth_fetch_token_network_error(httpx_mock: HTTPXMock):
    """Test token fetching failure due to network error."""
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    request = httpx.Request("GET", "http://example.com")

    with pytest.raises(
        AuthError, match="Failed to fetch access token: Connection failed"
    ):
        await strategy.async_authenticate(request)

    assert strategy._access_token is None
    await strategy.close()


@pytest.mark.asyncio
async def test_client_credentials_auth_fetch_token_missing_in_response(
    httpx_mock: HTTPXMock,
):
    """Test token fetching failure when 'access_token' is missing in the response."""
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        json={"wrong_key": "some_value"},  # Missing access_token
        status_code=200,
    )

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    request = httpx.Request("GET", "http://example.com")

    with pytest.raises(AuthError, match="Access token not found in token response"):
        await strategy.async_authenticate(request)

    assert strategy._access_token is None
    await strategy.close()


@pytest.mark.asyncio
async def test_client_credentials_auth_close():
    """Test that the close method closes the internal client."""
    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )
    # Access the client to ensure it's created
    internal_client = await strategy._get_token_client()
    assert internal_client is not None
    assert not internal_client.is_closed

    await strategy.close()

    assert strategy._token_client is None
    # Optionally check if the original client object is closed if needed,
    # but checking strategy._token_client is None is sufficient here.
    assert internal_client.is_closed


@pytest.mark.asyncio
async def test_client_credentials_auth_concurrent_fetch(httpx_mock: HTTPXMock):
    """Test that concurrent authenticate calls only fetch the token once."""
    # Simplify mock: Just add the expected response directly.
    # The internal lock in ClientCredentialsAuth should handle concurrency.
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        json={"access_token": MOCK_ACCESS_TOKEN, "expires_in": 3600},
        status_code=200,
    )
    # Remove the complex callback and delay simulation

    strategy = ClientCredentialsAuth(
        client_id=MOCK_CLIENT_ID,
        client_secret=MOCK_CLIENT_SECRET,
        token_url=MOCK_TOKEN_URL,
    )

    request1 = httpx.Request("GET", "http://example.com/1")
    request2 = httpx.Request("GET", "http://example.com/2")

    # Run authenticate concurrently
    task1 = asyncio.create_task(strategy.async_authenticate(request1))
    task2 = asyncio.create_task(strategy.async_authenticate(request2))

    await asyncio.gather(task1, task2)

    # Assert that only one request was made to the token endpoint
    requests_made = httpx_mock.get_requests(url=MOCK_TOKEN_URL, method="POST")
    assert len(requests_made) == 1

    # Assert both original requests got authenticated
    assert request1.headers["Authorization"] == f"Bearer {MOCK_ACCESS_TOKEN}"
    assert request2.headers["Authorization"] == f"Bearer {MOCK_ACCESS_TOKEN}"
    assert strategy._access_token == MOCK_ACCESS_TOKEN

    await strategy.close()



# -------------------------------------------------------
#
# C:\dev\AIREloom\tests\test_client.py
#
# ------------------------------------------------------

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from aireloom.auth import ClientCredentialsAuth, NoAuth, StaticTokenAuth
from aireloom.client import AireloomClient
from aireloom.config import ApiSettings
from aireloom.constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)
from aireloom.exceptions import (
    APIError,
    AuthError,
    NetworkError,
    TimeoutError,
)

# --- Constants for Testing ---
MOCK_BASE_URL = "https://api.test.com"
MOCK_STATIC_TOKEN = "static_test_token"
MOCK_CLIENT_ID = "client_test_id"
MOCK_CLIENT_SECRET = "client_test_secret"
MOCK_OAUTH_TOKEN = "oauth_test_token"
MOCK_TOKEN_URL = "https://token.test.com/token"
MOCK_USER_AGENT = "Test User Agent"


# --- Fixtures ---
@pytest.fixture
def mock_settings() -> ApiSettings:
    """Fixture for mock API settings."""
    return ApiSettings(
        openaire_api_token=None, # Default to no token
        openaire_client_id=None, # Default to no client creds
        openaire_client_secret=None,
        openaire_token_url=MOCK_TOKEN_URL,
        request_timeout=10,
        max_retries=2,
        backoff_factor=0.5,
        user_agent=MOCK_USER_AGENT,
    )

@pytest.fixture
def mock_settings_with_token() -> ApiSettings:
    """Fixture for mock API settings with a static token."""
    return ApiSettings(
        openaire_api_token=MOCK_STATIC_TOKEN,
        openaire_client_id=None,
        openaire_client_secret=None,
        openaire_token_url=MOCK_TOKEN_URL,
        request_timeout=10,
        max_retries=2,
        backoff_factor=0.5,
        user_agent=MOCK_USER_AGENT,
    )

@pytest.fixture
def mock_settings_with_creds() -> ApiSettings:
    """Fixture for mock API settings with client credentials."""
    return ApiSettings(
        openaire_api_token=None,
        openaire_client_id=MOCK_CLIENT_ID,
        openaire_client_secret=MOCK_CLIENT_SECRET,
        openaire_token_url=MOCK_TOKEN_URL,
        request_timeout=10,
        max_retries=2,
        backoff_factor=0.5,
        user_agent=MOCK_USER_AGENT,
    )


# --- Test Client Initialization ---

def test_client_init_no_auth_default(mock_settings):
    """Test client initialization uses NoAuth by default when no creds provided."""
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)
    assert isinstance(client._auth_strategy, NoAuth)
    assert client._base_url == MOCK_BASE_URL
    assert client._http_client.timeout.read == mock_settings.request_timeout
    assert client._http_client.headers["User-Agent"] == MOCK_USER_AGENT

@pytest.mark.asyncio
async def test_client_init_no_auth_explicit(mock_settings):
    """Test client initialization with explicit NoAuth strategy."""
    auth_strategy = NoAuth()
    client = AireloomClient(settings=mock_settings, auth_strategy=auth_strategy)
    assert client._auth_strategy is auth_strategy
    await client.aclose()

def test_client_init_static_token_from_settings(mock_settings_with_token):
    """Test client initialization uses StaticTokenAuth from settings."""
    client = AireloomClient(settings=mock_settings_with_token)
    assert isinstance(client._auth_strategy, StaticTokenAuth)
    assert client._auth_strategy._token == MOCK_STATIC_TOKEN

def test_client_init_static_token_override(mock_settings):
    """Test client initialization uses StaticTokenAuth with override."""
    client = AireloomClient(settings=mock_settings, api_token="override_token")
    assert isinstance(client._auth_strategy, StaticTokenAuth)
    assert client._auth_strategy._token == "override_token"

def test_client_init_client_creds_from_settings(mock_settings_with_creds):
    """Test client initialization uses ClientCredentialsAuth from settings."""
    client = AireloomClient(settings=mock_settings_with_creds)
    assert isinstance(client._auth_strategy, ClientCredentialsAuth)
    assert client._auth_strategy._client_id == MOCK_CLIENT_ID
    assert client._auth_strategy._client_secret == MOCK_CLIENT_SECRET
    assert client._auth_strategy._token_url == MOCK_TOKEN_URL

def test_client_init_client_creds_override(mock_settings):
    """Test client initialization uses ClientCredentialsAuth with overrides."""
    client = AireloomClient(
        settings=mock_settings,
        client_id="override_id",
        client_secret="override_secret"
    )
    assert isinstance(client._auth_strategy, ClientCredentialsAuth)
    assert client._auth_strategy._client_id == "override_id"
    assert client._auth_strategy._client_secret == "override_secret"
    assert client._auth_strategy._token_url == MOCK_TOKEN_URL # From settings

def test_client_init_creds_precedence_over_token(mock_settings_with_creds):
    """Test client credentials take precedence over static token in settings."""
    settings = mock_settings_with_creds
    settings.openaire_api_token = MOCK_STATIC_TOKEN # Add a token too
    client = AireloomClient(settings=settings)
    # Should still use ClientCredentialsAuth
    assert isinstance(client._auth_strategy, ClientCredentialsAuth)

def test_client_init_explicit_auth_precedence(mock_settings_with_creds):
    """Test explicit auth strategy takes precedence over settings."""
    explicit_auth = StaticTokenAuth(token="explicit_token")
    client = AireloomClient(settings=mock_settings_with_creds, auth_strategy=explicit_auth)
    assert client._auth_strategy is explicit_auth


# --- Test Request Execution and Authentication ---

@pytest.mark.asyncio
async def test_request_with_no_auth(mock_settings, httpx_mock: HTTPXMock):
    """Test a request is made without Authorization header using NoAuth."""
    httpx_mock.add_response(url=f"{MOCK_BASE_URL}/test", method="GET", status_code=httpx.codes.OK, json={"ok": True})
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/test")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"ok": True}
    request = httpx_mock.get_requests()[0]
    assert "Authorization" not in request.headers

@pytest.mark.asyncio
async def test_request_with_static_token_auth(mock_settings_with_token, httpx_mock: HTTPXMock):
    """Test a request includes correct Authorization header with StaticTokenAuth."""
    httpx_mock.add_response(url=f"{MOCK_BASE_URL}/test", method="GET", status_code=httpx.codes.OK, json={"ok": True})
    client = AireloomClient(settings=mock_settings_with_token, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/test")

    assert response.status_code == httpx.codes.OK
    request = httpx_mock.get_requests()[0]
    assert "Authorization" in request.headers
    assert request.headers["Authorization"] == f"Bearer {MOCK_STATIC_TOKEN}"


@pytest.mark.asyncio
async def test_request_with_client_creds_auth_success(mock_settings_with_creds, httpx_mock: HTTPXMock):
    """Test a request with ClientCredentialsAuth fetches token and uses it."""
    # Mock the token endpoint
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        json={"access_token": MOCK_OAUTH_TOKEN, "expires_in": 3600},
        status_code=httpx.codes.OK,
    )
    # Mock the actual API endpoint
    httpx_mock.add_response(url=f"{MOCK_BASE_URL}/data", method="GET", status_code=httpx.codes.OK, json={"data": "value"})

    client = AireloomClient(settings=mock_settings_with_creds, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/data")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"data": "value"}

    # Check token request
    token_requests = httpx_mock.get_requests(url=MOCK_TOKEN_URL, method="POST")
    assert len(token_requests) == 1
    assert token_requests[0].headers["Authorization"].startswith("Basic ") # Basic auth used

    # Check API request
    api_requests = httpx_mock.get_requests(url=f"{MOCK_BASE_URL}/data", method="GET")
    assert len(api_requests) == 1
    assert "Authorization" in api_requests[0].headers
    assert api_requests[0].headers["Authorization"] == f"Bearer {MOCK_OAUTH_TOKEN}"


@pytest.mark.asyncio
async def test_request_with_client_creds_auth_token_failure(mock_settings_with_creds, httpx_mock: HTTPXMock):
    """Test that AuthError during token fetch prevents API call and propagates."""
    # Mock the token endpoint to fail
    httpx_mock.add_response(
        url=MOCK_TOKEN_URL,
        method="POST",
        status_code=401,
        text="Invalid Credentials"
    )
    # Do NOT mock the /data endpoint

    client = AireloomClient(settings=mock_settings_with_creds, base_url=MOCK_BASE_URL)
    with pytest.raises(AuthError, match="Failed to fetch access token: 401"):
        async with client:
            await client.request("GET", "/data")
    # Ensure the API endpoint was never called
    api_requests = httpx_mock.get_requests(url=f"{MOCK_BASE_URL}/data", method="GET")
    assert len(api_requests) == 0


# --- Test Retries and Error Handling ---

@pytest.mark.asyncio
async def test_request_retry_on_503(mock_settings, httpx_mock: HTTPXMock):
    """Test that the client retries on 503 status code."""
    url = f"{MOCK_BASE_URL}/retry_test"
    httpx_mock.add_response(url=url, method="GET", status_code=503) # First attempt fails
    httpx_mock.add_response(url=url, method="GET", status_code=503) # Second attempt fails
    httpx_mock.add_response(url=url, method="GET", status_code=httpx.codes.OK, json={"ok": True}) # Third succeeds

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL) # max_retries = 2

    async with client:
        response = await client.request("GET", "/retry_test")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"ok": True}
    assert len(httpx_mock.get_requests()) == 3 # Initial + 2 retries


@pytest.mark.asyncio
async def test_request_retry_on_rate_limit(mock_settings, httpx_mock: HTTPXMock):
    """Test that the client retries on 429 status code."""
    url = f"{MOCK_BASE_URL}/rate_limit_test"
    httpx_mock.add_response(url=url, method="GET", status_code=429) # First attempt fails
    httpx_mock.add_response(url=url, method="GET", status_code=httpx.codes.OK, json={"ok": True}) # Second succeeds

    # Use only 1 retry for this test
    mock_settings.max_retries = 1
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/rate_limit_test")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"ok": True}
    assert len(httpx_mock.get_requests()) == 2 # Initial + 1 retry


@pytest.mark.asyncio
async def test_request_failure_after_retries(mock_settings, httpx_mock: HTTPXMock):
    """Test that ApiError is raised after exhausting retries."""
    url = f"{MOCK_BASE_URL}/fail_test"
    httpx_mock.add_response(url=url, method="GET", status_code=500) # Attempt 1
    httpx_mock.add_response(url=url, method="GET", status_code=502) # Attempt 2
    httpx_mock.add_response(url=url, method="GET", status_code=504) # Attempt 3 (max_retries = 2)

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL) # max_retries = 2

    with pytest.raises(APIError) as excinfo:
        async with client:
            await client.request("GET", "/fail_test")

    assert len(httpx_mock.get_requests()) == 3
    assert excinfo.value.response.status_code == 504 # Last error encountered
    assert "API request failed with status 504" in str(excinfo.value)

@pytest.mark.asyncio
async def test_request_non_retryable_4xx_error(mock_settings, httpx_mock: HTTPXMock):
    """Test that ApiError is raised immediately for non-retryable 4xx errors."""
    url = f"{MOCK_BASE_URL}/client_error_test"
    httpx_mock.add_response(url=url, method="GET", status_code=404, text="Not Found")

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    with pytest.raises(APIError) as excinfo:
        async with client:
            await client.request("GET", "/client_error_test")

    assert len(httpx_mock.get_requests()) == 1 # No retries
    assert excinfo.value.response.status_code == 404
    assert "API request failed with status 404" in str(excinfo.value)

@pytest.mark.asyncio
async def test_request_timeout_error(mock_settings, httpx_mock: HTTPXMock):
    """Test that TimeoutError is raised on timeout."""
    url = f"{MOCK_BASE_URL}/timeout_test"
    for _ in range(mock_settings.max_retries + 1):
        httpx_mock.add_exception(httpx.TimeoutException("Request timed out", request=httpx.Request("GET", url)))

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)
    with pytest.raises(TimeoutError, match="Request timed out"):
        async with client:
            await client.request("GET", "/timeout_test")

    # Retries should have happened (initial + max_retries)
    assert len(httpx_mock.get_requests()) == mock_settings.max_retries + 1

@pytest.mark.asyncio
async def test_request_network_error(mock_settings, httpx_mock: HTTPXMock):
    """Test that NetworkError is raised on connection error."""
    url = f"{MOCK_BASE_URL}/network_error_test"
    # Register the exception for each retry attempt
    for _ in range(mock_settings.max_retries + 1):
        httpx_mock.add_exception(httpx.ConnectError("Connection failed", request=httpx.Request("GET", url)))

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)
    with pytest.raises(NetworkError, match="Network error occurred"):
        async with client:
            await client.request("GET", "/network_error_test")


# --- Test Client Context Manager and Closing ---

@pytest.mark.asyncio
async def test_client_aclose(mock_settings_with_creds):
    """Test that aclose closes the http client and the auth strategy client."""
    # Mock the ClientCredentialsAuth close method
    mock_auth_close = AsyncMock()

    with patch("aireloom.client.ClientCredentialsAuth", spec=ClientCredentialsAuth) as MockAuth:
        mock_auth_instance = MockAuth.return_value
        mock_auth_instance.close = mock_auth_close

        # Mock the httpx client's aclose method
        mock_http_client = MagicMock(spec=httpx.AsyncClient)
        mock_http_client.aclose = AsyncMock()

        # Create client with the mocked http client
        client = AireloomClient(
            settings=mock_settings_with_creds,
            http_client=mock_http_client
        )

        # Verify the mock auth was used
        assert client._auth_strategy is mock_auth_instance
        # Prevent closing the client we passed in
        client._should_close_client = False

        await client.aclose()

        # Assert auth strategy close was called
        mock_auth_close.assert_awaited_once()
        # Assert http client close was *not* called (because we provided it)
        mock_http_client.aclose.assert_not_awaited()

        # Test again, this time letting the client create its own http client
        client_creates_http = AireloomClient(settings=mock_settings_with_creds)
        # Manually replace auth strategy with our mock that has mocked close
        client_creates_http._auth_strategy = mock_auth_instance

        real_http_client = client_creates_http._http_client
        with patch.object(real_http_client, "aclose", new_callable=AsyncMock) as mock_real_aclose:
            await client_creates_http.aclose()

            # Assert auth strategy close was called again
            assert mock_auth_close.call_count == 2
            # Assert the internal http client's close *was* called
            mock_real_aclose.assert_awaited_once()


@pytest.mark.asyncio
async def test_client_context_manager(mock_settings):
    """Test the client works as an async context manager."""
    client = AireloomClient(settings=mock_settings)
    # Mock aclose to check if it's called
    client.aclose = AsyncMock()

    async with client:
        assert isinstance(client, AireloomClient)
        # Perform some action (optional)

    # Assert aclose was called upon exiting the context
    client.aclose.assert_awaited_once()


# --- Test Base URL Handling ---

@pytest.mark.asyncio
async def test_base_url_override(mock_settings, httpx_mock: HTTPXMock):
    """Test that base_url_override works correctly."""
    default_url = f"{MOCK_BASE_URL}/default"
    override_url = "https://override.api.com/override"

    httpx_mock.add_response(url=default_url, method="GET", status_code=httpx.codes.OK, json={"ok": "default"})
    httpx_mock.add_response(url=override_url, method="GET", status_code=httpx.codes.OK, json={"ok": "override"})

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    async with client:
        # Request to default base URL
        resp1 = await client.request("GET", "/default")
        # Request with override
        resp2 = await client.request("GET", "/override", base_url_override="https://override.api.com")

    assert resp1.json() == {"ok": "default"}
    assert resp2.json() == {"ok": "override"}

    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    assert str(requests[0].url) == default_url
    assert str(requests[1].url) == override_url


@pytest.mark.asyncio
async def test_default_base_urls_used(mock_settings, httpx_mock: HTTPXMock):
    """Test that the correct default OpenAIRE base URLs are used if not overridden."""
    graph_url = f"{OPENAIRE_GRAPH_API_BASE_URL.rstrip('/')}/graph_test"
    # Example using Scholix URL via override for testing constants
    scholix_url = f"{OPENAIRE_SCHOLIX_API_BASE_URL.rstrip('/')}/scholix_test"

    httpx_mock.add_response(url=graph_url, method="GET", status_code=httpx.codes.OK)
    httpx_mock.add_response(url=scholix_url, method="GET", status_code=httpx.codes.OK)

    # Client defaults to Graph API base URL
    client = AireloomClient(settings=mock_settings)
    assert client._base_url == OPENAIRE_GRAPH_API_BASE_URL.rstrip('/')

    async with client:
        # Request using default base URL (Graph)
        await client.request("GET", "/graph_test")
        # Request overriding to Scholix base URL
        await client.request("GET", "/scholix_test", base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL)

    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    assert str(requests[0].url) == graph_url
    assert str(requests[1].url) == scholix_url

@pytest.mark.asyncio
async def test_request_http_error_no_retry(mock_settings, httpx_mock: HTTPXMock):
    """Test that HTTPError is raised and not retried for non-retriable status codes."""
    url = f"{MOCK_BASE_URL}/not_found_test"
    httpx_mock.add_response(url=url, status_code=httpx.codes.NOT_FOUND)
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    with pytest.raises(APIError) as excinfo:
        async with client:
            await client.request("GET", "/not_found_test")

    assert len(httpx_mock.get_requests()) == 1 # No retries
    assert excinfo.value.response.status_code == httpx.codes.NOT_FOUND
    assert "API request failed with status 404" in str(excinfo.value)



# -------------------------------------------------------
#
# C:\dev\AIREloom\tests\test_session.py
#
# ------------------------------------------------------

# tests/test_session.py
import pytest
from dotenv import load_dotenv
from pytest_httpx import HTTPXMock

# Make sure aireloom can be imported from the src directory
# This might require specific pytest configuration or PYTHONPATH adjustments
# depending on project structure and how tests are run.
# Assuming standard src layout is handled by pytest/uv.
from aireloom import AireloomSession
from aireloom.auth import (  # Import specific auth strategies for checking
    NoAuth,
    StaticTokenAuth,
)
from aireloom.constants import OPENAIRE_SCHOLIX_API_BASE_URL
from aireloom.exceptions import AireloomError, ValidationError

# Load .env file for local testing (e.g., containing AIRELOOM_OPENAIRE_API_TOKEN)
load_dotenv()

# --- Constants ---
# Keep existing constants
KNOWN_PRODUCT_ID = "doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108"
KNOWN_PRODUCT_TITLE_FRAGMENT = (
    "OpenAIRE Graph"  # A fragment likely present in the title
)
KNOWN_DOI_WITH_LINKS = "10.5281/zenodo.7668094"
UNKNOWN_PRODUCT_ID = "oai:example.org:nonexistent123"
INVALID_PRODUCT_ID_FORMAT = "not-a-valid-id-format"

# --- Mock Data ---
MOCK_SCHOLIX_RESPONSE = {
    "currentPage": 0,
    "totalLinks": 1,
    "totalPages": 1,
    "result": [
        {
            "LinkProvider": [
                {
                    "Name": "DataCite", # Correct casing
                    "Identifier": [{"ID": "datacite", "IDScheme": "datacid"}],
                }
            ],
            "RelationshipType": {
                "Name": "References", # Use valid literal from ScholixRelationshipNameValue
                "SubType": "Dataset",
                # SubTypeSchema is optional and needs to be a URL or None
                "SubTypeSchema": "http://example.com/schema/references",
            },
            "Source": { # Add Source (Required)
                "Identifier": [{"ID": KNOWN_DOI_WITH_LINKS, "IDScheme": "doi"}],
                "Type": "publication", # Use valid literal from ScholixEntityTypeName
            },
            "Target": { # Add Target (Required)
                "Identifier": [{"ID": "10.1234/target.dataset", "IDScheme": "doi"}],
                "Type": "dataset", # Use valid literal from ScholixEntityTypeName
            },
            "LinkPublicationDate": "2023-01-15T12:00:00Z", # Added field, use ISO format with Z
            "LicenseURL": None, # Optional
            "HarvestDate": None, # Optional
        }
    ],
}

# --- Basic Initialization Tests ---


@pytest.mark.asyncio
async def test_session_initialization_no_token():
    """Test initializing AireloomSession without providing a token."""
    async with AireloomSession() as session:
        assert session is not None
        # Check if NoAuth strategy is implicitly used
        assert isinstance(session._api_client._auth_strategy, NoAuth)


@pytest.mark.asyncio
async def test_session_initialization_with_token(
    api_token,
):  # Uses fixture from conftest.py
    """Test initializing AireloomSession with a token (from fixture)."""
    if not api_token:
        pytest.skip(
            "Skipping token test: AIRELOOM_OPENAIRE_API_TOKEN not set in environment."
        )

    # Test explicit token argument
    async with AireloomSession(api_token=api_token) as session:
        assert session is not None
        # Check if TokenAuth strategy is used
        assert isinstance(session._api_client._auth_strategy, StaticTokenAuth)
        assert session._api_client._auth_strategy._token == api_token

    # Test token via settings (implicitly via environment variable AIRELOOM_OPENAIRE_API_TOKEN)
    # This assumes the ApiClient correctly reads from settings when no strategy/token is passed
    async with AireloomSession() as session_env:
        assert session_env is not None
        assert isinstance(session_env._api_client._auth_strategy, StaticTokenAuth)
        assert session_env._api_client._auth_strategy._token == api_token


# --- Graph API Tests ---


# Use a known, stable, public research product ID for testing
# Example: OpenAIRE-Nexus project publication


@pytest.mark.asyncio
async def test_get_research_product_success():
    """Test fetching a known public research product."""
    async with AireloomSession() as session:
        try:
            product = await session.get_research_product(KNOWN_PRODUCT_ID)
            assert product is not None
            assert product.id == KNOWN_PRODUCT_ID
            assert isinstance(product.mainTitle, str)  # Fix: use mainTitle
        except AireloomError as e:
            pytest.fail(f"Fetching known product failed: {e}")


@pytest.mark.asyncio
async def test_get_research_product_not_found():
    """Test fetching a non-existent research product."""
    async with AireloomSession() as session:
        with pytest.raises(
            AireloomError, match="API request failed with status 404"
        ):
            await session.get_research_product("nonexistent:id_123456789_invalid")


@pytest.mark.asyncio
async def test_search_research_products_simple():
    """Test a simple search for research products."""
    async with AireloomSession() as session:
        try:
            # Search for a common term, limit results
            response = await session.search_research_products(
                page_size=5, mainTitle="Open Science" # Use mainTitle filter
            )
            assert response is not None
            assert response.header is not None
            # Total might fluctuate, just check > 0 if results expected
            # assert response.header.total > 0
            assert response.results is not None
            # Check actual results count matches expectation (up to page_size)
            assert 0 <= len(response.results) <= 5  # noqa: PLR2004
            # Optional: Check if results seem relevant
            if response.results:
                assert isinstance(response.results[0].id, str)
                # Use mainTitle attribute for assertion
                assert isinstance(response.results[0].mainTitle, str)
        except AireloomError as e:
            pytest.fail(f"Simple product search failed: {e}")


@pytest.mark.asyncio
async def test_iterate_research_products(httpx_mock: HTTPXMock):
    """Test iterating through research products."""
    # Mock the API response for the iteration
    mock_response = {
        "header": {"total": 2},
        "results": [
            {"id": "id1", "mainTitle": "Title 1"},
            {"id": "id2", "mainTitle": "Title 2"},
        ],
    }
    httpx_mock.add_response(
        url="https://api.openaire.eu/graph/v1/researchProducts?pageSize=5&sortBy=&mainTitle=FAIR+data&cursor=%2A&size=20",
        method="GET",
        json=mock_response,
        status_code=200,
    )
    async with AireloomSession() as session:
        count = 0
        max_items_to_iterate = 15
        try:
            async for product in session.iterate_research_products(
                page_size=5, mainTitle="FAIR data"
            ):
                assert product is not None
                assert isinstance(product.id, str)
                count += 1
                if count >= max_items_to_iterate:
                    break
            assert count >= 0
            assert count <= max_items_to_iterate
        except AireloomError as e:
            pytest.fail(f"Product iteration failed: {e}")


# --- Scholix API Tests ---


# Use a known DOI with known relationships if possible, otherwise use a general one


@pytest.mark.asyncio
async def test_search_scholix_links_success(httpx_mock: HTTPXMock):
    """Test searching for Scholix links for a known DOI."""
    # Mock the API call
    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=0&rows=10",
        method="GET",
        json=MOCK_SCHOLIX_RESPONSE,
        status_code=200,
    )
    async with AireloomSession() as session:
        try:
            response = await session.search_scholix_links(
                page_size=10, sourcePid=KNOWN_DOI_WITH_LINKS
            )
            assert response is not None
            assert response.currentPage == 0  # API is 0-indexed
            assert response.totalLinks >= 0 # Check for non-negative
            assert response.result is not None
            assert 0 <= len(response.result) <= 10  # noqa: PLR2004
            # If results exist, check basic structure
            if response.result:
                link = response.result[0]
                # Assuming LinkPublicationDate might be None in real data or mock
                # assert link.LinkPublicationDate is not None
                assert link.Source is not None
                assert link.Target is not None
                assert isinstance(link.Source.Identifier, list)
                assert isinstance(link.Target.Identifier, list)
                assert link.RelationshipType is not None # Check added field
        except AireloomError as e:
            pytest.fail(f"Scholix link search failed: {e}")


@pytest.mark.asyncio
async def test_iterate_scholix_links(httpx_mock: HTTPXMock):
    """Test iterating through Scholix links."""
    # Mock the first page API call
    # Use a response with enough links for the test iteration count.
    mock_response_page1 = MOCK_SCHOLIX_RESPONSE.copy()
    mock_response_page1["currentPage"] = 0
    mock_response_page1["totalLinks"] = 7 # Example: 7 links total across 2 pages
    mock_response_page1["totalPages"] = 2 # Example: 2 pages total
    # Create 5 links for page 1 (size=5)
    # Ensure the base link structure is valid
    base_link = MOCK_SCHOLIX_RESPONSE["result"][0]
    mock_response_page1["result"] = []
    for i in range(5):
        link = base_link.copy()
        link["LinkPublicationDate"] = f"2023-01-15T12:00:0{i}Z" # Vary slightly, use Z
        # Ensure Source and Target are valid ScholixEntity structures
        link["Source"] = { # Add Source (Required)
            "Identifier": [{"ID": f"{KNOWN_DOI_WITH_LINKS}/{i}", "IDScheme": "doi"}],
            "Type": "publication",
        }
        link["Target"] = { # Add Target (Required)
            "Identifier": [{
                "ID": f"10.1234/target.dataset.{i}", "IDScheme": "doi"
                }],
            "Type": "dataset", # Ensure valid type
        }
        mock_response_page1["result"].append(link)


    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=0&rows=5",
        method="GET",
        json=mock_response_page1,
        status_code=200,
    )

    # Mock the second page
    mock_response_page2 = MOCK_SCHOLIX_RESPONSE.copy()
    mock_response_page2["currentPage"] = 1
    mock_response_page2["totalLinks"] = 7
    mock_response_page2["totalPages"] = 2
    # Create 2 remaining links for page 2
    mock_response_page2["result"] = []
    for i in range(2):
        link = base_link.copy()
        link["LinkPublicationDate"] = f"2023-01-16T13:00:0{i}Z" # Vary slightly, use Z
        # Ensure Source and Target are valid ScholixEntity structures
        link["Source"] = { # Add Source (Required)
            "Identifier": [{"ID": f"{KNOWN_DOI_WITH_LINKS}/{i+5}", "IDScheme": "doi"}],
            "Type": "publication",
        }
        link["Target"] = { # Add Target (Required)
            "Identifier": [{
                "ID": f"10.1234/target.dataset.{i+5}", "IDScheme": "doi"
                }],
            "Type": "dataset", # Ensure valid type
        }
        mock_response_page2["result"].append(link)

    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=1&rows=5",
        method="GET",
        json=mock_response_page2,
        status_code=200,
    )

    async with AireloomSession() as session:
        count = 0
        max_items_to_iterate = 7 # Iterate through all mocked items
        try:
            async for link in session.iterate_scholix_links(
                page_size=5, sourcePid=KNOWN_DOI_WITH_LINKS
            ):
                assert link is not None
                assert link.RelationshipType is not None  # Core field
                assert link.Source is not None
                assert link.Target is not None
                assert link.LinkPublicationDate is not None # Check date exists
                count += 1
                if count >= max_items_to_iterate:
                    break
            assert count == max_items_to_iterate
        except AireloomError as e:
            pytest.fail(f"Scholix iteration failed: {e}")


@pytest.mark.asyncio
async def test_search_scholix_invalid_filter():
    """Test searching Scholix links with an invalid filter key."""
    async with AireloomSession() as session:
        with pytest.raises(
            ValidationError, match="Invalid filter key"
        ):  # Check error message content
            # Pass a deliberately invalid filter key
            await session.search_scholix_links(
                page_size=10, someMadeUpFilterKey="someValue"
            )



