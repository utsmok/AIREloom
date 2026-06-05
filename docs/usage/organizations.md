# Organizations

Organizations represent institutions — universities, research centers, companies — involved in research activities.

## Access

```python
async with AireloomSession() as session:
    client = session.organizations  # OrganizationsResource
```

## Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | Full-text search query |
| `legalName` | `str` | Full legal name |
| `legalShortName` | `str` | Short name or acronym |
| `pid` | `str` | Persistent identifier (ROR, etc.) |
| `countryCode` | `str` | Two-letter country code |
| `relCommunityId` | `str` | Linked community ID |
| `relCollectedFromDatasourceId` | `str` | Collected-from data source ID |

See the [full filter reference](../endpoints/organizations.md) for all available fields. See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Sort Fields

`relevance` only. Use `"relevance asc"` or `"relevance desc"`.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
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
| `ror_id` | `str \| None` | ROR identifier from the `pids` list |

See [Features](../ergonomics.md) for an overview of computed properties and `SafeList`.

## Linked Entities

To find research products or projects linked to an organization, use the `relOrganizationId` filter on other endpoints:

```python
from aireloom.endpoints import ResearchProductsFilters, ProjectsFilters

async with AireloomSession() as session:
    products = await session.research_products.collect(
        filters=ResearchProductsFilters(relOrganizationId=org.id), limit=20,
    )
    projects = await session.projects.collect(
        filters=ProjectsFilters(relOrganizationId=org.id), limit=20,
    )
```

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/04_organization_projects.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
