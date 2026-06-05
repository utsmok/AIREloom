# Projects

Projects represent funded research initiatives — EU Framework Programme grants, national funding calls, and more.

## Access

```python
async with AireloomSession() as session:
    client = session.projects  # ProjectsResource
```

## Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | Full-text search query |
| `title` | `str` | Project title |
| `keywords` | `list[str]` | Keywords |
| `acronym` | `str` | Project acronym |
| `code` | `str` | Project code or grant number |
| `grantID` | `str` | Grant identifier |
| `fundingShortName` | `str` | Funder short name (e.g. `EC`, `NSF`) |
| `fundingStreamId` | `str` | Funding stream identifier |
| `fromStartDate` | `date` | Start of start-date range |
| `toStartDate` | `date` | End of start-date range |
| `fromEndDate` | `date` | Start of end-date range |
| `toEndDate` | `date` | End of end-date range |
| `relOrganizationId` | `str` | Linked organization ID |
| `relOrganizationName` | `str` | Linked organization name |
| `relOrganizationCountryCode` | `str` | Linked organization country |

See the [full filter reference](../endpoints/projects.md) for all available fields. See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Sort Fields

`relevance`, `startDate`, `endDate`. Use `"field asc"` or `"field desc"`.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Project title |
| `acronym` | `str` | Short acronym |
| `code` | `str \| None` | Project code or grant number |
| `startDate` | `str \| None` | Start date (YYYY-MM-DD) |
| `endDate` | `str \| None` | End date (YYYY-MM-DD) |
| `fundings` | `SafeList[Funding]` | Funding sources with funder details |
| `granted` | `Grant` | Awarded grant amounts |
| `keywords` | `SafeList[str]` | Keywords |
| `summary` | `str` | Project abstract |
| `websiteUrl` | `str \| None` | Official website |
| `openAccessMandateForPublications` | `bool \| None` | OA mandate for publications |
| `openAccessMandateForDataset` | `bool \| None` | OA mandate for datasets |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `funder_name` | `str \| None` | First funder short name or name |
| `funder_jurisdiction` | `str \| None` | First funder jurisdiction |
| `start_year` | `int \| None` | Year parsed from `startDate` |
| `end_year` | `int \| None` | Year parsed from `endDate` |

See [Features](../ergonomics.md) for an overview of computed properties and `SafeList`.

## Linked Entities

Find research outputs linked to a project using `relProjectId`:

```python
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    outputs = await session.research_products.collect(
        filters=ResearchProductsFilters(relProjectId=project.id), limit=50,
    )
```
