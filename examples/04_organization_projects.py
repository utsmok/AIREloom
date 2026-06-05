# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "aireloom",
#   "certifi",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        r"""
    # Organization → Research Products & Projects

    Look up **University of Twente**, retrieve their research products and projects
    using `relOrganizationId` filters, and display funding info from typed Project models.

    **What Aireloom provides over raw HTTP:**
    - **Type-safe filter models**: `relOrganizationId` is a validated field on both
      `ResearchProductsFilters` and `ProjectsFilters`. Typos like `relOrgId` are
      caught by Pydantic's `extra='forbid'` BEFORE the API call.
    - **Nested model access**: `project.fundings[0].shortName`, `project.granted.fundedAmount`,
      `project.granted.currency` — all typed and autocompletable.
    - **Reusable `AireloomClient` context**: one auth session handles multiple resource
      clients (organizations, research_products, projects) with shared connection pooling.

    *Switch to code view with Ctrl+. to see all code cells*
    """
    )
    return (mo,)


@app.cell
def _():
    from aireloom import AireloomClient
    from aireloom.endpoints import (
        OrganizationsFilters,
        ProjectsFilters,
        ResearchProductsFilters,
    )

    ORG_NAME = "University of Twente"
    client = AireloomClient()
    return (
        AireloomClient,
        ORG_NAME,
        OrganizationsFilters,
        ProjectsFilters,
        ResearchProductsFilters,
        client,
    )


@app.cell
async def _(ORG_NAME, OrganizationsFilters, client, mo):
    mo.md(f"## 1. Searching for organization '{ORG_NAME}'")

    org_filters = OrganizationsFilters(search=ORG_NAME)
    org_response = await client.organizations.search(
        page=1, page_size=5, filters=org_filters
    )

    if not org_response.results:
        mo.stop(True, mo.md("**No organizations found.**"))

    org = org_response.results[0]
    org_id = org.id

    details = f"**Found:** {org.legalName} (id: `{org_id}`)"
    if org.country:
        details += f"\n\nCountry: {org.country.label} ({org.country.code})"
    if org.websiteUrl:
        details += f"\n\nWebsite: {org.websiteUrl}"

    mo.md(details)
    return org, org_id, org_response


@app.cell
async def _(ORG_NAME, ResearchProductsFilters, client, mo, org, org_id):
    short_name = org.legalShortName or ORG_NAME
    mo.md(f"## 2. Research products linked to {short_name}")

    rp_filters = ResearchProductsFilters(
        relOrganizationId=org_id,
        type="publication",
        isPeerReviewed=True,
    )

    rp_response = await client.research_products.search(
        page=1,
        page_size=10,
        filters=rp_filters,
        sort_by="publicationDate DESC",
    )

    total_rp = rp_response.header.numFound or 0
    mo.md(f"Total publications: **{total_rp:,}**")
    return rp_response, short_name, total_rp


@app.cell
def _(mo, rp_response):
    mo.md("### Recent Publications")

    rows = []
    for product in (rp_response.results or [])[:10]:
        title = (product.title or "—")[:60]
        year = (product.publicationDate or "—")[:4]
        access = product.bestAccessRight.label if product.bestAccessRight else "—"
        ptype = product.type or "—"
        rows.append(
            {
                "Title": title,
                "Year": year,
                "Access": access,
                "Type": ptype,
            }
        )

    mo.ui.table(rows, selection=None)
    return (rows,)


@app.cell
async def _(ORG_NAME, ProjectsFilters, client, mo, org_id):
    mo.md(f"## 3. Projects linked to {ORG_NAME}")

    proj_filters = ProjectsFilters(
        relOrganizationId=org_id,
    )

    proj_response = await client.projects.search(
        page=1,
        page_size=20,
        filters=proj_filters,
        sort_by="startDate DESC",
    )

    total_proj = proj_response.header.numFound or 0
    mo.md(f"Total projects: **{total_proj:,}**")
    return proj_response, total_proj


@app.cell
def _(mo, proj_response):
    mo.md("### Recent Projects")

    rows = []
    funder_counts: dict[str, int] = {}
    total_funding = 0.0
    currency = "EUR"

    for project in (proj_response.results or [])[:20]:
        acronym = project.acronym or "—"
        title = (project.title or "—")[:45]
        period = f"{project.startDate or '?'} → {project.endDate or '?'}"

        funder = "—"
        if project.fundings:
            for f in project.fundings:
                if f.shortName:
                    funder = f.shortName
                    funder_counts[f.shortName] = funder_counts.get(f.shortName, 0) + 1
                    break

        grant_str = "—"
        if project.granted:
            currency = project.granted.currency or "EUR"
            if project.granted.fundedAmount is not None:
                total_funding += project.granted.fundedAmount
                grant_str = f"{project.granted.fundedAmount:,.0f} {currency}"
            elif project.granted.totalCost is not None:
                grant_str = f"Cost: {project.granted.totalCost:,.0f} {currency}"

        rows.append(
            {
                "Acronym": acronym,
                "Title": title,
                "Funding": funder,
                "Period": period,
                "Grant": grant_str,
            }
        )

    mo.ui.table(rows, selection=None)

    # Funding summary
    summary_parts = ["#### Funding Summary\n"]
    if funder_counts:
        summary_parts.append("**Funder distribution (of displayed projects):**\n")
        for funder, cnt in sorted(funder_counts.items(), key=lambda x: -x[1]):
            summary_parts.append(f"- {funder}: {cnt} projects")
        summary_parts.append("")

    if total_funding > 0:
        summary_parts.append(
            f"**Total funded amount (displayed):** {total_funding:,.0f} {currency}"
        )

    if len(summary_parts) > 1:
        mo.md("\n".join(summary_parts))

    return currency, funder_counts, rows, total_funding


@app.cell
def _(mo):
    mo.md(
        """
    ## Type-safe filter models

    Valid field names are enforced by Pydantic.

    This would raise `ValidationError` at instantiation:

    ```python
    ResearchProductsFilters(relOrgId='...')  # typo: should be relOrganizationId
    ```

    The correct spelling:

    ```python
    ResearchProductsFilters(relOrganizationId='...')  # ✓
    ```
    """
    )


@app.cell
async def _(client):
    await client.aclose()


if __name__ == "__main__":
    app.run()
