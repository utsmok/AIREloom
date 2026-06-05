# Getting Started

AIREloom is an async Python client for the OpenAIRE Graph API. This page walks you through installation, authentication, and your first queries.

## Install

See the [Installation Guide](installation.md) for full details. The short version:

```bash
pip install aireloom
```

## Authentication

AIREloom defaults to public access — no credentials required for querying open data. For authenticated access (higher rate limits, protected resources), see the [Authentication Guide](authentication.md).

## Examples

### Fetch a research product by DOI

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    product = await session.queries.search_by_doi("10.5281/zenodo.7664304")
    print(product.mainTitle)
    print(product.doi)
```

### Search publications about a topic

```python
from aireloom import AireloomSession
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    filters = ResearchProductsFilters(search="machine learning", type="publication")
    results = await session.research_products.search(filters=filters, page_size=10)
    for product in results.results:
        print(product.mainTitle)
```

### Iterate all matching results

```python
from aireloom import AireloomSession
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    filters = ResearchProductsFilters(type="dataset", fromPublicationDate="2024-01-01")
    async for dataset in session.research_products.iterate(filters=filters):
        print(dataset.mainTitle)
```

## Ergonomics

AIREloom includes an ergonomics layer that makes everyday queries simpler:

- **Computed properties** — `product.doi`, `product.is_open_access`, `product.citation_class` and more, derived from the raw API response
- **Convenience queries** — `session.queries.search_by_doi(...)`, `session.queries.search_publications(...)` for common lookups
- **Iterator helpers** — `.collect(max_items=100)`, `.count()`, `.first()` on every resource client

See the [Ergonomics](ergonomics.md) page for the full reference.

## Next Steps

Explore the detailed usage guides for each entity type:

- [Research Products](usage/research_products.md)
- [Projects](usage/projects.md)
- [Organizations](usage/organizations.md)
- [Data Sources](usage/data_sources.md)
- [Scholix Links](usage/scholix.md)
