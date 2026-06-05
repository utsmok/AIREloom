# Ergonomics

AIREloom includes an ergonomics layer that makes working with OpenAIRE data safer and more Pythonic. It consists of three parts: safe types that eliminate `None` checks, computed properties that derive common values, and convenience functions that wrap common workflows into single calls.

## Safe Types

API responses often have missing fields. AIREloom uses two custom types to make traversal safe without constant `None` guards:

### SafeList[T]

A `list` that coerces `None` → `[]` and strips null entries. You can always iterate, index, and call `len()` without checking for `None` first.

```python
# These fields are never None — empty list instead
for author in product.authors:
    print(author.fullName)

# Safe to call len(), index, etc.
num_pids = len(product.pids)
first_pid = product.pids[0] if product.pids else None
```

### SafeStr

A `str` that coerces `None` → `""`. You can call any string method without guarding.

```python
# These fields are never None — empty string instead
product.mainTitle.upper()       # never crashes
product.description.split("\n") # works even if empty
```

Both types use Pydantic `BeforeValidator`, so coercion happens during model construction — not at access time.

## Computed Properties

Models expose `@computed_field` properties that derive commonly needed values from raw API data. These are available as regular attributes — no method calls needed.

```python
product = await session.research_products.get("openaire____::123")

product.doi               # → "10.1234/..." or None
product.is_open_access    # → True / False
product.publication_year  # → 2024 or None
```

### Full Reference

| Model | Property | Type | Description |
|---|---|---|---|
| `ResearchProduct` | `doi` | `str \| None` | First DOI from the `pids` list |
| `ResearchProduct` | `all_dois` | `list[str]` | All DOI values from `pids` |
| `ResearchProduct` | `is_open_access` | `bool` | `True` when best access right is OPEN |
| `ResearchProduct` | `open_access_url` | `str \| None` | URL of the first open access instance |
| `ResearchProduct` | `citation_count` | `int \| None` | Citation count from indicators |
| `ResearchProduct` | `publication_year` | `int \| None` | Year parsed from `publicationDate` |
| `ResearchProduct` | `journal_name` | `str \| None` | Container / journal name |
| `ResearchProduct` | `author_names` | `list[str]` | Non-empty full names of all authors |
| `ResearchProduct` | `license` | `str \| None` | First non-empty license across instances |
| `Person` | `orcid` | `str \| None` | ORCID extracted from `originalId` or `id` |
| `Person` | `full_name` | `str` | Concatenation of `givenName` and `familyName` |
| `Organization` | `ror_id` | `str \| None` | ROR identifier from `pids` |
| `Organization` | `country_code` | `str \| None` | Country code, `None` if UNKNOWN |
| `Project` | `funder_name` | `str \| None` | Short name or name of the first funder |
| `Project` | `funder_jurisdiction` | `str \| None` | Jurisdiction of the first funder |
| `Project` | `start_year` | `int \| None` | Year parsed from `startDate` |
| `Project` | `end_year` | `int \| None` | Year parsed from `endDate` |
| `DataSource` | `type_name` | `str \| None` | Value of the `type` controlled field |

### Example

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    product = await session.research_products.get("openaire____::doi:10.5281/zenodo.7664304")

    print(f"Title:   {product.mainTitle}")
    print(f"DOI:     {product.doi}")
    print(f"Year:    {product.publication_year}")
    print(f"Open:    {product.is_open_access}")
    print(f"Authors: {', '.join(product.author_names)}")
```

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/09_computed_fields_and_safe_types.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

## Convenience Queries

The `aireloom.queries` module provides single-call functions for common workflows. Access them via `session.queries` or import directly:

```python
from aireloom import AireloomSession
from aireloom.queries import publications_by_doi

async with AireloomSession() as session:
    papers = await publications_by_doi(session, "10.1038/s41586-024-07386-0")
```

### Available Functions

| Function | Description |
|---|---|
| `publications_by_doi(session, *dois)` | Fetch products matching one or more DOIs |
| `publications_by_organization(session, identifier)` | Fetch products from an organization |
| `publications_by_author(session, identifier)` | Fetch products by an author |
| `publications_by_project(session, identifier)` | Fetch products linked to a project |
| `count_publications(session, *, type, keywords, from_year, to_year)` | Count products matching criteria |
| `projects_by_organization(session, identifier)` | Fetch projects associated with an organization |
| `citing_works(session, doi)` | Fetch works that cite a given DOI (via Scholix) |
| `related_datasets(session, doi)` | Fetch datasets related to a publication DOI (via Scholix) |
| `all_links(session, doi)` | Fetch all Scholix links involving a DOI |

### Example

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    # Search by DOI
    papers = await session.queries.publications_by_doi(
        "10.1038/s41586-024-07386-0"
    )

    # Count publications on a topic
    n = await session.queries.count_publications(
        keywords="machine learning", from_year=2023
    )
    print(f"Found {n} publications")

    # Fetch citing works via Scholix
    citations = await session.queries.citing_works("10.1038/s41586-024-07386-0")
```

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/10_convenience_queries.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

## Iterator Helpers

Every resource endpoint (`session.research_products`, `session.organizations`, etc.) exposes three helper methods that wrap the async iterator into common collection patterns:

### `collect()`

Gather results into a plain list.

```python
from aireloom import AireloomSession
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    f = ResearchProductsFilters(keywords="machine learning")
    papers = await session.research_products.collect(filters=f, max_items=100)
    print(f"Collected {len(papers)} papers")
```

### `count()`

Return the total number of matching results (from the API response header).

```python
async with AireloomSession() as session:
    f = ResearchProductsFilters(keywords="climate change")
    total = await session.research_products.count(filters=f)
    print(f"{total} results match")
```

### `first()`

Return the first matching result, or `None` if there are no results.

```python
async with AireloomSession() as session:
    f = ResearchProductsFilters(keywords="quantum computing")
    top = await session.research_products.first(filters=f)
    if top:
        print(f"Top result: {top.mainTitle}")
```

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/08_iterator_helpers.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

## Before and After

Without the ergonomics layer, working with OpenAIRE data requires defensive checks everywhere:

```python
# Before — manual guards everywhere
if product.authors:
    for author in product.authors:
        if author.fullName:
            print(author.fullName)

doi = None
if product.pids:
    for pid in product.pids:
        if pid.scheme == "doi":
            doi = pid.value
            break
```

With the ergonomics layer, the same code is straightforward:

```python
# After — safe by default
for author in product.authors:        # SafeList: never None
    print(author.fullName)            # SafeStr: never None

doi = product.doi                     # computed property
```

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/07_ergonomics_showcase.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
