# Basic Usage

The patterns below work identically for every entity type. After reading this page, see the per-entity guides for type-specific fields and filters.

## Creating a session

All API access goes through a session. Use it as an async context manager:

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    ...
```

You can also use `AireloomClient` directly -- it gives the same resource properties but without the convenience query layer:

```python
from aireloom import AireloomClient

async with AireloomClient() as client:
    ...
```

Pick one. `AireloomSession` wraps `AireloomClient` and adds `session.queries` (convenience functions). Both support `async with`.

## Resource clients

Every session exposes a property per entity type:

| Property | Client | Entity |
|---|---|---|
| `session.research_products` | `ResearchProductsClient` | Research products |
| `session.projects` | `ProjectsClient` | Projects |
| `session.organizations` | `OrganizationsClient` | Organizations |
| `session.data_sources` | `DataSourcesClient` | Data sources |
| `session.persons` | `PersonsClient` | Persons |
| `session.scholix` | `ScholixClient` | Scholix links |

Every client above (except `ScholixClient`) supports the same five operations.

## Common operations

### `search()` -- paginated response

Returns a response object with `.results` (list of entities) and `.header` (pagination metadata).

```python
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    response = await session.research_products.search(
        filters=ResearchProductsFilters(search="machine learning", type="publication"),
        page=1,
        page_size=10,
        sort_by="publicationDate desc",
    )
    for product in response.results:
        print(product.mainTitle)
```

### `get()` -- single entity by ID

```python
async with AireloomSession() as session:
    product = await session.research_products.get("doi_________::abc123")
    print(product.mainTitle)
```

### `iterate()` -- async generator with cursor pagination

Yields entities one at a time. Handles paging automatically.

```python
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    filters = ResearchProductsFilters(type="dataset", fromPublicationDate="2024-01-01")
    async for dataset in session.research_products.iterate(filters=filters):
        print(dataset.mainTitle)
```

### `collect()` -- gather into a list

Like `iterate()` but collects results into a list. Use `limit` to cap the count.

```python
products = await session.research_products.collect(
    filters=ResearchProductsFilters(type="publication"),
    limit=50,
)
```

### `count()` -- total matching entities

```python
total = await session.research_products.count(
    filters=ResearchProductsFilters(search="open science"),
)
print(f"Found {total} results")
```

### `first()` -- first match or None

```python
product = await session.research_products.first(
    filters=ResearchProductsFilters(search="zenodo.7664304"),
)
```

## Filters

Filters are Pydantic models with `extra='forbid'` -- invalid fields raise a validation error. Each entity type has its own filters class:

| Filters class | Entity |
|---|---|
| `ResearchProductsFilters` | Research products |
| `ProjectsFilters` | Projects |
| `OrganizationsFilters` | Organizations |
| `DataSourcesFilters` | Data sources |
| `PersonsFilters` | Persons |
| `ScholixFilters` | Scholix links |

```python
from aireloom.endpoints import ProjectsFilters

filters = ProjectsFilters(
    search="horizon europe",
    fundingStream="Horizon Europe",
    fromStartDate="2021-01-01",
)
```

Import from `aireloom.endpoints`:

```python
from aireloom.endpoints import ResearchProductsFilters, ProjectsFilters, OrganizationsFilters
```

See the [Endpoints reference](endpoints/research_products.md) for all available filter fields per entity.

## Computed properties

Models provide computed properties beyond what the raw API returns. For research products:

```python
product.doi              # first DOI from pids list
product.is_open_access   # bool: bestAccessRight is OPEN
product.open_access_url  # first open access instance URL
product.citation_count   # from indicators
product.publication_year # parsed from publicationDate
product.journal_name     # container name
product.author_names     # list of author full names
product.license          # first license from instances
```

See per-entity pages for the full list of computed properties per model.

## Safe types

All models use `SafeList` and `SafeStr` annotated types. These coerce `None` to safe defaults:

- `SafeList[T]` -- `None` becomes `[]`, null elements are stripped
- `SafeStr` -- `None` becomes `""`

This means you never need None guards:

```python
# These never crash, even if the API returns null
for pid in product.pids:
    print(pid.value)

print(product.mainTitle.upper())
```

Nested models use the same pattern (`SafeBestAccessRight`, `SafeContainer`, etc.) -- `None` is replaced with an empty default instance.
