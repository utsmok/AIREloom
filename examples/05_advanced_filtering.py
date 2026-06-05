# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "aireloom",
#     "marimo",
# ]
#
# [tool.marimo.display]
# cell_output = "above"
# ///

"""
Advanced Filtering — Complex filter combinations with Pydantic validation.

This example demonstrates building complex queries with multiple filter fields,
combining type/date/access/subject constraints, using sort parameters, and
showing how Pydantic validation catches mistakes before hitting the API.

Run with: uv run examples/05_advanced_filtering.py
"""

import marimo

__generated_with = "0.13.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from datetime import date

    from aireloom import AireloomClient
    from aireloom.endpoints import (
        ProjectsFilters,
        ResearchProductsFilters,
        ScholixFilters,
    )

    return (
        AireloomClient,
        ProjectsFilters,
        ResearchProductsFilters,
        ScholixFilters,
        date,
        mo,
    )


@app.cell
def _(mo):
    mo.md(
        """
    # Advanced Filtering: Complex Queries & Validation

    **Switch to code view with Ctrl+. to see all code cells**

    This notebook demonstrates:

    - Building complex **ResearchProductsFilters** (type + date + OA + peer-reviewed + subjects)
    - Building **ProjectsFilters** (funding program + date range + sort)
    - How **Pydantic validation** catches typos and invalid values *before* any API call
    """
    )


@app.cell
async def _(AireloomClient, ProjectsFilters, date, mo):
    mo.md("## EC-Funded Projects (2023–2024)").center()

    filters = ProjectsFilters(
        fundingShortName="EC",
        fromStartDate=date(2023, 1, 1),
        toStartDate=date(2024, 12, 31),
    )

    mo.md(
        f"""
    **Filters applied:**

    | Field | Value |
    |---|---|
    | `fundingShortName` | `EC` |
    | `fromStartDate` | `2023-01-01` |
    | `toStartDate` | `2024-12-31` |
    | `sort_by` | `startDate DESC` |
    """
    )

    async with AireloomClient() as client:
        try:
            response = await client.projects.search(
                page=1, page_size=10, filters=filters, sort_by="startDate DESC"
            )
        except Exception as exc:
            mo.md(f"**Search failed:** {exc}")
            return

    total = response.header.numFound or 0
    mo.md(f"**Results:** {total:,} EC-funded projects starting 2023–2024").center()

    rows = []
    for project in (response.results or [])[:10]:
        funded = "—"
        if project.granted and project.granted.fundedAmount is not None:
            curr = project.granted.currency or "EUR"
            funded = f"{project.granted.fundedAmount:,.0f} {curr}"
        rows.append(
            {
                "Acronym": project.acronym or "—",
                "Title": (project.title or "—")[:80],
                "Code": project.code or "—",
                "Start → End": f"{project.startDate or '?'} → {project.endDate or '?'}",
                "Funded": funded,
            }
        )

    mo.ui.table(rows, selection=None)


@app.cell
async def _(AireloomClient, ResearchProductsFilters, date, mo):
    mo.md("## Research Products: Multi-Field Filter").center()

    filters = ResearchProductsFilters(
        search="machine learning",
        type="publication",
        fromPublicationDate=date(2023, 1, 1),
        toPublicationDate=date(2024, 12, 31),
        bestOpenAccessRightLabel="OPEN",
        isPeerReviewed=True,
        subjects=["computer science"],
    )

    mo.md(
        """
    **Filters applied:**

    | Field | Value |
    |---|---|
    | `search` | `machine learning` |
    | `type` | `publication` |
    | `fromPublicationDate` | `2023-01-01` |
    | `toPublicationDate` | `2024-12-31` |
    | `bestOpenAccessRightLabel` | `OPEN` |
    | `isPeerReviewed` | `True` |
    | `subjects` | `['computer science']` |
    """
    )

    async with AireloomClient() as client:
        try:
            response = await client.research_products.search(
                page=1,
                page_size=10,
                filters=filters,
                sort_by="publicationDate DESC",
            )
        except Exception as exc:
            mo.md(f"**Search failed:** {exc}")
            return

    total = response.header.numFound or 0
    mo.md(f"**Results:** {total:,} matching publications").center()

    rows = []
    for product in (response.results or [])[:10]:
        doi = "—"
        if product.pids:
            for pid in product.pids:
                if (pid.scheme or "").lower() == "doi":
                    doi = pid.value or "—"
                    break
        rows.append(
            {
                "Title": (product.title or "—")[:80],
                "DOI": doi,
                "Date": product.publicationDate or "—",
                "Publisher": (product.publisher or "—")[:30],
            }
        )

    table = mo.ui.table(rows, selection=None)

    # iterate() sample
    async with AireloomClient() as client:
        iterated = []
        try:
            async for product in client.research_products.iterate(
                page_size=50, filters=filters, sort_by="publicationDate DESC"
            ):
                iterated.append(product.title or "—")
                if len(iterated) >= 5:
                    break
        except Exception as exc:
            iterated.append(f"(error: {exc})")

    sample = mo.md(
        "**Streaming first 5 via `iterate()` with same filters:**\n\n"
        + "\n".join(f"{i + 1}. {t}" for i, t in enumerate(iterated))
    )

    mo.vstack([table, sample])


@app.cell
def _(ResearchProductsFilters, ScholixFilters, mo):
    mo.md(
        """
    ## Pydantic Validation: Catching Errors Early

    All filter models use `extra='forbid'` and strict type checking.
    Typos, invalid values, and wrong types are caught **at instantiation** —
    no silent 400 errors or empty result sets from the server.
    """
    )

    results = []

    # 1. Typo in field name
    try:
        ResearchProductsFilters(tipe="publication")  # type: ignore[call-arg]
    except Exception as exc:
        results.append(
            (
                "Typo in filter field name",
                "tipe='publication'",
                type(exc).__name__,
                str(exc),
            )
        )

    # 2. Invalid literal value for 'type'
    try:
        ResearchProductsFilters(type="journal")  # type: ignore[call-arg]
    except Exception as exc:
        results.append(
            (
                "Invalid literal value for 'type'",
                "type='journal'",
                type(exc).__name__,
                str(exc),
            )
        )

    # 3. Wrong type for date field
    try:
        ResearchProductsFilters(fromPublicationDate="last year")  # type: ignore[arg-type]
    except Exception as exc:
        results.append(
            (
                "Wrong type for date field",
                "fromPublicationDate='last year'",
                type(exc).__name__,
                str(exc),
            )
        )

    # 4. Unknown field (extra='forbid')
    try:
        ScholixFilters(sourceDOI="10.1234/x")  # type: ignore[call-arg]
    except Exception as exc:
        results.append(
            (
                "Unknown field (extra='forbid')",
                "sourceDOI='10.1234/x'",
                type(exc).__name__,
                str(exc),
            )
        )

    sections = []
    for label, code_snippet, exc_type, exc_msg in results:
        sections.append(
            f"### {label}\n\n"
            f"```python\n{code_snippet}\n```\n\n"
            f"**✓ Caught:** `{exc_type}`\n\n"
            f"> {exc_msg}\n"
        )

    sections.append(
        "\n---\n\n**All invalid inputs caught BEFORE any API call.**\n\n"
        "With raw HTTP, these would either silently return empty results or produce confusing 400 errors."
    )

    mo.md("\n".join(sections))


if __name__ == "__main__":
    app.run()
