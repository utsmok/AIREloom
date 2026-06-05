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
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    > 💡 **Switch to code view with Ctrl+. to see all code cells**

    # Ergonomics Showcase — Before & After

    AIREloom provides an **ergonomics layer** on top of the raw API:

    - **Computed fields** replace manual data extraction loops and null-guard chains
    - **Safe types** (`SafeStr`, `SafeList`) eliminate `None` checks for common fields
    - **Convenience queries** compose multi-step workflows into single calls

    This notebook demonstrates the difference using a real paper
    (`10.1038/s41586-024-07386-0`).
    """
    )


@app.cell
def _():
    from aireloom.endpoints import ResearchProductsFilters
    from aireloom.session import AireloomSession

    DOI = "10.1038/s41586-024-07386-0"
    session = AireloomSession()
    return DOI, ResearchProductsFilters, session


@app.cell
def _(mo):
    mo.md(r"""## Raw API Usage — Manual Extraction""")


@app.cell
async def _(DOI, ResearchProductsFilters, mo, session):
    resp = await session.research_products.search(
        page=1,
        page_size=1,
        filters=ResearchProductsFilters(pid=DOI),
    )
    results = resp.results or []
    raw_paper = results[0] if results else None
    raw_paper
    return (raw_paper,)


@app.cell
def _(mo, raw_paper):
    # Manually extract DOI from pids list
    manual_doi = None
    for _pid in raw_paper.pids or []:
        if (_pid.scheme or "").lower() == "doi" and _pid.value:
            manual_doi = _pid.value
            break

    # Manually check open access
    manual_is_oa = (
        raw_paper.bestAccessRight
        and raw_paper.bestAccessRight.label
        and raw_paper.bestAccessRight.label.upper() == "OPEN"
    )

    # Manually find open access URL
    manual_oa_url = None
    for _inst in raw_paper.instances or []:
        if (
            _inst.accessRight
            and _inst.accessRight.label
            and _inst.accessRight.label.upper() == "OPEN"
            and _inst.urls
        ):
            manual_oa_url = _inst.urls[0]
            break

    # Manually extract citation count (deeply nested, each level may be None)
    manual_citation_count = None
    if raw_paper.indicators:
        if raw_paper.indicators.citationImpact:
            manual_citation_count = raw_paper.indicators.citationImpact.citationCount

    # Manually get author names
    manual_author_names = []
    for _author in raw_paper.authors or []:
        if _author.fullName:
            manual_author_names.append(_author.fullName)

    # Manually extract journal name
    manual_journal = None
    if raw_paper.container and raw_paper.container.name:
        manual_journal = raw_paper.container.name

    # Manually extract publication year
    manual_year = None
    if raw_paper.publicationDate and len(raw_paper.publicationDate) >= 4:
        try:
            manual_year = int(raw_paper.publicationDate[:4])
        except ValueError:
            pass

    mo.md(
        f"""
    ### What you had to write with the raw API

    **DOI** — loop through `pids`, check `scheme == "doi"`:

    ```
    for pid in (paper.pids or []):
        if (pid.scheme or "").lower() == "doi" and pid.value:
            doi = pid.value; break
    ```
    → **`{manual_doi}`**

    **Open Access** — null-guard chain on `bestAccessRight`:

    ```
    paper.bestAccessRight and paper.bestAccessRight.label
        and paper.bestAccessRight.label.upper() == "OPEN"
    ```
    → **`{manual_is_oa}`**

    **OA URL** — loop instances, check accessRight, grab first URL:

    ```
    for inst in (paper.instances or []):
        if inst.accessRight and inst.accessRight.label == "OPEN" and inst.urls:
            url = inst.urls[0]; break
    ```
    → **`{manual_oa_url}`**

    **Citation count** — navigate three nullable levels:

    ```
    if paper.indicators:
        if paper.indicators.citationImpact:
            count = paper.indicators.citationImpact.citationCount
    ```
    → **`{manual_citation_count}`**

    **Authors** — loop with None guard on each fullName:

    ```
    [a.fullName for a in (paper.authors or []) if a.fullName]
    ```
    → **`{manual_author_names[:5]}`**

    **Journal** — guard `container` and `container.name`:

    ```
    paper.container and paper.container.name or None
    ```
    → **`{manual_journal}`**

    **Year** — parse from date string with try/except:

    ```
    int(paper.publicationDate[:4])
    ```
    → **`{manual_year}`**
    """
    )


