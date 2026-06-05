# Research Products

Research products are the core entities in the OpenAIRE Graph — publications, datasets, software, and other research outputs.

## Access

```python
async with AireloomSession() as session:
    client = session.research_products  # ResearchProductsResource
```

## Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | Full-text search query |
| `type` | `str` | `publication`, `dataset`, `software`, `other` |
| `mainTitle` | `str` | Filter by main title |
| `pid` | `str` | Persistent identifier (e.g. DOI) |
| `fromPublicationDate` | `date` | Start of publication date range |
| `toPublicationDate` | `date` | End of publication date range |
| `subjects` | `list[str]` | Subject keywords |
| `countryCode` | `str` | Two-letter country code |
| `authorFullName` | `str` | Author full name |
| `authorOrcid` | `str` | Author ORCID |
| `publisher` | `str` | Publisher name |
| `bestOpenAccessRightLabel` | `str` | Access right label (e.g. `OPEN`) |
| `isPeerReviewed` | `bool` | Peer-reviewed only |
| `relProjectId` | `str` | Linked project OpenAIRE ID |
| `relOrganizationId` | `str` | Linked organization OpenAIRE ID |

See the [full filter reference](../endpoints/research_products.md) for all available fields. See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Sort Fields

`relevance`, `publicationDate`, `dateOfCollection`, `influence`, `citationCount`, `impulse`. Use `"field asc"` or `"field desc"`.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `mainTitle` | `str` | Primary title |
| `type` | `str` | `publication`, `dataset`, `software`, `other` |
| `publicationDate` | `str` | Publication date (YYYY-MM-DD) |
| `pids` | `SafeList[Pid]` | Persistent identifiers (DOI, Handle, etc.) |
| `authors` | `SafeList[Author]` | Author list with `fullName`, `orcid` |
| `bestAccessRight` | `BestAccessRight` | Best available access status |
| `indicators` | `Indicator` | Citation counts, usage metrics |
| `instances` | `SafeList[Instance]` | Hosted versions with URLs and licenses |
| `subjects` | `SafeList[Subject]` | Subject classifications |
| `container` | `Container` | Journal or book series info |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `doi` | `str \| None` | First DOI from the `pids` list |
| `all_dois` | `list[str]` | All DOI values |
| `is_open_access` | `bool` | `True` when best access right is OPEN |
| `open_access_url` | `str \| None` | URL of the first open access instance |
| `publication_year` | `int \| None` | Year parsed from `publicationDate` |
| `citation_count` | `int \| None` | Citation count from indicators |
| `journal_name` | `str \| None` | Container/journal name |
| `author_names` | `list[str]` | Non-empty full names of all authors |
| `license` | `str \| None` | First license found across instances |

See [Features](../ergonomics.md) for an overview of computed properties and `SafeList`.

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/03_research_product_analysis.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
