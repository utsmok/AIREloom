# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "aireloom",
#     "certifi",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        """
    # AIREloom Quick Start

    **Switch to code view with Ctrl+. to see all code cells**

    This notebook demonstrates basic usage of AIREloom for retrieving
    and searching OpenAIRE research data.
    """
    )
    return (mo,)


@app.cell
def _():
    from aireloom import AireloomClient
    from aireloom.endpoints import ResearchProductsFilters
    from datetime import date

    client = AireloomClient()
    return ResearchProductsFilters, client, date


@app.cell
async def _(client, mo):
    mo.md("## 📄 Get a Single Research Product")
    try:
        product = await client.research_products.get(
            "doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108"
        )
        mo.md(f"**Found:** {product.title}")
    except Exception as e:
        mo.md(f"**Error:** {e}")
    return (product,)


@app.cell
async def _(ResearchProductsFilters, client, date, mo):
    mo.md("## 🔍 Search Research Products")
    filters = ResearchProductsFilters(
        search="machine learning", fromPublicationDate=date(2024, 1, 1)
    )

    response = await client.research_products.search(
        page=1, page_size=5, filters=filters
    )

    total_results = (
        response.header.numFound if response.header else len(response.results or [])
    )

    mo.md(f"Found **{total_results}** total results")
    return filters, response, total_results


@app.cell
def _(mo, response):
    mo.md("### Results Table")

    results = response.results or []
    rows = []
    for product in results[:5]:
        title = product.title or "No title"
        rows.append(
            {
                "Title": title,
                "Type": product.type or "Unknown",
                "Date": product.publicationDate or "N/A",
            }
        )

    mo.ui.table(rows, selection=None)
    return (rows,)


@app.cell
async def _(client, filters, mo):
    mo.md("## 🔄 Iterate Through Results")

    count = 0
    async for product in client.research_products.iterate(
        page_size=10, filters=filters
    ):
        count += 1
        if count >= 25:
            break

    mo.md(f"Processed **{count}** research products (capped at 25)")
    return (count,)


@app.cell
async def _(client, mo):
    mo.md("## 📊 Search Projects")
    try:
        projects_response = await client.projects.search(page_size=3)
        project_rows = []
        for project in projects_response.results or []:
            project_rows.append(
                {
                    "Title": project.title or "No title",
                    "Code": project.code or "N/A",
                    "Funding": (
                        project.funding[0].fundingPath if project.funding else "N/A"
                    ),
                }
            )
        mo.ui.table(project_rows, selection=None)
    except Exception as e:
        mo.md(f"**Error fetching projects:** {e}")
    return (project_rows,)


@app.cell
async def _(client):
    await client.aclose()


if __name__ == "__main__":
    app.run()
