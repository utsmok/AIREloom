# Research Product Links

The Links endpoint discovers **relationships between research products** within the OpenAIRE Graph — citations, supplements, versions, and more. It is accessed through `session.research_products` using dedicated link methods.

## Accessing the Client

Links are part of the Research Products client. No separate client is needed:

```python
from aireloom import AireloomSession
from aireloom.endpoints import LinksFilters

async with AireloomSession() as session:
    response = await session.research_products.search_links(
        filters=LinksFilters(sourcePid="10.1234/example")
    )
```

## Search for Links

Find relationships between research products by source/target identifiers, types, or publishers:

```python
from aireloom.endpoints import LinksFilters

filters = LinksFilters(
    sourcePid="10.1038/s41586-020-2649-2",
    sourceType="publication",
)

async with AireloomSession() as session:
    response = await session.research_products.search_links(filters=filters)
    for rel in response.results:
        source = rel.source.title[:50] if rel.source else "?"
        target = rel.target.title[:50] if rel.target else "?"
        print(f"{source} → {target}")
```

## Iterate Over Links

Auto-paginate through all matching links:

```python
from aireloom.endpoints import LinksFilters

filters = LinksFilters(targetType="dataset")

async with AireloomSession() as session:
    async for rel in session.research_products.iterate_links(filters=filters):
        if rel.source and rel.target:
            print(rel.source.title[:40], "→", rel.target.title[:40])
```

## Get Available Relation Types

Discover which relationship types the API supports:

```python
async with AireloomSession() as session:
    relation_types = await session.research_products.get_relations_info()
    for rt in relation_types:
        print(rt)
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `sourcePid` | `str` | Source persistent identifier (e.g. DOI) |
| `targetPid` | `str` | Target persistent identifier |
| `sourcePublisher` | `str` | Source publisher name |
| `targetPublisher` | `str` | Target publisher name |
| `sourceType` | `str` | `publication`, `dataset`, `software`, `other` |
| `targetType` | `str` | Target entity type |
| `relation` | `str` | Relationship type name |
| `fromDate` | `str` | Start date (YYYY or YYYY-MM-DD) |
| `toDate` | `str` | End date (YYYY or YYYY-MM-DD) |

## Model Overview

Each link is a `Relation` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `source` | `Node \| None` | Source entity with `title`, `type`, `identifiers`, `authors` |
| `target` | `Node \| None` | Target entity |
| `relType` | `RelType \| None` | Relationship type with `name`, `type`, `typeSchema` |

### Node Fields

Each `Node` (source or target) contains:

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Entity title |
| `type` | `str \| None` | Entity type |
| `instanceType` | `str \| None` | Instance type |
| `publicationDate` | `str \| None` | Publication date |
| `identifiers` | `SafeList[Identifier]` | PIDs with `id`, `idScheme`, `idUrl` |
| `authors` | `SafeList[EntityRef]` | Author names with identifiers |
| `collectedFrom` | `SafeList[EntityRef]` | Source data sources |

All `SafeList` fields (`identifiers`, `authors`, `collectedFrom`) default to an empty list — never `None`.

## Links vs Scholix

AIREloom provides two link-discovery mechanisms:

- **Graph Links** (this page) — Relationships between research products **within** the OpenAIRE Graph. Accessed via `session.research_products.search_links()`.
- **Scholix** — Cross-platform scholarly links from the Scholexplorer service. Accessed via `session.scholix`. Best for discovering dataset–publication relationships across external repositories.
