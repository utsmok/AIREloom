# Error Handling

AIREloom raises a hierarchy of custom exceptions, all inheriting from `BibliofabricError`. Each carries a `message`, an optional `response` (`httpx.Response`), and an optional `request` (`httpx.Request`).

## Exception Hierarchy

```
BibliofabricError
├── APIError              # Non-success HTTP status (4xx / 5xx)
│   ├── NotFoundError     # 404
│   └── RateLimitError    # 429
├── ValidationError       # Invalid input or API validation error (400 / 422)
├── TimeoutError          # Request timed out
├── NetworkError          # DNS, connection refused, etc.
├── AuthError             # 401 / 403 or token acquisition failure
└── ConfigurationError    # Missing or invalid config
```

## Quick Reference

| Exception | When | Has `response`? |
|---|---|---|
| `NotFoundError` | Resource not found (404) | Yes |
| `RateLimitError` | Rate limit exceeded (429) | Yes |
| `ValidationError` | Bad input or validation failure | Maybe |
| `TimeoutError` | Request exceeded timeout | No |
| `NetworkError` | DNS or connection failure | No |
| `AuthError` | Authentication / authorization failure | Maybe |
| `APIError` | Any other HTTP error | Yes |

## Example

```python
from aireloom import AireloomSession
from bibliofabric.auth import NoAuth
from bibliofabric.exceptions import (
    BibliofabricError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

async with AireloomSession(auth_strategy=NoAuth()) as session:
    try:
        product = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")
        print(product.mainTitle)

    except NotFoundError as e:
        print(f"Not found: {e.message}")

    except ValidationError as e:
        print(f"Validation failed: {e.message}")

    except RateLimitError as e:
        retry = e.response.headers.get("Retry-After") if e.response else None
        print(f"Rate limited. Retry after: {retry}s")

    except BibliofabricError as e:
        print(f"Error: {e.message}")
```

## Best Practices

- **Catch specific exceptions first** — `NotFoundError` before `APIError` before `BibliofabricError`.
- **Inspect `response` and `request`** — they carry the HTTP details you need for logging and diagnostics.
- **Log details in production** — include `e.response.status_code`, `e.response.text`, and `e.request.url`.
- **Don't suppress errors silently** — at minimum, log the `message` and relevant context.
