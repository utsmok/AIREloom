# Research Products

Research products are the core entities in the OpenAIRE Graph — publications, datasets, software, and other research outputs. AIREloom provides full access to search, filter, iterate, and inspect these products through `session.research_products`.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    products = await session.research_products.search(
        filters=ResearchProductsFilters(type="publication"),
        page_size=10,
    )
```

## Fetch a Single Product

Retrieve a research product by its OpenAIRE ID:

```python
async with AireloomSession() as session:
    product = await session.research_products.get(
        "doi_dedup___::7f1d8b0a6e13b2a4d4d9c7dab9e2c5d1"
    )
    print(product.mainTitle)
    print(product.doi)
```

## Search with Filters

Use `ResearchProductsFilters` to narrow results. Combine with sorting and pagination:

```python
from aireloom.endpoints import ResearchProductsFilters

filters = ResearchProductsFilters(
    type="publication",
    fromPublicationDate="2024-01-01",
    bestOpenAccessRightLabel="OPEN",
    isPeerReviewed=True,
)

async with AireloomSession() as session:
    response = await session.research_products.search(
        filters=filters,
        page=1,
        page_size=10,
        sort_by="publicationDate desc",
    )
    for product in response.results:
        print(f"{product.publication_year} — {product.mainTitle}")
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | General keyword search |
| `mainTitle` | `str` | Filter by main title |
| `type` | `str` | `publication`, `dataset`, `software`, `other` |
| `pid` | `str` | Persistent identifier (e.g. DOI) |
| `fromPublicationDate` | `date` | Start of publication date range |
| `toPublicationDate` | `date` | End of publication date range |
| `subjects` | `list[str]` | Subject keywords |
| `countryCode` | `str` | Two-letter country code |
| `authorFullName` | `str` | Author full name |
| `authorOrcid` | `str` | Author ORCID |
| `publisher` | `str` | Publisher name |
| `bestOpenAccessRightLabel` | `str` | Access right label (e.g. `OPEN`) |
| `isPeerReviewed` | `bool` | Peer-reviewed only |
| `relProjectId` | `str` | Linked project OpenAIRE ID |
| `relOrganizationId` | `str` | Linked organization OpenAIRE ID |

See the [full filter reference](../endpoints/research_products.md) for all available fields.

### Sort Fields

Research products support sorting by: `relevance`, `publicationDate`, `dateOfCollection`, `influence`, `citationCount`, `impulse`. Use `"field asc"` or `"field desc"`.

## Iterate Over Results

For large result sets, use `iterate()` which handles cursor-based pagination automatically:

```python
from aireloom.endpoints import ResearchProductsFilters

filters = ResearchProductsFilters(
    type="dataset", subject="climate", fromPublicationDate="2023-01-01"
)

async with AireloomSession() as session:
    async for product in session.research_products.iterate(
        filters=filters, sort_by="publicationDate desc"
    ):
        print(product.doi, product.mainTitle)
```

### Iterator Helpers

Collect, count, or grab the first result without manual loops:

```python
async with AireloomSession() as session:
    products = await session.research_products.collect(
        filters=filters, max_items=50
    )
    total = await session.research_products.count(filters=filters)
    first = await session.research_products.first(filters=filters)
```

## Model Overview

Each result is a `ResearchProduct` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | OpenAIRE identifier |
| `mainTitle` | `str` | Primary title |
| `type` | `str` | `publication`, `dataset`, `software`, `other` |
| `publicationDate` | `str` | Publication date (YYYY-MM-DD) |
| `publisher` | `str` | Publisher name |
| `pids` | `SafeList[Pid]` | Persistent identifiers (DOI, Handle, etc.) |
| `authors` | `SafeList[Author]` | Author list with `fullName`, `orcid` |
| `bestAccessRight` | `BestAccessRight` | Best available access status |
| `indicators` | `Indicator` | Citation counts, usage metrics |
| `instances` | `SafeList[Instance]` | Hosted versions with URLs and licenses |
| `subjects` | `SafeList[Subject]` | Subject classifications |
| `container` | `Container` | Journal or book series info |
| `language` | `Language` | Primary language |

## Computed Properties

The `ResearchProduct` model provides convenience properties that extract common values without manual traversal:

| Property | Return | Description |
|----------|--------|-------------|
| `doi` | `str \| None` | First DOI from the `pids` list |
| `all_dois` | `list[str]` | All DOI values |
| `is_open_access` | `bool` | `True` when best access right is OPEN |
| `open_access_url` | `str \| None` | URL of the first open access instance |
| `publication_year` | `int \| None` | Year parsed from `publicationDate` |
| `citation_count` | `int \| None` | Citation count from indicators |
| `journal_name` | `str \| None` | Container/journal name |
| `author_names` | `list[str]` | Non-empty full names of all authors |
| `license` | `str \| None` | First license found across instances |

All `SafeList` fields (`authors`, `pids`, `subjects`, `instances`, etc.) never return `None` — they default to an empty list, so you can iterate safely without null checks.

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/03_research_product_analysis.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
