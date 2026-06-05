# Research Product Links

Discover **relationships between research products** within the OpenAIRE Graph — citations, supplements, versions, and more.

!!! info "v1-only endpoint"
    This endpoint is only available on the v1 API. AIREloom routes it automatically.

## Access

Links are part of the Research Products client — no separate client is needed:

```python
async with AireloomSession() as session:
    await session.research_products.search_links(
        filters=LinksFilters(sourcePid="10.1234/example")
    )
```

## Filter Reference

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

See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Key Fields

Each link is a `Relation` instance:

| Field | Type | Description |
|-------|------|-------------|
| `source` | `Node \| None` | Source entity |
| `target` | `Node \| None` | Target entity |
| `relType` | `RelType \| None` | Relationship type with `name`, `type`, `typeSchema` |

### Node Fields

Each `Node` (source or target) contains:

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Entity title |
| `type` | `str \| None` | Entity type |
| `publicationDate` | `str \| None` | Publication date |
| `identifiers` | `SafeList[Identifier]` | PIDs with `id`, `idScheme`, `idUrl` |
| `authors` | `SafeList[EntityRef]` | Author names with identifiers |

See [Features](../ergonomics.md) for an overview of `SafeList`.

## Getting Relation Types

Discover which relationship types the API supports:

```python
async with AireloomSession() as session:
    relation_types = await session.research_products.get_relations_info()
```

## Links vs Scholix

AIREloom provides two link-discovery mechanisms:

- **Graph Links** (this page) — Relationships between research products **within** the OpenAIRE Graph. Accessed via `session.research_products.search_links()`.
- **Scholix** — Cross-platform scholarly links from the Scholexplorer service. Accessed via `session.scholix`. Best for discovering dataset–publication relationships across external repositories.
