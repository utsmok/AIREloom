# Features

AIREloom adds convenience features on top of the raw OpenAIRE API responses: safe field access, computed properties, and one-call query functions.

## Safe Field Access

API responses often have missing fields. AIREloom ensures common field types never return `None`:

- **List fields** (`authors`, `pids`, `subjects`, `instances`, etc.) always return a list — empty instead of `None`
- **String fields** (`mainTitle`, `description`, etc.) always return a string — empty instead of `None`

```python
# Iterate without null checks
for author in product.authors:       # always a list
    print(author.fullName)           # always a string

# String methods just work
product.mainTitle.upper()            # safe even if empty

# len(), indexing, etc. — no guards needed
num_pids = len(product.pids)
```

## Computed Properties

Models expose derived attributes for commonly needed values. No method calls — just access them like regular fields:

```python
product.doi               # "10.1234/..." or None
product.is_open_access    # True / False
product.publication_year  # 2024 or None
```

### Reference

| Model | Property | Returns | Description |
|---|---|---|---|
| `ResearchProduct` | `doi` | `str \| None` | First DOI from `pids` |
| `ResearchProduct` | `all_dois` | `list[str]` | All DOI values |
| `ResearchProduct` | `is_open_access` | `bool` | Best access right is OPEN |
| `ResearchProduct` | `open_access_url` | `str \| None` | URL of first open access instance |
| `ResearchProduct` | `citation_count` | `int \| None` | Citation count from indicators |
| `ResearchProduct` | `publication_year` | `int \| None` | Year from `publicationDate` |
| `ResearchProduct` | `journal_name` | `str \| None` | Container / journal name |
| `ResearchProduct` | `author_names` | `list[str]` | Non-empty full names |
| `ResearchProduct` | `license` | `str \| None` | First license across instances |
| `Person` | `orcid` | `str \| None` | ORCID from `originalId` or `id` |
| `Person` | `full_name` | `str` | `givenName` + `familyName` |
| `Organization` | `ror_id` | `str \| None` | ROR identifier |
| `Organization` | `country_code` | `str \| None` | Country code |
| `Project` | `funder_name` | `str \| None` | First funder short name |
| `Project` | `funder_jurisdiction` | `str \| None` | First funder jurisdiction |
| `Project` | `start_year` | `int \| None` | Year from `startDate` |
| `Project` | `end_year` | `int \| None` | Year from `endDate` |
| `DataSource` | `type_name` | `str \| None` | Controlled type value |

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/09_computed_fields_and_safe_types.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

## Convenience Queries

`session.queries` exposes nine pre-built functions for common research workflows:

| Function | Description |
|---|---|
| `publications_by_doi(*dois)` | Fetch products matching DOIs |
| `publications_by_organization(id)` | Products from an organization |
| `publications_by_author(id)` | Products by author name or ORCID |
| `publications_by_project(id)` | Products linked to a project |
| `count_publications(...)` | Count without downloading |
| `projects_by_organization(id)` | Projects for an organization |
| `citing_works(doi)` | Works citing a DOI (Scholix) |
| `related_datasets(doi)` | Datasets linked to a DOI (Scholix) |
| `all_links(doi)` | All Scholix links for a DOI |

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    papers = await session.queries.publications_by_doi("10.1038/s41586-024-07386-0")
    n = await session.queries.count_publications(keywords="machine learning", from_year=2023)
    citations = await session.queries.citing_works("10.1038/s41586-024-07386-0")
```

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/10_convenience_queries.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

## Iterator Helpers

Every resource client provides three helpers on top of `iterate()`:

```python
async with AireloomSession() as session:
    # Collect into a list
    papers = await session.research_products.collect(filters=f, max_items=100)

    # Count without downloading
    total = await session.research_products.count(filters=f)

    # Grab the top result
    top = await session.research_products.first(filters=f)
```

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/08_iterator_helpers.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
