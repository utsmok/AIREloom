# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "aireloom",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        """
    > 💡 **Switch to code view with Ctrl+. to see all code cells**

    # Computed Fields & Safe Types

    AIREloom models include **computed properties** that eliminate boilerplate
    (null-checking, nested navigation, manual extraction) and **safe types**
    (`SafeStr`, `SafeList`) that default to `""` and `[]` instead of `None`.

    This notebook demonstrates every computed field and safe type across all
    entity models.
"""
    )


@app.cell
async def _():
    from aireloom import AireloomClient
    from aireloom.endpoints import (
        ResearchProductsFilters,
    )

    client = AireloomClient()
    return AireloomClient, ResearchProductsFilters, client


@app.cell
async def _(ResearchProductsFilters, client, mo):
    papers = await client.research_products.collect(
        filters=ResearchProductsFilters(pid="10.1038/s41586-024-07386-0"),
        limit=1,
    )
    paper = papers[0]
    mo.md(f"**Fetched paper:** {paper}")
    return paper, papers


@app.cell
def _(mo, paper):
    mo.md(
        """
## Safe Types — No More None Checks

**SafeStr** (`title`, `description`, …) is always a `str`, never `None`.
**SafeList** (`authors`, `keywords`, `pids`, …) is always a `list`, never `None`.

You can iterate, call `.upper()`, check `len()` — no guards needed.
"""
    )


@app.cell
def _(mo, paper):
    mo.md(
        f"""
| Field | Type | Value | Works without guard? |
|---|---|---|---|
| `paper.title` | `SafeStr` | `{paper.title[:60]!r}` | ✅ always `str` |
| `paper.authors` | `SafeList` | `list` with `{len(paper.authors)}` items | ✅ always `list` |
| `paper.keywords` | `SafeList` | `{paper.keywords[:3]}` | ✅ always `list` |
| `len(paper.authors)` | — | `{len(paper.authors)}` | ✅ never `None` |
"""
    )


@app.cell
def _(mo):
    mo.md("## ResearchProduct — 9 Computed Properties")


@app.cell
def _(mo, paper):
    computed_table_data = [
        ("doi", str(paper.doi), "Loop through pids to find scheme='doi'"),
        ("all_dois", str(paper.all_dois), "Collect all pids with scheme='doi'"),
        (
            "is_open_access",
            str(paper.is_open_access),
            "Check bestAccessRight.label == 'OPEN'",
        ),
        (
            "open_access_url",
            str(paper.open_access_url),
            "Search instances for OA access URL",
        ),
        (
            "citation_count",
            str(paper.citation_count),
            "Navigate indicators.citationImpact.citationCount",
        ),
        (
            "publication_year",
            str(paper.publication_year),
            "Parse publicationDate[:4] with error handling",
        ),
        ("journal_name", str(paper.journal_name), "Guard container.name against None"),
        (
            "author_names",
            str(paper.author_names[:3]),
            "List comprehension with None filtering",
        ),
        ("license", str(paper.license), "Search instances for first non-empty license"),
    ]
    mo.ui.table(
        computed_table_data,
        headers=["Property", "Value", "What it replaces"],
        page_size=9,
    )
    return (computed_table_data,)


@app.cell
def _(mo):
    mo.md(
        """
## `__str__` & `__repr__` — Human-Readable Output

Every entity model provides a useful `str()` and `repr()` so you never
need to manually format titles, years, and identifiers.
"""
    )


@app.cell
async def _(client, mo, paper):
    org = await client.organizations.first(
        filters={"search": "University of Twente"},
    )
    project = await client.projects.first(
        filters={"search": "European"},
    )
    person = await client.persons.first(
        filters={"search": "machine learning"},
    )
    ds = await client.data_sources.first(
        filters={"search": "Zenodo"},
    )

    entity_strs = []
    entity_strs.append(("ResearchProduct", repr(paper), str(paper)))
    if org:
        entity_strs.append(("Organization", repr(org), str(org)))
    if project:
        entity_strs.append(("Project", repr(project), str(project)))
    if person:
        entity_strs.append(("Person", repr(person), str(person)))
    if ds:
        entity_strs.append(("DataSource", repr(ds), str(ds)))

    mo.ui.table(
        entity_strs,
        headers=["Entity", "repr()", "str()"],
        page_size=5,
    )
    return ds, entity_strs, org, person, project


@app.cell
def _(mo):
    mo.md("## Other Entity Computed Fields")


@app.cell
def _(ds, mo, org, person, project):
    other_data = []

    if org is not None:
        other_data.append(("Organization", "ror_id", str(org.ror_id)))
        other_data.append(("Organization", "country_code", str(org.country_code)))

    if person is not None:
        other_data.append(("Person", "full_name", person.full_name))
        other_data.append(("Person", "orcid", str(person.orcid)))

    if project is not None:
        other_data.append(("Project", "funder_name", str(project.funder_name)))
        other_data.append(
            ("Project", "funder_jurisdiction", str(project.funder_jurisdiction))
        )
        other_data.append(("Project", "start_year", str(project.start_year)))
        other_data.append(("Project", "end_year", str(project.end_year)))

    if ds is not None:
        other_data.append(("DataSource", "type_name", str(ds.type_name)))

    mo.ui.table(
        other_data,
        headers=["Entity", "Property", "Value"],
        page_size=10,
    )
    return (other_data,)


if __name__ == "__main__":
    app.run()
