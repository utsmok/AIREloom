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
        r"""
    # Iterator Helpers — collect(), count(), first()

    AIREloom provides three convenience helpers on every resource client that build on top
    of `iterate()` and `search()` to eliminate common boilerplate:

    | Helper | Returns | Purpose |
    |--------|---------|---------|
    | `count()` | `int` | Total results without downloading any data |
    | `first()` | `Entity \| None` | Grab the single top match for a query |
    | `collect()` | `list[Entity]` | Materialize iteration into a list, with optional limit |

    All three accept the same `filters` parameter as `search()` and `iterate()`.
    """
    )


@app.cell
def _():
    from aireloom import AireloomClient
    from aireloom.endpoints import (
        OrganizationsFilters,
        ProjectsFilters,
        ResearchProductsFilters,
    )

    client = AireloomClient()
    return OrganizationsFilters, ProjectsFilters, ResearchProductsFilters, client


@app.cell
async def _(ResearchProductsFilters, client, mo):
    total_pubs = await client.research_products.count(
        filters=ResearchProductsFilters(type="publication"),
    )
    total_datasets = await client.research_products.count(
        filters=ResearchProductsFilters(type="dataset"),
    )
    total_oa = await client.research_products.count(
        filters=ResearchProductsFilters(
            type="publication",
            bestOpenAccessRightLabel="OPEN",
        ),
    )
    total_ml = await client.research_products.count(
        filters=ResearchProductsFilters(search="machine learning"),
    )

    oa_ratio = f"{total_oa / total_pubs:.1%}" if total_pubs else "N/A"

    mo.md(
        f"""
    ## `count()` — Zero-download tallies

    | Query | Count |
    |-------|------|
    | Total publications | **{total_pubs:,}** |
    | Total datasets | **{total_datasets:,}** |
    | Open Access publications | **{total_oa:,}** |
    | Machine learning results | **{total_ml:,}** |

    **OA ratio:** {oa_ratio}
    """
    )


@app.cell
async def _(OrganizationsFilters, ProjectsFilters, ResearchProductsFilters, client, mo):
    paper = await client.research_products.first(
        filters=ResearchProductsFilters(
            search="transformer architecture",
            type="publication",
        ),
        sort_by="publicationDate desc",
    )

    org = await client.organizations.first(
        filters=OrganizationsFilters(search="CERN"),
    )

    project = await client.projects.first(
        filters=ProjectsFilters(search="quantum computing"),
        sort_by="startDate desc",
    )

    _parts = []
    if paper:
        authors = ", ".join(paper.author_names[:3])
        _parts.append(
            f"### Latest transformer paper\n"
            f"**{paper.title}**\n\n"
            f"- DOI: `{paper.doi}`\n"
            f"- Year: {paper.publication_year}\n"
            f"- Authors: {authors}\n"
        )
    else:
        _parts.append("### Latest transformer paper\nNo results found.")

    if org:
        _parts.append(
            f"### Top CERN match\n"
            f"**{org}**\n\n"
            f"- Country: `{org.country_code}`\n"
            f"- ROR: `{org.ror_id}`\n"
        )
    else:
        _parts.append("### Top CERN match\nNo results found.")

    if project:
        period = f"{project.start_year}–{project.end_year}"
        _parts.append(
            f"### Latest quantum project\n"
            f"**{project}**\n\n"
            f"- Funder: {project.funder_name}\n"
            f"- Period: {period}\n"
        )
    else:
        _parts.append("### Latest quantum project\nNo results found.")

    mo.md("## `first()` — Grab the top result\n\n" + "\n".join(_parts))


@app.cell
async def _(ProjectsFilters, ResearchProductsFilters, client, mo):
    software = await client.research_products.collect(
        filters=ResearchProductsFilters(
            type="software",
            fromPublicationDate="2024-01-01",
        ),
        sort_by="publicationDate desc",
        limit=5,
    )

    ai_projects = await client.projects.collect(
        filters=ProjectsFilters(search="artificial intelligence"),
        limit=5,
    )

    sw_rows = "\n".join(
        f"| {sw.title[:50]} | `{sw.programmingLanguage or '—'}` | `{sw.codeRepositoryUrl or '—'}` |"
        for sw in software
    )

    proj_rows = "\n".join(
        f"| {p} | {p.funder_name or '—'} | {p.start_year or '—'}–{p.end_year or '—'} |"
        for p in ai_projects
    )

    mo.md(
        f"""
    ## `collect()` — Materialize results into a list

    ### Recent software packages ({len(software)} collected)

    | Title | Language | Repo |
    |-------|----------|------|
    {sw_rows}

    ### AI-related projects ({len(ai_projects)} collected)

    | Project | Funder | Period |
    |---------|--------|--------|
    {proj_rows}
    """
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Summary

    | Helper | Returns | Use case |
    |--------|---------|----------|
    | `count()` | `int` | Get total results without downloading data |
    | `first()` | `Entity \| None` | Grab the single top match |
    | `collect()` | `list[Entity]` | Materialize iteration into a list, with optional limit |
    | `iterate()` | `AsyncIterator[Entity]` | Stream results one-by-one (cursor or page-based) |
    | `search()` | `ApiResponse` | Paginated search with header metadata |
    | `get()` | `Entity` | Fetch a single entity by ID |
    """
    )


if __name__ == "__main__":
    app.run()
