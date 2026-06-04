from unittest.mock import AsyncMock

import httpx
import pytest

from aireloom.client import AireloomClient
from aireloom.config import ApiSettings
from aireloom.unwrapper import OpenAireUnwrapper


@pytest.fixture
def mock_settings_with_creds():
    return ApiSettings(
        openaire_client_id="test_id",
        openaire_client_secret="test_secret",
        openaire_token_url="https://test.token.url",
    )


@pytest.fixture
def mock_api_client_fixture():
    """Fixture to create a mock AireloomClient."""
    mock_client = AsyncMock(spec=AireloomClient)
    mock_client._response_unwrapper = OpenAireUnwrapper()
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = {
        "header": {
            "numFound": 0,
            "pageSize": 10,
            "pageNumber": 1,
            "totalPages": 0,
            "nextCursor": None,
        },
        "results": [],
    }
    mock_client.request.return_value = mock_http_response
    return mock_client


@pytest.mark.asyncio
async def test_context_manager_enter_exit():
    """Test __aenter__ and __aexit__ cover the logging branches."""
    async with AireloomClient() as client:
        assert client is not None
        assert not client._http_client.is_closed
    # After exit, client should be closed
    assert client._http_client.is_closed


def test_no_auth_fallback():
    """When no credentials are provided at all, NoAuth is used (lines 165-166)."""
    # Use empty settings with no credentials
    settings = ApiSettings(
        openaire_client_id=None,
        openaire_client_secret=None,
        openaire_api_token=None,
    )
    client = AireloomClient(settings=settings)
    # Client should be created without error (NoAuth path)
    assert client is not None


def test_client_credentials_from_params():
    """Client credentials passed directly as parameters."""
    settings = ApiSettings(
        openaire_client_id=None,
        openaire_client_secret=None,
    )
    client = AireloomClient(
        settings=settings,
        client_id="param_id",
        client_secret="param_secret",
    )
    assert client is not None


def test_static_token_from_param():
    """Static token passed as parameter."""
    settings = ApiSettings(
        openaire_api_token=None,
        openaire_client_id=None,
        openaire_client_secret=None,
    )
    client = AireloomClient(settings=settings, api_token="my-test-token")
    assert client is not None
