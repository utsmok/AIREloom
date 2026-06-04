# AIREloom — Project Guide

## What It Is

AIREloom is an async Python client library for the [OpenAIRE Graph API](https://api.openaire.eu) and [Scholexplorer API](https://api.scholexplorer.openaire.eu). It provides typed, ergonomic access to research products, organizations, projects, data sources, and scholarly link relationships.

Built on top of **bibliofabric** — a generic async API client framework providing auth, pagination, response unwrapping, and mixin-based resource operations.

**Status:** Alpha. Published on PyPI as `aireloom`.

## Architecture

```
AireloomSession          # User-facing async context manager (session.py)
 └─ AireloomClient       # Core HTTP client, auth resolution, resource orchestration (client.py)
     ├─ ResearchProductsClient   # v2, mixin-based (bibliofabric)
     ├─ ProjectsClient           # v1, mixin-based (bibliofabric)
     ├─ OrganizationsClient      # v1, mixin-based (bibliofabric)
     ├─ DataSourcesClient        # v1, mixin-based (bibliofabric)
     ├─ PersonsClient            # v1, mixin-based (bibliofabric) — NEW
     └─ ScholixClient            # v3, custom methods (different base URL, 0-indexed pagination)
```

### Key Layers

| Layer | File(s) | Role |
|-------|---------|------|
| **Session** | `session.py` | Thin async context manager wrapper around `AireloomClient`. Entry point for users. |
| **Client** | `client.py` | Extends `bibliofabric.BaseApiClient`. Resolves auth strategy, initializes resource clients. |
| **Resources** | `resources/*.py` | Per-endpoint clients. All inherit from `bibliofabric.resources.BaseResourceClient`. Graph API clients use mixins (`GettableMixin`, `SearchableMixin`, `CursorIterableMixin`). `ResearchProductsClient` overrides `_base_url_override` to v2. Others use default v1. `ScholixClient` has custom `search_links()`/`iterate_links()` (0-indexed pages, `size` param, `_base_url_override`). |
| **Models** | `models/*.py` | Pydantic v2 models for each entity type. All inherit `BaseEntity` (has `id` field). `ApiResponse[T]` is the generic list-response envelope with `Header` + `results`. All models use `extra="allow"` for forward compatibility. |
| **Endpoints** | `endpoints.py` | Pydantic filter models per endpoint (`ResearchProductsFilters`, etc.) with `extra="forbid"`. `ENDPOINT_DEFINITIONS` maps endpoint paths to filter models and valid sort fields. |
| **Unwrapper** | `unwrapper.py` | Implements `bibliofabric.ResponseUnwrapper` protocol. Extracts `results`, `header.nextCursor`, `header.numFound` from OpenAIRE's JSON envelope. |
| **Config** | `config.py` | `ApiSettings(BaseApiSettings)` via pydantic-settings. Env prefix `AIRELOOM_`. Reads `.env`. Cached via `@lru_cache`. |
| **Constants** | `constants.py` | Base URLs, defaults, version detection (`importlib.metadata`), enums (`SortOrder`). |


### API Version Routing
- **Research Products**: `api.openaire.eu/graph/v2` — via `_base_url_override` on `ResearchProductsClient`
- **All other Graph entities** (projects, organizations, data sources, persons): `api.openaire.eu/graph/v1` — default base URL
- **Scholix API**: `api.scholexplorer.openaire.eu/v3` — via `_base_url_override` on `ScholixClient`. Page-based, 0-indexed pagination. Requires either `sourcePid` or `targetPid` filter.

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
  constants.py          # URLs (v1 + v2), defaults, version detection
  endpoints.py          # Filter models + ENDPOINT_DEFINITIONS (6 entity types)
  unwrapper.py          # OpenAireUnwrapper (ResponseUnwrapper protocol)
  models/
    base.py             # Header (numFound, page, maxScore, nextCursor), BaseEntity, ApiResponse[T]
    research_product.py # ResearchProduct — 40+ typed fields including v2 relationship fields
    project.py          # Project + nested funding/grant models
    organization.py     # Organization
    data_source.py      # DataSource
    person.py           # Person (givenName, familyName, biography, etc.)
    scholix.py          # ScholixRelationship + nested types
  resources/
    research_products_client.py  # v2, mixin-based, _base_url_override
    projects_client.py           # v1, mixin-based
    organizations_client.py      # v1, mixin-based
    data_sources_client.py       # v1, mixin-based
    persons_client.py            # v1, mixin-based
    scholix_client.py            # v3, custom methods, _base_url_override
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
- **Resource clients:** All inherit from `bibliofabric.resources.BaseResourceClient`. Graph API clients use mixins (~58 lines each). `ResearchProductsClient` routes to v2; others use default v1. `ScholixClient` has custom methods due to 0-indexed pagination and `size` param.

## Known Issues & Gaps

- **Cursor pagination ordering**: Solr's cursorMark uses deterministic internal ordering that ignores `sortBy`. The first pages of cursor results may surface records without PIDs even when filtering for DOI-rich records. Not a library issue — use page-based pagination (`search()`) when PIDs matter.
- **Graph API v3**: OpenAIRE Graph API v3 uses kebab-case URLs and string-based filters. Not yet supported — stick with v1/v2. (Scholix v3 is fully supported and is not a beta.)
- **No sub-endpoints**: The API does NOT support `/{entity}/{id}/related*`, `/{entity}/{id}/links`, or `/{entity}/count` — all return 405/404. Verified by live testing.
- **Person filter bug**: `givenName` and `lastName` are accepted API parameters but cause HTTP 500 from the server. Only `search`, `id`, `originalId` work reliably.
- **Sort format**: `sortBy` takes `"fieldname ASC|DESC"` as a single string (e.g. `sortBy="relevance ASC"`). No separate `sortOrder` param exists.
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
- ~~`openaireCompatibility` filter~~ — Removed from `DataSourcesFilters`. Not a valid API parameter (returns 400 "Unknown parameter").
- ~~Missing `logicalOperator` filter~~ — Added to all 5 Graph API filter models. Accepts `"AND"` or `"OR"`.
- ~~Missing `rorId` filter~~ — Added to `ResearchProductsFilters`. ROR identifier for affiliated organization.
- ~~`popularity` sort field~~ — Removed from RP sort fields. Not a valid sort field (API returns 400).
- ~~Persons sort fields~~ — Added `startDate`, `endDate` (matching API validation).
- ~~Person model incomplete~~ — Added `originalId`, `alternativeNames` fields, typed `consent` as `bool`, typed list elements.
