# Configuration

AIREloom uses `ApiSettings` (powered by Pydantic BaseSettings) to load configuration from environment variables, `.env` files, or direct arguments.

## Precedence

Settings are resolved in this order (highest first):

1. **Direct arguments** — values passed to the `ApiSettings` constructor.
2. **Environment variables** — prefixed with `AIRELOOM_`.
3. **`.env` / `secrets.env`** — files in the project root.
4. **Defaults** — hardcoded in `ApiSettings`.

## Client Behavior

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `request_timeout` | `AIRELOOM_REQUEST_TIMEOUT` | `30.0` | Request timeout in seconds |
| `max_retries` | `AIRELOOM_MAX_RETRIES` | `3` | Max retries for transient errors |
| `backoff_factor` | `AIRELOOM_BACKOFF_FACTOR` | `0.5` | Backoff multiplier: `factor × 2^(attempt-1)` |
| `user_agent` | `AIRELOOM_USER_AGENT` | `aireloom/{version}` | User-Agent header |

## Authentication

See the [Authentication Guide](../authentication.md) for details.

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `openaire_api_token` | `AIRELOOM_OPENAIRE_API_TOKEN` | `None` | Static API token |
| `openaire_client_id` | `AIRELOOM_OPENAIRE_CLIENT_ID` | `None` | OAuth2 client ID |
| `openaire_client_secret` | `AIRELOOM_OPENAIRE_CLIENT_SECRET` | `None` | OAuth2 client secret |
| `openaire_token_url` | `AIRELOOM_OPENAIRE_TOKEN_URL` | `https://aai.openaire.eu/oidc/token` | OAuth2 token endpoint |

## Rate Limiting

See [Rate Limiting](rate_limiting.md) for details.

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `enable_rate_limiting` | `AIRELOOM_ENABLE_RATE_LIMITING` | `True` | Enable rate limit handling |
| `rate_limit_buffer_percentage` | `AIRELOOM_RATE_LIMIT_BUFFER_PERCENTAGE` | `0.1` | Buffer percentage (e.g. 10%) |
| `rate_limit_retry_after_default` | `AIRELOOM_RATE_LIMIT_RETRY_AFTER_DEFAULT` | `60` | Default retry-after seconds on 429 |

## Caching

See [Caching](caching.md) for details.

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `enable_caching` | `AIRELOOM_ENABLE_CACHING` | `False` | Enable response caching |
| `cache_ttl_seconds` | `AIRELOOM_CACHE_TTL_SECONDS` | `300` | Cache entry TTL in seconds |
| `cache_max_size` | `AIRELOOM_CACHE_MAX_SIZE` | `128` | Max LRU cache entries |

## Hooks

See [Request Hooks](hooks.md) for details.

| Setting | Default | Description |
|---|---|---|
| `pre_request_hooks` | `[]` | Callables invoked before each request |
| `post_request_hooks` | `[]` | Callables invoked after each response |

## API Base URLs

Base URLs are hardcoded in `aireloom.constants` and cannot be overridden via settings:

- Graph API: `https://api.openaire.eu/v1/`
- Scholexplorer: `https://api-beta.scholexplorer.openaire.eu/v3/`

## Using `.env` Files

Create a `.env` or `secrets.env` file in your project root:

```dotenv
AIRELOOM_REQUEST_TIMEOUT=45.0
AIRELOOM_MAX_RETRIES=5
AIRELOOM_OPENAIRE_API_TOKEN="your_token_here"
AIRELOOM_ENABLE_CACHING=true
AIRELOOM_CACHE_TTL_SECONDS=600
```

## Programmatic Configuration

```python
from aireloom import AireloomSession
from aireloom.config import ApiSettings
from bibliofabric.auth import NoAuth

settings = ApiSettings(
    request_timeout=60.0,
    max_retries=2,
    enable_caching=True,
    cache_ttl_seconds=1800,
)

async with AireloomSession(settings=settings, auth_strategy=NoAuth()) as session:
    # Your API calls here
    pass
```
