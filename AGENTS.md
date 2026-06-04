# AIREloom — Project Guide

## What It Is

AIREloom is an async Python client library for the [OpenAIRE Graph API](https://api.openaire.eu) and [Scholexplorer API](https://api.scholexplorer.openaire.eu). It provides typed, ergonomic access to research products, organizations, projects, data sources, and scholarly link relationships.

Built on top of **bibliofabric** — a generic async API client framework providing auth, pagination, response unwrapping, and mixin-based resource operations.

**Status:** Alpha. Published on PyPI as `aireloom`.

## Architecture

```
AireloomSession          # User-facing async context manager (session.py)
 └─ AireloomClient       # Core HTTP client, auth resolution, resource orchestration (client.py)
     ├─ ResearchProductsClient   # Mixin-based (bibliofabric)
     ├─ ProjectsClient           # Mixin-based (bibliofabric)
     ├─ OrganizationsClient      # Mixin-based (bibliofabric)
     ├─ DataSourcesClient        # Mixin-based (bibliofabric)
     └─ ScholixClient            # Custom methods (different base URL, 0-indexed pagination)
```

### Key Layers

| Layer | File(s) | Role |
|-------|---------|------|
| **Session** | `session.py` | Thin async context manager wrapper around `AireloomClient`. Entry point for users. |
| **Client** | `client.py` | Extends `bibliofabric.BaseApiClient`. Resolves auth strategy, initializes resource clients. |
| **Resources** | `resources/*.py` | Per-endpoint clients. All five clients inherit from `bibliofabric.resources.BaseResourceClient`. Graph API clients use mixins (`GettableMixin`, `SearchableMixin`, `CursorIterableMixin`). `ScholixClient` has custom `search_links()`/`iterate_links()` (0-indexed pages, `rows` param, `_base_url_override`). |
| **Models** | `models/*.py` | Pydantic v2 models for each entity type. All inherit `BaseEntity` (has `id` field). `ApiResponse[T]` is the generic list-response envelope with `Header` + `results`. All models use `extra="allow"` for forward compatibility. |
| **Endpoints** | `endpoints.py` | Pydantic filter models per endpoint (`ResearchProductsFilters`, etc.) with `extra="forbid"`. `ENDPOINT_DEFINITIONS` maps endpoint paths to filter models and valid sort fields. |
| **Unwrapper** | `unwrapper.py` | Implements `bibliofabric.ResponseUnwrapper` protocol. Extracts `results`, `header.nextCursor`, `header.numFound` from OpenAIRE's JSON envelope. |
| **Config** | `config.py` | `ApiSettings(BaseApiSettings)` via pydantic-settings. Env prefix `AIRELOOM_`. Reads `.env`. Cached via `@lru_cache`. |
| **Constants** | `constants.py` | Base URLs, defaults, version detection (`importlib.metadata`), enums (`SortOrder`). |


### Two API Surfaces
- **Graph API** (`api.openaire.eu/graph/v1`): research products, organizations, projects, data sources. Cursor-based pagination.
- **Scholix API** (`api.scholexplorer.openaire.eu/v3`): scholarly link relationships between entities. Page-based, 0-indexed pagination. Requires either `sourcePid` or `targetPid` filter. `ScholixClient` uses `_base_url_override`.

### Auth

Three strategies (from `bibliofabric.auth`), resolved in this priority:
1. `ClientCredentialsAuth` — OAuth2 client credentials flow (client_id + client_secret)
2. `StaticTokenAuth` — Bearer token
3. `NoAuth` — unauthenticated (rate-limited)

Credentials from: explicit params > env vars (`AIRELOOM_*`) > `.env`.

## Tech Stack

- **Python 3.12+**, `uv` for dependency management
- **bibliofabric** — framework providing `BaseApiClient`, auth strategies, resource mixins, `ResponseUnwrapper` protocol
- **pydantic v2** + **pydantic-settings** for models and config
- **httpx** for async HTTP (via bibliofabric)
- **pytest** + **pytest-asyncio** + **pytest-httpx** for testing
- **ruff** for linting/formatting
- **ty** for type checking
- **mkdocs-material** + **mkdocstrings** for docs

## Project Structure

```
src/aireloom/
  __init__.py           # Re-exports: client, session, models, exceptions
  client.py             # AireloomClient (BaseApiClient subclass)
  session.py            # AireloomSession (user-facing async context manager)
  config.py             # ApiSettings (pydantic-settings)
  constants.py          # URLs, defaults, enums, version detection
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
    research_products_client.py  # Mixin-based
    projects_client.py           # Mixin-based
    organizations_client.py      # Mixin-based
    data_sources_client.py       # Mixin-based
    scholix_client.py            # Custom methods, _base_url_override
tests/
  conftest.py           # Loads .env, provides api_token fixture
  test_session.py       # Integration tests via mocked HTTP (httpx_mock)
  test_auth.py          # Auth strategy unit tests
  test_config.py        # Config/env override tests
  test_unwrapper.py     # Response unwrapper unit tests
  test_client.py        # Client unit tests + coverage
  test_models.py        # Pydantic model validator tests
  test_actual_data.py   # Live API tests (requires token, skipped by default)
  resources/            # Per-resource client unit tests
examples/
  simple_example.py     # Basic usage demo
  comprehensive_analysis.py  # Full analysis pipeline (DuckDB, matplotlib)
  README.md             # Example descriptions
docs/                   # MkDocs documentation
.github/workflows/      # CI: lint, type check, test, build docs, publish on tag
```

## Development Commands

```bash
uv sync --all-groups --all-extras         # Install everything
uv run ruff check src/ --fix              # Lint
uv run ruff format src/                   # Format
uvx ty check src/                         # Type check
uv run pytest tests/                      # Run tests
uv run pytest --cov=aireloom tests/       # Coverage (CI threshold: 95%)
uv build                                  # Build package
uv run mkdocs serve                       # Local docs
```

## Key Patterns & Conventions

- **All I/O is async.** Every resource method is `async`. Use `async with AireloomSession() as session:` or `async with AireloomClient() as client:`.
- **Pydantic filter models** are passed to `search()` and `iterate()`. They serialize to query params. `extra="forbid"` on filters prevents typos.
- **Sort validation** happens via overridable `_validate_sort_field()` in `bibliofabric.BaseResourceClient`. Default is no-op; AIREloom consumers can override to check against `ENDPOINT_DEFINITIONS`.
- **Models use `extra="allow"`** everywhere to tolerate API field additions without breaking.
- **Resource clients:** All five clients inherit from `bibliofabric.resources.BaseResourceClient`. Graph API clients use mixins (~58 lines each). `ScholixClient` has custom methods due to 0-indexed pagination and `rows` param.

## Known Issues & Gaps

- **`constants.py` TODO** comment lists unfinished enumerations (sortable fields, filter keys, open access routes, funder IDs, country codes).
- **ScholixClient doesn't use `SearchableMixin`/`PageIterableMixin`** — Scholix API uses `rows` (not `pageSize`) and 0-indexed pages. Custom methods are kept. If bibliofabric mixins gain param-name configurability, Scholix could adopt them.

## Resolved Issues

- ~~Duplicate `BaseResourceClient`~~ — Removed. All resource clients now use `bibliofabric.resources.BaseResourceClient`.
- ~~Root scripts clutter~~ — Moved to `examples/` directory.
- ~~`secrets.env` references~~ — Fixed to `.env`.
- ~~CI `--cov=myproj`~~ — Fixed to `--cov=aireloom`.
- ~~Version triple source of truth~~ — Single source: `constants.py` via `importlib.metadata`.
- ~~`EndpointName` enum~~ — Removed (unused).
- ~~Duplicate base URL definitions~~ — Removed from `endpoints.py`.
- ~~`test_actual_data.py` live API~~ — Guarded with `pytest.mark.live_api` marker, skipped by default.
- ~~No type checking in CI~~ — `ty check src/` added.
- ~~Single Python version in CI~~ — Matrix includes 3.12 + 3.13.
- ~~Docs deploy on PRs~~ — Guarded to only deploy on pushes.
- ~~No coverage enforcement~~ — `--cov-fail-under=95` in CI.
