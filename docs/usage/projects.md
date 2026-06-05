# Projects

Projects represent funded research initiatives — EU Framework Programme grants, national funding calls, and more. Use `session.projects` to discover projects, inspect funding details, and find linked research outputs.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import ProjectsFilters

async with AireloomSession() as session:
    response = await session.projects.search(
        filters=ProjectsFilters(fundingShortName="EC"),
        page_size=10,
    )
```

## Fetch a Single Project

```python
async with AireloomSession() as session:
    project = await session.projects.get(
        "corda_______::6b9e0c4e1e5e4a1e5c6b9e0c4e1e5e4a"
    )
    print(project.title)
    print(project.funder_name)
    print(project.code)
```

## Search with Filters

```python
from aireloom.endpoints import ProjectsFilters

filters = ProjectsFilters(
    search="machine learning",
    fundingShortName="EC",
    fromStartDate="2020-01-01",
    toStartDate="2024-12-31",
)

async with AireloomSession() as session:
    response = await session.projects.search(
        filters=filters, sort_by="startDate desc"
    )
    for project in response.results:
        print(f"{project.start_year} — {project.title[:60]}")
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | General keyword search |
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

See the [full filter reference](../endpoints/projects.md) for all available fields.

### Sort Fields

Projects support sorting by: `relevance`, `startDate`, `endDate`.

## Iterate Over Results

```python
from aireloom.endpoints import ProjectsFilters

filters = ProjectsFilters(fundingShortName="EC", fromStartDate="2023-01-01")

async with AireloomSession() as session:
    async for project in session.projects.iterate(
        filters=filters, sort_by="startDate desc"
    ):
        print(project.acronym, project.title[:50], project.funder_name)
```

## Model Overview

Each result is a `Project` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | OpenAIRE identifier |
| `title` | `str` | Project title |
| `acronym` | `str` | Short acronym |
| `code` | `str \| None` | Project code or grant number |
| `startDate` | `str \| None` | Start date (YYYY-MM-DD) |
| `endDate` | `str \| None` | End date (YYYY-MM-DD) |
| `fundings` | `SafeList[Funding]` | Funding sources with funder details |
| `granted` | `Grant` | Awarded grant amounts |
| `keywords` | `SafeList[str]` | Keywords |
| `summary` | `str` | Project abstract |
| `subjects` | `SafeList[str]` | Subject classifications |
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

All `SafeList` fields (`fundings`, `keywords`, `subjects`) default to an empty list — never `None`.

## Linked Entities

Find research outputs linked to a project using `relProjectId`:

```python
from aireloom.endpoints import ResearchProductsFilters

async with AireloomSession() as session:
    outputs = await session.research_products.collect(
        filters=ResearchProductsFilters(relProjectId=project.id),
        max_items=50,
    )
    for p in outputs:
        print(p.doi, p.mainTitle[:60])
```
