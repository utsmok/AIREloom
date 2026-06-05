# Scholix (Scholarly Link Discovery)

Scholix is a separate API from the main OpenAIRE Graph — it discovers relationships (links) between scholarly objects such as publications, datasets, and software. Use `session.scholix` to explore how research outputs cite, supplement, or reference each other.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import ScholixFilters

async with AireloomSession() as session:
    response = await session.scholix.search_links(
        filters=ScholixFilters(sourcePid="10.1234/test")
    )
```

The Scholix client connects to the Scholexplorer API (a different base URL from the main Graph API). No separate configuration is needed — `AireloomSession` routes Scholix calls automatically.

## Search for Links

Search for relationships involving a specific DOI, publisher, or entity type:

```python
from aireloom.endpoints import ScholixFilters

filters = ScholixFilters(
    sourcePid="10.1038/s41586-020-2649-2",
    sourceType="Publication",
)

async with AireloomSession() as session:
    response = await session.scholix.search_links(filters=filters)
    print(f"Total links: {response.total_links}")
    for link in response.result:
        print(link.source.objectType, "→", link.target.objectType)
```

## Iterate Over Links

For large result sets, use `iterate_links()` to auto-paginate:

```python
from aireloom.endpoints import ScholixFilters

filters = ScholixFilters(
    targetType="Dataset",
    relation="IsReferencedBy",
)

async with AireloomSession() as session:
    async for link in session.scholix.iterate_links(filters=filters):
        print(link.source.title[:50], "→", link.target.title[:50])
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `sourcePid` | `str` | Source persistent identifier (DOI, etc.) |
| `targetPid` | `str` | Target persistent identifier |
| `sourcePublisher` | `str` | Source publisher name |
| `targetPublisher` | `str` | Target publisher name |
| `sourceType` | `str` | Source type: `Publication`, `Dataset`, `Software`, `Other` |
| `targetType` | `str` | Target type |
| `relation` | `str` | Relationship type (e.g. `IsReferencedBy`, `IsSupplementedBy`) |
| `from_date` | `date` | Start of link date range |
| `to_date` | `date` | End of link date range |

## Model Overview

Each link is a `ScholixRelationship` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `source` | `ScholixEntity` | Source entity with `title`, `objectType`, `identifier` |
| `target` | `ScholixEntity` | Target entity with `title`, `objectType`, `identifier` |
| `relationship_type` | `ScholixRelationshipType` | Relation name and schema |
| `link_provider` | `list[ScholixLinkProvider]` | Who provided this link |
| `link_publication_date` | `datetime \| None` | When the link was published |
| `harvest_date` | `str \| None` | Last harvest date |

### ScholixEntity Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Entity title |
| `objectType` | `str` | `Publication`, `Dataset`, `Software`, `Other` |
| `identifier` | `list[ScholixIdentifier]` | PIDs with `scheme` and `value` |
| `creator` | `list[ScholixCreator]` | Authors/creators |
| `publisher` | `list[ScholixPublisher]` | Publishers |

## Scholix vs Graph Links

AIREloom provides two distinct link-discovery mechanisms:

- **Scholix** (`session.scholix`) — Cross-platform scholarly links from the Scholexplorer service. Best for discovering dataset-publication, software-publication relationships across repositories.
- **Graph Links** (`session.research_products.search_links`) — Links from the OpenAIRE Graph between research products. Best for intra-Graph relationship discovery.

## Example Notebook

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/02_scholix_link_discovery.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
