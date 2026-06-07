# AIREloom: Asynchronous Python client for the OpenAIRE API

<p align="center"><img src="https://github.com/user-attachments/assets/54a7de2e-9469-4d81-ba33-788a5a0aa753" alt="AIREloom logo" height="393" width="500" /></p>

*Samuel Mok · s.mok@utwente.nl · 2025–2026*

AIREloom is an async Python client for the [OpenAIRE Graph API](https://graph.openaire.eu/) and [Scholexplorer API](https://scholexplorer.openaire.eu/), built on [bibliofabric](https://github.com/utsmok/bibliofabric).

**Docs:** [utsmok.github.io/AIREloom](https://utsmok.github.io/AIREloom/) · **PyPI:** [aireloom](https://pypi.org/project/aireloom/) · **License:** MIT

## Features

- **Full API coverage** — Research Products (v2), Projects, Organizations, Data Sources, Persons, Research Product Links (v1), Scholexplorer (v3)
- **Async by design** — built on `httpx` + `asyncio` with proper connection pooling
- **Typed throughout** — Pydantic models for all inputs/outputs, PEP 561 `py.typed` marker
- **Ergonomics layer** — computed properties, SafeStr/SafeList defaults, convenience queries, iterator helpers
- **Flexible auth** — auto-detection from env vars, static tokens, OAuth2 client credentials, or no auth
- **Resilient** — retries with backoff, rate-limit handling (`Retry-After`), optional client-side caching, hook system

## Installation

```bash
uv add aireloom
```

Or with pip: `pip install aireloom`. Requires Python ≥3.12.

## Quick Start

```python
import asyncio
from aireloom import AireloomSession
from aireloom.endpoints import ResearchProductsFilters

async def main():
    async with AireloomSession() as session:
        # Search publications
        filters = ResearchProductsFilters(
            type="article", mainTitle="climate change",
            fromPublicationDate="2024-01-01",
        )
        response = await session.research_products.search(
            filters=filters, page_size=5, sortBy="publicationDate desc",
        )
        for product in response.results:
            print(f"{product.title} — DOI: {product.doi or 'N/A'}")

        # Iterate all results (cursor-based auto-pagination)
        filters2 = ResearchProductsFilters(type="dataset", countryCode="NL")
        async for product in session.research_products.iterate(
            filters=filters2, page_size=50,
        ):
            print(product.title)
            break  # stop when you want

        # Get a single entity
        product = await session.research_products.get("doi:10.1038/s41586-021-03964-9")
        print(product.title, product.doi)

        # Convenience queries
        citations = await session.queries.citing_works("doi:10.1038/s41586-021-03964-9")
        print(f"{len(citations)} citations")

asyncio.run(main())
```

No authentication required — the OpenAIRE API works without it. For higher rate limits, see [Authentication](#authentication).

## Core API

### Retrieval methods

Every resource client (`session.research_products`, `session.organizations`, etc.) provides:

| Method | Description |
|--------|-------------|
| `get(id)` | Retrieve a single entity by ID |
| `search(filters, page, page_size, sortBy)` | Paginated search |
| `iterate(filters, page_size, sortBy)` | Auto-paginate all results (cursor-based) |
| `collect(limit, ...)` | Collect results into a list |
| `count(filters)` | Count matching entities |
| `first(filters)` | Get first matching entity or `None` |

### Resource clients

| Client | API | Notes |
|--------|-----|-------|
| `session.research_products` | Graph API v2 | Enriched responses with related entities |
| `session.projects` | Graph API v1 | |
| `session.organizations` | Graph API v1 | |
| `session.data_sources` | Graph API v1 | |
| `session.persons` | Graph API v1 | `givenName`/`lastName` filters cause 500s (upstream bug) |
| `session.scholix` | Scholix v3 | `search_links()` / `iterate_links()` |

### Ergonomics

**Computed properties** on models — derived fields that don't exist in the raw API response:

```python
product.doi              # → "10.1234/example" (extracted from pids)
product.publication_year  # → 2024 (from publicationDate)
product.is_open_access   # → True (from bestAccessRight)
org.ror_id               # → "https://ror.org/..." (from rorId)
project.funder_name      # → "EC" (from funding array)
```

**SafeStr/SafeList** — `None` is never returned for string/list fields; you get `""` or `[]` instead:

```python
product.subjects  # [] instead of None
product.title     # "" instead of None
```

**Convenience queries** via `session.queries`:

```python
session.queries.publications_by_doi("10.1234/example")
session.queries.citing_works("doi:10.1234/example")
session.queries.datasets_by_organization("openaire____::orgID:grid.5522.e")
session.queries.projects_by_funder("EC")
```

See [Ergonomics docs](https://utsmok.github.io/AIREloom/ergonomics/) for the full list.

### Filters & Sorting

Filters are Pydantic models — import from `aireloom.endpoints`:

```python
from aireloom.endpoints import ResearchProductsFilters, ProjectsFilters

filters = ResearchProductsFilters(
    type="article",
    mainTitle="machine learning",
    fromPublicationDate="2024-01-01",
    countryCode="NL",
)
```

Sort with `sortBy="field asc"` or `sortBy="field desc"`. Valid fields depend on the endpoint (see [`ENDPOINT_DEFINITIONS`](src/aireloom/endpoints.py)).

## Authentication

AIREloom auto-detects auth from environment variables or `.env` files (prefixed with `AIRELOOM_`). No auth is the default if nothing is configured.

```dotenv
# Option 1: Static token
AIRELOOM_OPENAIRE_API_TOKEN=your_token

# Option 2: OAuth2 client credentials
AIRELOOM_OPENAIRE_CLIENT_ID=your_id
AIRELOOM_OPENAIRE_CLIENT_SECRET=your_secret
```

Or pass explicitly:

```python
from bibliofabric.auth import NoAuth, StaticTokenAuth, ClientCredentialsAuth

session = AireloomSession(auth_strategy=StaticTokenAuth(token="..."))
```

See [Authentication docs](https://utsmok.github.io/AIREloom/authentication/) for details.

## Error Handling

```python
from bibliofabric.exceptions import (
    BibliofabricError, APIError, NotFoundError, RateLimitError,
    TimeoutError, NetworkError, AuthError, ValidationError,
)
```

See [Error Handling docs](https://utsmok.github.io/AIREloom/advanced/error_handling/) for the full hierarchy.

## Examples

All examples in [`examples/`](examples/) are dual-purpose — run as scripts or as interactive [marimo](https://marimo.io) notebooks:

```bash
# As a script
uv run examples/simple_example.py

# As an interactive notebook
uv run marimo edit examples/simple_example.py
```

| Script | Description |
|--------|-------------|
| `simple_example.py` | Search, iterate, get research products |
| `02_scholix_link_discovery.py` | Discover publication–dataset links via Scholexplorer |
| `03_research_product_analysis.py` | Deep-dive into product metadata |
| `04_organization_projects.py` | Organizations and their projects |
| `05_advanced_filtering.py` | Complex filter combinations |
| `06_persons_discovery.py` | Person search and co-authorship |
| `07_ergonomics_showcase.py` | Before/after: raw API vs ergonomics layer |
| `08_iterator_helpers.py` | `collect()`, `count()`, `first()` |
| `09_computed_fields_and_safe_types.py` | Computed properties and SafeStr/SafeList |
| `10_convenience_queries.py` | All convenience query functions |

See [`examples/README.md`](examples/README.md) for marimo embedding and WASM details.

## Known OpenAIRE API Issues

Full bug report with reproduction steps: [`OPENAIRE_BUG_REPORT.md`](OPENAIRE_BUG_REPORT.md).

- **Persons `givenName`/`lastName` filters** — cause HTTP 500 despite being in the spec
- **`pageSize=100`** on Links/Scholix — silently falls back to 10. Use `pageSize ≤ 99`
- **Undocumented endpoints** — Persons has no filtering docs; Links (`/v1/researchProducts/links`) is entirely undocumented
- **Sort field issues** — Persons only accepts `relevance`; Data Sources error messages say "organizations"

## Development

```bash
uv sync                  # install dev deps
uv run pytest -x -q      # run tests
uvx ruff check src/      # lint
uvx ty check src/        # type check
```

Pre-commit hooks for ruff format + lint are configured in `.pre-commit-config.yaml`.

Contributions welcome — see [Contributing](https://utsmok.github.io/AIREloom/contributing/).
