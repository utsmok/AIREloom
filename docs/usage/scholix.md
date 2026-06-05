# Scholix (Scholarly Link Discovery)

Scholix discovers relationships (links) between scholarly objects — publications, datasets, and software — using the **Scholexplorer API**, a separate service from the main OpenAIRE Graph API. No separate configuration is needed — `AireloomSession` routes Scholix calls automatically.

## Access

```python
async with AireloomSession() as session:
    client = session.scholix  # ScholixResource
```

## Filter Reference

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

See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

!!! note "Different API"
    Scholix uses the Scholexplorer API, not the Graph API. Methods are `search_links` / `iterate_links` instead of `search` / `iterate`.

## Key Fields

Each link is a `ScholixRelationship` instance:

| Field | Type | Description |
|-------|------|-------------|
| `source` | `ScholixEntity` | Source entity |
| `target` | `ScholixEntity` | Target entity |
| `relationship_type` | `ScholixRelationshipType` | Relation name and schema |
| `link_provider` | `list[ScholixLinkProvider]` | Who provided this link |
| `link_publication_date` | `datetime \| None` | When the link was published |

### ScholixEntity Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Entity title |
| `objectType` | `str` | `Publication`, `Dataset`, `Software`, `Other` |
| `identifier` | `list[ScholixIdentifier]` | PIDs with `scheme` and `value` |
| `creator` | `list[ScholixCreator]` | Authors/creators |
| `publisher` | `list[ScholixPublisher]` | Publishers |

## Scholix vs Graph Links

- **Scholix** (`session.scholix`) — Cross-platform scholarly links from Scholexplorer. Best for discovering dataset–publication, software–publication relationships across repositories.
- **Graph Links** (`session.research_products.search_links`) — Links from the OpenAIRE Graph between research products. Best for intra-Graph relationship discovery.

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/02_scholix_link_discovery.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
