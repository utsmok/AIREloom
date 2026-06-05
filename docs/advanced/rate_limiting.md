# Rate Limiting

AIREloom handles API rate limits automatically when `enable_rate_limiting` is `True` (the default).

## How It Works

### HTTP headers inspected

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Total requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests remaining in the window |
| `X-RateLimit-Reset` | When the window resets (UTC epoch seconds) |
| `Retry-After` | Seconds to wait after a 429 response |

### Behavior

1. **Proactive pausing** — if `X-RateLimit-Remaining` drops below the buffer threshold, the client may pause before the next request.
2. **429 handling** — on a `429 Too Many Requests` response:
   - Wait for `Retry-After` seconds if the header is present.
   - Otherwise wait for `rate_limit_retry_after_default` seconds.
   - Retry up to `max_retries` times with exponential backoff.
3. **Final failure** — if all retries are exhausted, a `RateLimitError` is raised.

## Configuration

| Setting | Env Variable | Default | Description |
|---|---|---|---|
| `enable_rate_limiting` | `AIRELOOM_ENABLE_RATE_LIMITING` | `True` | Enable rate limit handling |
| `rate_limit_buffer_percentage` | `AIRELOOM_RATE_LIMIT_BUFFER_PERCENTAGE` | `0.1` | Buffer (e.g. 10%) before proactive pausing |
| `rate_limit_retry_after_default` | `AIRELOOM_RATE_LIMIT_RETRY_AFTER_DEFAULT` | `60` | Default wait on 429 without `Retry-After` |
| `max_retries` | `AIRELOOM_MAX_RETRIES` | `3` | Max retry attempts for 429 errors |

See [Configuration](configuration.md) for general config details.

## Example

```python
from aireloom import AireloomSession
from aireloom.config import ApiSettings
from bibliofabric.auth import NoAuth
from bibliofabric.exceptions import RateLimitError

settings = ApiSettings(
    enable_rate_limiting=True,
    max_retries=5,
    rate_limit_retry_after_default=30,
)

async with AireloomSession(settings=settings, auth_strategy=NoAuth()) as session:
    try:
        product = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")
        print(product.mainTitle)
    except RateLimitError as e:
        print(f"Rate limited after retries: {e.message}")
```

## Best Practices

- **Keep rate limiting enabled** unless you handle it externally.
- **Be mindful of batch operations** — loops of `get()` or `iterate()` calls can still hit limits; the client will wait and retry, but overall latency increases.
- **Adjust `max_retries`** if the default of 3 is too aggressive or too conservative for your workload.
