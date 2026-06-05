# Request Hooks

AIREloom lets you inject custom logic into the request/response lifecycle via hook functions registered on `ApiSettings`.

## Hook Types

### Pre-request hooks

Called before each HTTP request. Receives an `httpx.Request` object.

```python
import httpx

def log_request(request: httpx.Request) -> None:
    print(f"→ {request.method} {request.url}")
```

### Post-request hooks

Called after each response is received and parsed. Receives an `httpx.Response` and an optional parsed Pydantic model.

```python
import httpx
from typing import Any

def log_response(response: httpx.Response, model: Any) -> None:
    print(f"← {response.status_code} from {response.url}")
    if model:
        print(f"  Parsed: {type(model).__name__}")
```

## Registering Hooks

Pass lists of callables to `ApiSettings`:

```python
from aireloom import AireloomSession
from aireloom.config import ApiSettings
from bibliofabric.auth import NoAuth

settings = ApiSettings(
    pre_request_hooks=[log_request],
    post_request_hooks=[log_response],
)

async with AireloomSession(settings=settings, auth_strategy=NoAuth()) as session:
    product = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")
    print(product.mainTitle)
```

## Configuration Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `pre_request_hooks` | `list[callable]` | `[]` | Called before each request |
| `post_request_hooks` | `list[callable]` | `[]` | Called after each response |

These are set programmatically (not via environment variables) since they require function objects.

## Use Cases

- **Logging** — record request URLs, methods, and response statuses.
- **Metrics** — collect timing data or success/failure rates.
- **Request modification** — add tracing headers or custom auth tokens.
- **Response validation** — trigger alerts on specific status codes or content patterns.

## Considerations

- **Keep hooks lightweight.** They run synchronously in the async request flow.
- **Handle errors inside hooks.** An exception in a hook will disrupt the request.
- **Hooks run per retry.** If a request is retried, pre-request hooks fire again.
- **Order matters.** Hooks execute in the order they appear in the list.
