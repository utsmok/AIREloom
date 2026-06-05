# Client-Side Caching

AIREloom can cache `GET` responses in an in-memory LRU store to reduce latency and avoid redundant API calls.

## How It Works

When caching is enabled:

1. On each `GET` request, AIREloom checks the cache for a matching URL + parameters entry.
2. If a valid (non-expired) entry exists, it is returned without hitting the API.
3. If not found or expired, the API is called and the successful response is stored.

Only `GET` requests are cached. Mutating operations (`POST`, `PUT`, `DELETE`) are never cached.

## Configuration

All settings live in `ApiSettings`. See [Configuration](configuration.md) for general config details.

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `enable_caching` | `AIRELOOM_ENABLE_CACHING` | `False` | Enable or disable caching |
| `cache_ttl_seconds` | `AIRELOOM_CACHE_TTL_SECONDS` | `300` | Time-to-live for cache entries (seconds) |
| `cache_max_size` | `AIRELOOM_CACHE_MAX_SIZE` | `128` | Maximum entries in the LRU cache |

### Via environment variables

```dotenv
AIRELOOM_ENABLE_CACHING=true
AIRELOOM_CACHE_TTL_SECONDS=600
AIRELOOM_CACHE_MAX_SIZE=256
```

### Programmatically

```python
from aireloom import AireloomSession
from aireloom.config import ApiSettings
from bibliofabric.auth import NoAuth

settings = ApiSettings(
    enable_caching=True,
    cache_ttl_seconds=900,  # 15 minutes
    cache_max_size=100,
)

async with AireloomSession(settings=settings, auth_strategy=NoAuth()) as session:
    # First call fetches from API and caches
    product = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")
    print(product.mainTitle)

    # Second call is served from cache (within TTL)
    product2 = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")
    print(product2.mainTitle)
```

## Considerations

- **Staleness:** Cached data may become stale before TTL expires. Use a shorter TTL for frequently changing resources.
- **Memory:** The cache is in-process. `cache_max_size` bounds memory usage.
- **Scope:** Each `AireloomClient` (and therefore each `AireloomSession`) has its own cache. Separate sessions do not share cache entries.
