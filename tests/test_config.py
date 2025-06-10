import pytest

from aireloom import AireloomSession
from aireloom.config import ApiSettings, AuthStrategyType


@pytest.mark.asyncio
async def test_session_programmatic_config_override(httpx_mock, monkeypatch):
    # Mock an API call that would depend on a setting
    httpx_mock.add_response(
        url="https://api.openaire.eu/graph/v1/researchProducts/progcfg123",
        method="GET",
        json={"id": "progcfg123", "title": "Prog Config Test"},
    )

    # Ensure env vars are not set for these, or set to different values
    monkeypatch.delenv("AIRELOOM_API_TOKEN", raising=False)
    monkeypatch.delenv("AIRELOOM_AUTH_STRATEGY", raising=False)
    monkeypatch.setenv(
        "AIRELOOM_REQUEST_TIMEOUT", "10"
    )  # A default that will be overridden

    custom_settings = ApiSettings(
        auth_strategy=AuthStrategyType.STATIC_TOKEN,
        api_token="override_token_12345",
        request_timeout=45.0,  # Override the env var
    )

    async with AireloomSession(settings=custom_settings) as session:
        # Verify the client inside the session uses the overridden settings
        assert session._api_client.settings.api_token == "override_token_12345"
        assert (
            session._api_client.settings.auth_strategy == AuthStrategyType.STATIC_TOKEN
        )
        assert session._api_client.settings.request_timeout == 45.0

        # Make a call to ensure it works with these settings
        # The httpx_mock will need to be set up to expect the 'override_token_12345'
        # if auth was tested here. For this test, we are primarily checking if the settings
        # are passed through correctly. The actual auth mechanism is tested elsewhere.
        await session.research_products.get("progcfg123")

    # Test that default init still works and picks up env vars if set
    monkeypatch.setenv("AIRELOOM_API_TOKEN", "env_token_67890")
    monkeypatch.setenv("AIRELOOM_AUTH_STRATEGY", "STATIC_TOKEN")
    # AIRELOOM_REQUEST_TIMEOUT is still "10" from the earlier monkeypatch.setenv

    async with AireloomSession() as session_env:
        assert session_env._api_client.settings.api_token == "env_token_67890"
        assert (
            session_env._api_client.settings.auth_strategy
            == AuthStrategyType.STATIC_TOKEN
        )
        assert (
            session_env._api_client.settings.request_timeout == 10.0
        )  # From env var set earlier
