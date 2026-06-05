# Data Sources

Data sources in OpenAIRE represent repositories, journals, aggregators, and other platforms that provide research metadata. Use `session.data_sources` to discover and inspect them.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import DataSourcesFilters

async with AireloomSession() as session:
    response = await session.data_sources.search(
        filters=DataSourcesFilters(dataSourceTypeName="Journal"),
        page_size=10,
    )
```

## Fetch a Single Data Source

```python
async with AireloomSession() as session:
    ds = await session.data_sources.get("openaire____::4691ea4e28928e5bf3e809d0d3a0e8b0")
    print(ds.officialName)
    print(ds.type_name)
```

## Search with Filters

```python
from aireloom.endpoints import DataSourcesFilters

filters = DataSourcesFilters(
    search="zenodo",
    dataSourceTypeName="Journal",
)

async with AireloomSession() as session:
    response = await session.data_sources.search(
        filters=filters, sort_by="relevance desc"
    )
    for ds in response.results:
        print(ds.officialName, ds.type_name)
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | General keyword search |
| `officialName` | `str` | Official data source name |
| `englishName` | `str` | English name |
| `legalShortName` | `str` | Short name or acronym |
| `id` | `str` | OpenAIRE identifier |
| `pid` | `str` | Persistent identifier |
| `subjects` | `list[str]` | Subject keywords |
| `dataSourceTypeName` | `str` | Type (e.g. `Journal`, `Repository`) |
| `contentTypes` | `list[str]` | Available content types |
| `relOrganizationId` | `str` | Linked organization ID |
| `relCommunityId` | `str` | Linked community ID |
| `relCollectedFromDatasourceId` | `str` | Collected-from data source ID |

See the [full filter reference](../endpoints/data_sources.md) for all available fields.

### Sort Fields

Data sources support sorting by: `relevance`.

## Iterate Over Results

```python
from aireloom.endpoints import DataSourcesFilters

filters = DataSourcesFilters(dataSourceTypeName="Aggregator")

async with AireloomSession() as session:
    async for ds in session.data_sources.iterate(filters=filters):
        print(ds.officialName, ds.websiteUrl)
```

## Model Overview

Each result is a `DataSource` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | OpenAIRE identifier |
| `officialName` | `str` | Official name |
| `englishName` | `str` | English name |
| `websiteUrl` | `str \| None` | Website URL |
| `type` | `ControlledField` | Type with `scheme` and `value` |
| `openaireCompatibility` | `str \| None` | OpenAIRE compatibility level |
| `description` | `str` | Description text |
| `subjects` | `SafeList[str]` | Subject keywords |
| `contentTypes` | `SafeList[str]` | Content types |
| `languages` | `SafeList[str]` | Supported languages |
| `pids` | `SafeList[ControlledField]` | Persistent identifiers |
| `journal` | `Container` | Journal metadata (if applicable) |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `type_name` | `str \| None` | Human-readable type value (e.g. `Journal`) |

All `SafeList` fields (`subjects`, `contentTypes`, `languages`, etc.) default to an empty list — never `None`.
