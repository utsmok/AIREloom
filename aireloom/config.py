# aireloom/config.py
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Assuming constants.py defines OPENAIRE_TOKEN_URL
from .constants import DEFAULT_USER_AGENT, REGISTERED_SERVICE_API_TOKEN_URL
from .types import PostRequestHook, PreRequestHook  # Add this


class ApiSettings(BaseSettings):
    """
    Manages user-configurable settings for the AIREloom client,
    primarily loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "secrets.env"),  # Look in both .env and secrets.env
        env_file_encoding="utf-8",
        # Environment variables should be prefixed, e.g., AIRELOOM_OPENAIRE_API_TOKEN
        env_prefix="AIRELOOM_",
        extra="ignore",  # Ignore extra fields found in environment
        case_sensitive=False,  # Allow AIRELOOM_openaire_api_token etc.
        arbitrary_types_allowed=True,  # Add this
    )

    # --- Client Behavior Settings ---
    request_timeout: float = Field(
        default=30.0, description="Default request timeout in seconds"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for failed requests"
    )
    backoff_factor: float = Field(
        default=0.5, description="Backoff factor for retries (seconds)"
    )
    user_agent: str = Field(
        default=DEFAULT_USER_AGENT,  # Get default from constants
        description="User-Agent header for requests",
    )

    # --- Rate Limiting Settings ---
    enable_rate_limiting: bool = Field(
        default=True, description="Enable/disable API rate limiting features"
    )
    rate_limit_buffer_percentage: float = Field(
        default=0.1,
        description="Buffer percentage to consider rate limit approaching (e.g., 0.1 for 10%)",
    )
    rate_limit_retry_after_default: int = Field(
        default=60,
        description="Default wait time in seconds if Retry-After header is not present on 429",
    )

    # --- Caching Settings ---
    enable_caching: bool = Field(
        default=False, description="Enable/disable client-side caching"
    )
    cache_ttl_seconds: int = Field(
        default=300,
        description="Default TTL for cache entries in seconds (e.g., 300 for 5 minutes)",
    )
    cache_max_size: int = Field(
        default=128, description="Maximum number of items in the LRU cache"
    )

    # --- Hook Settings ---
    pre_request_hooks: list[PreRequestHook] = Field(
        default_factory=list,
        description="List of hooks to call before a request is made.",
    )
    post_request_hooks: list[PostRequestHook] = Field(
        default_factory=list,
        description="List of hooks to call after a response is received and parsed.",
    )

    # --- Authentication Settings ---
    # Option 1: Static API Token
    openaire_api_token: str | None = Field(
        default=None, description="Static OpenAIRE API Token (optional)"
    )

    # Option 2: Client Credentials for OAuth2 Token Fetching
    openaire_client_id: str | None = Field(
        default=None,
        description="OpenAIRE Client ID for OAuth2 (required for client_credentials)",
    )
    openaire_client_secret: str | None = Field(
        default=None,
        description="OpenAIRE Client Secret for OAuth2 (required for client_credentials)",
    )
    # Token URL is fetched from constants, but could be overridden via env if needed
    openaire_token_url: str = Field(
        default=REGISTERED_SERVICE_API_TOKEN_URL,
        description="OAuth2 Token Endpoint URL",
    )


# Create a single, cached instance of settings
@lru_cache
def get_settings() -> ApiSettings:
    """
    Provides access to the application settings.

    Settings are loaded from environment variables (prefixed with 'AIRELOOM_')
    or .env/secrets.env files. The instance is cached for performance.

    Returns:
        ApiSettings: The application settings instance.
    """
    # Check if running in a test environment and potentially load test-specific env
    # For now, relies on standard .env/.secrets.env loading
    return ApiSettings()
