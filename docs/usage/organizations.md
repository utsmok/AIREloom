# Organizations

Organizations represent institutions — universities, research centers, companies — involved in research activities. Use `session.organizations` to search, filter, and explore organizational metadata and their linked entities.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import OrganizationsFilters

async with AireloomSession() as session:
    response = await session.organizations.search(
        filters=OrganizationsFilters(countryCode="NL"),
        page_size=10,
    )
```

## Fetch a Single Organization

```python
async with AireloomSession() as session:
    org = await session.organizations.get(
        "openaire____::b8b717c26e1d1bac00d2e1e7efda106b"
    )
    print(org.legalName)
    print(org.country_code)
```

## Search with Filters

```python
from aireloom.endpoints import OrganizationsFilters

filters = OrganizationsFilters(
    search="delft",
    countryCode="NL",
)

async with AireloomSession() as session:
    response = await session.organizations.search(
        filters=filters, sort_by="relevance desc"
    )
    for org in response.results:
        print(org.legalName, org.country_code)
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | General keyword search |
| `legalName` | `str` | Full legal name |
| `legalShortName` | `str` | Short name or acronym |
| `id` | `str` | OpenAIRE identifier |
| `pid` | `str` | Persistent identifier (ROR, etc.) |
| `countryCode` | `str` | Two-letter country code |
| `relCommunityId` | `str` | Linked community ID |
| `relCollectedFromDatasourceId` | `str` | Collected-from data source ID |

See the [full filter reference](../endpoints/organizations.md) for all available fields.

### Sort Fields

Organizations support sorting by: `relevance`.

## Iterate Over Results

```python
from aireloom.endpoints import OrganizationsFilters

filters = OrganizationsFilters(countryCode="DE")

async with AireloomSession() as session:
    async for org in session.organizations.iterate(filters=filters):
        print(org.legal_name, org.country_code, org.ror_id)
```

## Model Overview

Each result is an `Organization` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | OpenAIRE identifier |
| `legalName` | `str` | Full legal name |
| `legalShortName` | `str` | Short name or acronym |
| `alternativeNames` | `SafeList[str]` | Other known names |
| `websiteUrl` | `str \| None` | Official website |
| `country` | `Country` | Country with `code` and `label` |
| `pids` | `SafeList[OrganizationPid]` | Persistent identifiers (ROR, etc.) |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `country_code` | `str \| None` | Country code (excludes `UNKNOWN`) |
| `legal_name` | — | Available directly as `legalName` field |
| `ror_id` | `str \| None` | ROR identifier from the `pids` list |

All `SafeList` fields (`alternativeNames`, `pids`) default to an empty list — never `None`.

## Linked Entities

To find research products, projects, or data sources linked to an organization, use the `relOrganizationId` filter on other endpoints:

```python
from aireloom.endpoints import ResearchProductsFilters, ProjectsFilters

async with AireloomSession() as session:
    products = await session.research_products.collect(
        filters=ResearchProductsFilters(relOrganizationId=org.id),
        max_items=20,
    )
    projects = await session.projects.collect(
        filters=ProjectsFilters(relOrganizationId=org.id),
        max_items=20,
    )
```

## Example Notebook

<iframe src="https://marimo.app/gh/utsmok/AIREloom/main/examples/04_organization_projects.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
