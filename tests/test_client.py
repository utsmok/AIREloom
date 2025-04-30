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
    url = f"{MOCK_BASE_URL}/test"
    httpx_mock.add_response(url=url, method="GET", status_code=httpx.codes.OK, json={"ok": True})
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/test")

    assert response.status_code == httpx.codes.OK
    assert response.json() == {"ok": True}
    requests = httpx_mock.get_requests(url=url)
    assert len(requests) == 1
    assert "Authorization" not in requests[0].headers
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT

@pytest.mark.asyncio
async def test_request_with_static_token_auth(mock_settings_with_token, httpx_mock: HTTPXMock):
    """Test a request includes correct Authorization header with StaticTokenAuth."""
    url = f"{MOCK_BASE_URL}/test"
    httpx_mock.add_response(url=url, method="GET", status_code=httpx.codes.OK, json={"ok": True})
    client = AireloomClient(settings=mock_settings_with_token, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("GET", "/test")

    assert response.status_code == httpx.codes.OK
    requests = httpx_mock.get_requests(url=url)
    assert len(requests) == 1
    assert requests[0].headers["Authorization"] == f"Bearer {MOCK_STATIC_TOKEN}"
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT


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
    api_url = f"{MOCK_BASE_URL}/data"
    httpx_mock.add_response(url=api_url, method="GET", status_code=httpx.codes.OK, json={"data": "value"})

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
    api_requests = httpx_mock.get_requests(url=api_url, method="GET")
    assert len(api_requests) == 1
    assert api_requests[0].headers["Authorization"] == f"Bearer {MOCK_OAUTH_TOKEN}"
    assert api_requests[0].headers["User-Agent"] == MOCK_USER_AGENT

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
    requests = httpx_mock.get_requests(url=url)
    assert len(requests) == 3 # Initial + 2 retries
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[1].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[2].headers["User-Agent"] == MOCK_USER_AGENT


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
    requests = httpx_mock.get_requests(url=url)
    assert len(requests) == 2 # Initial + 1 retry
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[1].headers["User-Agent"] == MOCK_USER_AGENT


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

    assert len(httpx_mock.get_requests(url=url)) == 3
    assert excinfo.value.response.status_code == 504 # Last error encountered
    assert "API request failed with status 504" in str(excinfo.value)
    requests = httpx_mock.get_requests(url=url)
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[1].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[2].headers["User-Agent"] == MOCK_USER_AGENT


@pytest.mark.asyncio
async def test_request_non_retryable_4xx_error(mock_settings, httpx_mock: HTTPXMock):
    """Test that ApiError is raised immediately for non-retryable 4xx errors."""
    url = f"{MOCK_BASE_URL}/client_error_test"
    httpx_mock.add_response(url=url, method="GET", status_code=404, text="Not Found")

    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    with pytest.raises(APIError) as excinfo:
        async with client:
            await client.request("GET", "/client_error_test")

    assert len(httpx_mock.get_requests(url=url)) == 1 # No retries
    assert excinfo.value.response.status_code == 404
    assert "API request failed with status 404" in str(excinfo.value)
    requests = httpx_mock.get_requests(url=url)
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT


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
    requests = httpx_mock.get_requests(url=url)
    assert len(requests) >= 1
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT


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

    requests = httpx_mock.get_requests(url=url)
    assert len(requests) == mock_settings.max_retries + 1 # Should retry on connect error
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT


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
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[1].headers["User-Agent"] == MOCK_USER_AGENT


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
    assert requests[0].headers["User-Agent"] == MOCK_USER_AGENT
    assert requests[1].headers["User-Agent"] == MOCK_USER_AGENT


# --- Test Request Parameters and Methods ---

@pytest.mark.asyncio
async def test_request_post_with_json(mock_settings, httpx_mock: HTTPXMock):
    """Test POST request with JSON body."""
    url = f"{MOCK_BASE_URL}/post_test"
    payload = {"key": "value", "num": 1}
    httpx_mock.add_response(url=url, method="POST", status_code=201, json={"created": True})
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)

    async with client:
        response = await client.request("POST", "/post_test", json=payload)

    assert response.status_code == 201
    assert response.json() == {"created": True}
    requests = httpx_mock.get_requests(url=url, method="POST")
    assert len(requests) == 1
    request = requests[0]
    assert request.read().decode() == '{"key": "value", "num": 1}' # Check JSON payload
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["User-Agent"] == MOCK_USER_AGENT


@pytest.mark.asyncio
async def test_request_get_with_params(mock_settings, httpx_mock: HTTPXMock):
    """Test GET request with query parameters."""
    # httpx encodes parameters, so the matched URL should reflect that
    expected_url_encoded = f"{MOCK_BASE_URL}/get_test?param1=value1&param2=123"
    httpx_mock.add_response(url=expected_url_encoded, method="GET", status_code=200, json={"ok": True})
    client = AireloomClient(settings=mock_settings, base_url=MOCK_BASE_URL)
    params = {"param1": "value1", "param2": 123} # Mix of str and int

    async with client:
        response = await client.request("GET", "/get_test", params=params)

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    # Verify the request URL was correctly encoded by httpx
    requests = httpx_mock.get_requests(url=expected_url_encoded, method="GET")
    assert len(requests) == 1
    request = requests[0]
    assert request.headers["User-Agent"] == MOCK_USER_AGENT
