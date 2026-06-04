# AIREloom — Project Guide

## What It Is

AIREloom is an async Python client library for the [OpenAIRE Graph API](https://api.openaire.eu) and [Scholexplorer API](https://api.scholexplorer.openaire.eu). It provides typed, ergonomic access to research products, organizations, projects, data sources, and scholarly link relationships.

Built on top of **bibliofabric** — a generic async API client framework providing auth, pagination, response unwrapping, and mixin-based resource operations.

**Status:** Alpha. No published release yet. Architecture is settled; needs real-world usage and validation.

## Architecture

```
AireloomSession          # User-facing async context manager (session.py)
 └─ AireloomClient       # Core HTTP client, auth resolution, resource orchestration (client.py)
     ├─ ResearchProductsClient   # Mixin-based (bibliofabric)
     ├─ ProjectsClient           # Mixin-based (bibliofabric)
     ├─ OrganizationsClient      # Mixin-based (bibliofabric)
     ├─ DataSourcesClient        # Mixin-based (bibliofabric)
     └─ ScholixClient            # Custom (different base URL, page-based pagination)
```

### Key Layers

| Layer | File(s) | Role |
|-------|---------|------|
| **Session** | `session.py` | Thin async context manager wrapper around `AireloomClient`. Entry point for users. |
| **Client** | `client.py` | Extends `bibliofabric.BaseApiClient`. Resolves auth strategy, initializes resource clients. ~230 lines. |
| **Resources** | `resources/*.py` | Per-endpoint clients. All Graph API clients (`ResearchProductsClient`, `ProjectsClient`, `OrganizationsClient`, `DataSourcesClient`) use bibliofabric mixins (`GettableMixin`, `SearchableMixin`, `CursorIterableMixin`). `ScholixClient` has a custom implementation (different base URL, page-based pagination via `PageIterableMixin`). |
| **Models** | `models/*.py` | Pydantic v2 models for each entity type. All inherit `BaseEntity` (has `id` field). `ApiResponse[T]` is the generic list-response envelope with `Header` + `results`. All models use `extra="allow"` for forward compatibility. |
| **Endpoints** | `endpoints.py` | Pydantic filter models per endpoint (`ResearchProductsFilters`, etc.) with `extra="forbid"`. `ENDPOINT_DEFINITIONS` maps endpoint paths to filter models and valid sort fields. |
| **Unwrapper** | `unwrapper.py` | Implements `bibliofabric.ResponseUnwrapper` protocol. Extracts `results`, `header.nextCursor`, `header.numFound` from OpenAIRE's JSON envelope. |
| **Config** | `config.py` | `ApiSettings(BaseApiSettings)` via pydantic-settings. Env prefix `AIRELOOM_`. Reads `.env`/`secrets.env`. Cached via `@lru_cache`. |
| **Constants** | `constants.py` | Base URLs, defaults, enums (`EndpointName`, `SortOrder`), HTTP headers. |


### Two API Surfaces
- **Graph API** (`api.openaire.eu/graph/v1`): research products, organizations, projects, data sources. Cursor-based pagination.
- **Scholix API** (`api.scholexplorer.openaire.eu/v3`): scholarly link relationships between entities. Page-based pagination. Requires either `sourcePid` or `targetPid` filter. `ScholixClient` uses its own base URL.

### Auth

Three strategies (from `bibliofabric.auth`), resolved in this priority:
1. `ClientCredentialsAuth` — OAuth2 client credentials flow (client_id + client_secret)
2. `StaticTokenAuth` — Bearer token
3. `NoAuth` — unauthenticated (rate-limited)

Credentials from: explicit params > env vars (`AIRELOOM_*`) > `.env`/`secrets.env`.

## Tech Stack

- **Python 3.12+**, `uv` for dependency management
- **bibliofabric** — framework providing `BaseApiClient`, auth strategies, resource mixins, `ResponseUnwrapper` protocol
- **pydantic v2** + **pydantic-settings** for models and config
- **httpx** for async HTTP (via bibliofabric)
- **pytest** + **pytest-asyncio** + **pytest-httpx** for testing
- **ruff** for linting/formatting
- **mkdocs-material** + **mkdocstrings** for docs

## Project Structure

```
src/aireloom/
  __init__.py           # Re-exports: client, session, models, exceptions
  client.py             # AireloomClient (BaseApiClient subclass)
  session.py            # AireloomSession (user-facing async context manager)
  config.py             # ApiSettings (pydantic-settings)
  constants.py          # URLs, defaults, enums
  endpoints.py          # Filter models + ENDPOINT_DEFINITIONS
  unwrapper.py          # OpenAireUnwrapper (ResponseUnwrapper protocol)
  models/
    base.py             # Header, BaseEntity, ApiResponse[T]
    research_product.py # ResearchProduct (~500 lines, richest model)
    project.py          # Project + nested funding/grant models
    organization.py     # Organization
    data_source.py      # DataSource
    scholix.py          # ScholixRelationship + nested types
  resources/
    base_client.py      # BaseResourceClient (holds ref to AireloomClient)
    research_products_client.py  # Mixin-based
    projects_client.py           # Mixin-based
    organizations_client.py      # Custom impl
    data_sources_client.py       # Custom impl
    scholix_client.py            # Custom impl, separate base URL
tests/
  conftest.py           # Loads .env, provides api_token fixture
  test_session.py       # Integration tests via mocked HTTP (httpx_mock)
  test_auth.py          # Auth strategy unit tests
  test_config.py        # Config/env override tests
  test_unwrapper.py     # Response unwrapper unit tests
  test_client.py        # Client fixture helpers
  test_actual_data.py   # Live API comparison tests (requires token)
  resources/            # Per-resource client unit tests
  verification_script.py # Manual end-to-end verification runner
docs/                   # MkDocs documentation
.github/workflows/      # CI: lint, test, build docs, publish on tag
```

## Development Commands

```bash
uv sync --all-groups --all-extras    # Install everything
uv run ruff check src/ --fix         # Lint
uv run ruff format src/              # Format
uv run pytest tests/                 # Run tests
uv run pytest --cov=aireloom tests/  # Coverage (note: CI uses --cov=myproj — likely a bug)
uv build                             # Build package
uv run mkdocs serve                  # Local docs
```

## Key Patterns & Conventions

- **All I/O is async.** Every resource method is `async`. Use `async with AireloomSession() as session:` or `async with AireloomClient() as client:`.
- **Pydantic filter models** are passed to `search()` and `iterate()`. They serialize to query params. `extra="forbid"` on filters prevents typos.
- **Sort validation** happens via overridable `_validate_sort_field()` in `bibliofabric.BaseResourceClient`. Default is no-op; AIREloom consumers can override to check against `ENDPOINT_DEFINITIONS`.
- **Models use `extra="allow"`** everywhere to tolerate API field additions without breaking.
- **Resource clients:** All four Graph API clients use bibliofabric mixins (clean, ~58 lines each). `ScholixClient` has a custom implementation due to different base URL and page-based pagination.

## Known Issues & Gaps

- **`verification_script.py`** at project root is a standalone script, not a pytest test.
- **`simple_example.py`** and `aireloom_comprehensive_analysis.py`** at root are standalone scripts, not part of the package.
- **Docs content files** like `filter_options.md` (41 bytes), `models.md` (30 bytes), `session.md` (32 bytes) are stubs.
- **`constants.py` TODO** comment lists unfinished enumerations (sortable fields, filter keys, open access routes, funder IDs, country codes).

## Resolved Issues

- ~~Inconsistent resource clients~~ — OrganizationsClient and DataSourcesClient now use bibliofabric mixins. ScholixClient stays custom (different base URL, page-based pagination).
- ~~CI `--cov=myproj`~~ — Fixed to `--cov=aireloom`.
- ~~Version triple source of truth~~ — Single source in `pyproject.toml`, dynamic via `importlib.metadata`.
- ~~`EndpointName` enum~~ — Removed (unused).
- ~~Duplicate base URL definitions~~ — Removed from `endpoints.py`.
- ~~`test_actual_data.py` live API~~ — Guarded with `pytest.mark.live_api` marker, skipped by default.
- ~~`ResearchProductsClient._valid_sort_fields`~~ — Removed. Sort validation now via overridable `_validate_sort_field()` in bibliofabric.
- ~~`publish-pypi` job URLs~~ — Fixed to `aireloom`.
- ~~`conftest.py` dotenv dependency~~ — `python-dotenv` added to dev dependencies.