@app.cell
def _(mo):
    mo.md(r"""## Ergonomics Layer — Computed Fields & Convenience Queries""")


@app.cell
async def _(DOI, mo, session):
    papers = await session.queries.publications_by_doi(session, DOI)
    paper = papers[0] if papers else None
    paper
    return (paper,)


@app.cell
def _(mo, paper):
    mo.md(
        f"""
    ### What you write with the ergonomics layer

    Each computed field is a single property access — no loops, no null guards:

    | Extraction | Raw API lines | Ergonomics | Result |
    |---|---|---|---|
    | DOI | `for pid in pids: if scheme == "doi"…` | `paper.doi` | `{paper.doi}` |
    | Open Access | `bestAccessRight and .label == "OPEN"` | `paper.is_open_access` | `{paper.is_open_access}` |
    | OA URL | `for inst in instances: if accessRight…` | `paper.open_access_url` | `{paper.open_access_url}` |
    | Citations | `indicators and .citationImpact.citationCount` | `paper.citation_count` | `{paper.citation_count}` |
    | Authors | `[a.fullName for a in authors if a.fullName]` | `paper.author_names` | `{paper.author_names[:5]}` |
    | Journal | `container and container.name or None` | `paper.journal_name` | `{paper.journal_name}` |
    | Year | `int(publicationDate[:4])` with try/except | `paper.publication_year` | `{paper.publication_year}` |
    | License | `for inst in instances: if inst.license…` | `paper.license` | `{paper.license}` |

    **Safe defaults** — `paper.title` is always a `str` (never `None`),
    `paper.authors` is always a `list` (never `None`).

    **Human-readable summary** — `str(paper)` produces:

    > `{paper}`
    """
    )


@app.cell
def _(mo):
    mo.md(r"""## Comparison Summary""")


@app.cell
def _(mo):
    comparison = [
        {
            "Task": "Get DOI",
            "Raw API": "for pid in pids:\n    if pid.scheme == 'doi'…",
            "Ergonomics": "paper.doi",
        },
        {
            "Task": "Check Open Access",
            "Raw API": "bestAccessRight and\nbestAccessRight.label\n== 'OPEN'",
            "Ergonomics": "paper.is_open_access",
        },
        {
            "Task": "Find OA URL",
            "Raw API": "for inst in instances:\n    if inst.accessRight…",
            "Ergonomics": "paper.open_access_url",
        },
        {
            "Task": "Citation count",
            "Raw API": "indicators and\nindicators.citationImpact\nand .citationCount",
            "Ergonomics": "paper.citation_count",
        },
        {
            "Task": "Author names",
            "Raw API": "[a.fullName for a in\nauthors if a.fullName]",
            "Ergonomics": "paper.author_names",
        },
        {
            "Task": "Journal name",
            "Raw API": "container and\ncontainer.name or None",
            "Ergonomics": "paper.journal_name",
        },
        {
            "Task": "Publication year",
            "Raw API": "int(publicationDate[:4])\nwith try/except",
            "Ergonomics": "paper.publication_year",
        },
        {
            "Task": "License",
            "Raw API": "for inst in instances:\n    if inst.license…",
            "Ergonomics": "paper.license",
        },
        {
            "Task": "Org publications",
            "Raw API": "search org → get id\n→ search products\nwith relOrganizationId",
            "Ergonomics": "queries.publications_by_\norganization(session, name)",
        },
        {
            "Task": "Count results",
            "Raw API": "search(pageSize=0)\n→ header.numFound",
            "Ergonomics": "queries.count_publications(\nsession, ...)",
        },
        {
            "Task": "Display summary",
            "Raw API": "product.title or\n'Untitled'",
            "Ergonomics": "str(product)",
        },
        {
            "Task": "Null safety",
            "Raw API": "if x is not None:\n    for item in x or []:",
            "Ergonomics": "SafeList → []\nSafeStr → ''",
        },
    ]
    mo.ui.table(comparison, selection=None)


if __name__ == "__main__":
    app.run()
