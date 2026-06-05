# Data Sources

Data sources represent repositories, journals, aggregators, and other platforms that provide research metadata to the OpenAIRE Graph.

## Access

```python
async with AireloomSession() as session:
    client = session.data_sources  # DataSourcesResource
```

## Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `officialName` | `str` | Official data source name |
| `englishName` | `str` | English name |
| `legalShortName` | `str` | Short name or acronym |
| `pid` | `str` | Persistent identifier |
| `subjects` | `list[str]` | Subject keywords |
| `dataSourceTypeName` | `str` | Type (e.g. `Journal`, `Repository`) |
| `contentTypes` | `list[str]` | Available content types |
| `relOrganizationId` | `str` | Linked organization ID |
| `relCommunityId` | `str` | Linked community ID |
| `relCollectedFromDatasourceId` | `str` | Collected-from data source ID |

See the [full filter reference](../endpoints/data_sources.md) for all available fields. See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Sort Fields

`relevance` only. Use `"relevance asc"` or `"relevance desc"`.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `officialName` | `str` | Official name |
| `englishName` | `str` | English name |
| `websiteUrl` | `str \| None` | Website URL |
| `type` | `ControlledField` | Type with `scheme` and `value` |
| `openaireCompatibility` | `str \| None` | OpenAIRE compatibility level |
| `subjects` | `SafeList[str]` | Subject keywords |
| `contentTypes` | `SafeList[str]` | Content types |
| `languages` | `SafeList[str]` | Supported languages |
| `pids` | `SafeList[ControlledField]` | Persistent identifiers |
| `journal` | `Container` | Journal metadata (if applicable) |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `type_name` | `str \| None` | Human-readable type value (e.g. `Journal`) |

See [Features](../ergonomics.md) for an overview of computed properties and `SafeList`.
