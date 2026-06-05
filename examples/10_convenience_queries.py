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

    mo.md(
        r"""
    > 💡 **Switch to code view with Ctrl+. to see all code cells**

    # Convenience Queries — High-Level Research Workflows

    `AireloomSession.queries` exposes nine pre-built query functions that
    compose the low-level client into common research workflows with a
    single call. This notebook demonstrates every one of them.

    | # | Function | Purpose |
    |---|----------|---------|
    | 1 | `publications_by_doi` | Look up papers by DOI |
    | 2 | `publications_by_organization` | Publications for an org |
    | 3 | `publications_by_author` | Publications by name / ORCID |
    | 4 | `publications_by_project` | Publications linked to a project |
    | 5 | `count_publications` | Count without downloading |
    | 6 | `projects_by_organization` | Projects for an org |
    | 7 | `citing_works` | Works that cite a DOI (Scholix) |
    | 8 | `related_datasets` | Datasets linked to a DOI (Scholix) |
    | 9 | `all_links` | All Scholix links for a DOI |
    """
    )


@app.cell
def _():
    from aireloom.session import AireloomSession

    session = AireloomSession()
    q = session.queries
    return q, session


@app.cell
async def _(mo, q, session):
    _papers = await q.publications_by_doi(
        session,
        "10.1038/s41586-024-07386-0",
        "10.1038/s41586-024-07891-0",
    )

    _rows = [
        {
            "title": p.title,
            "doi": p.doi or "—",
            "year": p.publication_year or "—",
            "open_access": p.is_open_access,
            "citations": p.citation_count or 0,
            "license": p.license or "—",
        }
        for p in _papers
    ]

    (
        mo.md(
            f"""
    ## 1. Publications by DOI

    `q.publications_by_doi(session, *dois)` — fetch research products
    for one or more DOIs.

    Found **{len(_papers)}** results:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _pubs = await q.publications_by_organization(
        session,
        "University of Twente",
        search_on="name",
        type="publication",
        from_publication_date="2024-01-01",
        open_access_only=True,
        sort_by="publicationDate desc",
        limit=5,
    )

    _rows = [
        {"title": p.title, "year": p.publication_year or "—", "doi": p.doi or "—"}
        for p in _pubs
    ]

    (
        mo.md(
            f"""
    ## 2. Publications by Organization

    `q.publications_by_organization(session, identifier, …)` — recent
    open-access publications from the University of Twente (2024+).

    Found **{len(_pubs)}** results:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _pubs = await q.publications_by_author(
        session,
        "0000-0002-3639-3956",
        search_on="orcid",
        limit=5,
    )

    _rows = [
        {"title": p.title, "year": p.publication_year or "—", "doi": p.doi or "—"}
        for p in _pubs
    ]

    (
        mo.md(
            f"""
    ## 3. Publications by Author

    `q.publications_by_author(session, identifier, search_on="orcid", …)`
    — publications by ORCID `0000-0002-3639-3956`.

    Found **{len(_pubs)}** results:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _pubs = await q.publications_by_project(
        session,
        "OpenAIRE-Nexus",
        search_on="name",
        limit=3,
    )

    _rows = [
        {"title": p.title, "year": p.publication_year or "—", "doi": p.doi or "—"}
        for p in _pubs
    ]

    (
        mo.md(
            f"""
    ## 4. Publications by Project

    `q.publications_by_project(session, identifier, search_on="name", …)`
    — publications linked to the OpenAIRE-Nexus project.

    Found **{len(_pubs)}** results:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _scenarios = [
        ("All publications", dict(type="publication")),
        ("All datasets", dict(type="dataset")),
        ("Open Access publications", dict(type="publication", open_access_only=True)),
        ("Machine learning", dict(search="machine learning")),
        (
            "Deep learning publications",
            dict(search="deep learning", type="publication"),
        ),
    ]

    _rows = [
        {"query": _label, "count": await q.count_publications(session, **_kw)}
        for _label, _kw in _scenarios
    ]

    (
        mo.md(
            r"""
    ## 5. Count Publications

    `q.count_publications(session, **filters)` — count matching products
    without downloading them. Various scenarios:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _projects = await q.projects_by_organization(
        session,
        "University of Twente",
        limit=5,
    )

    _rows = [
        {
            "title": p.title,
            "code": p.code or "—",
            "start": p.start_year or "—",
            "end": p.end_year or "—",
            "funder": p.funder_name or "—",
        }
        for p in _projects
    ]

    (
        mo.md(
            f"""
    ## 6. Projects by Organization

    `q.projects_by_organization(session, identifier, …)` — projects
    associated with the University of Twente.

    Found **{len(_projects)}** results:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _DOI = "10.1038/s41586-024-07386-0"

    _citations = await q.citing_works(session, _DOI, limit=5)
    _rows = [{"relationship": str(cite)} for cite in _citations]

    (
        mo.md(
            f"""
    ## 7. Citing Works (Scholix)

    `q.citing_works(session, doi, limit=5)` — works that cite
    `{_DOI}` via Scholix.

    Found **{len(_citations)}** citing works:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _DOI = "10.1038/s41586-024-07386-0"

    _datasets = await q.related_datasets(session, _DOI, limit=5)
    _rows = [{"relationship": str(ds)} for ds in _datasets]

    (
        mo.md(
            f"""
    ## 8. Related Datasets (Scholix)

    `q.related_datasets(session, doi, limit=5)` — datasets linked to
    `{_DOI}` via Scholix.

    Found **{len(_datasets)}** related datasets:
    """
        ),
        mo.ui.table(_rows, selection=None),
    )


@app.cell
async def _(mo, q, session):
    _DOI = "10.1038/s41586-024-07386-0"

    _links = await q.all_links(session, _DOI, direction="both", limit=10)

    mo.md(
        f"""
    ## 9. All Scholix Links

    `q.all_links(session, doi, direction="both", limit=10)` — every
    Scholix relationship involving `{_DOI}` (as source or target).

    Found **{len(_links)}** total links.
    """
    )


@app.cell
def _(mo):
    mo.md(r"""
## Summary — All 9 Convenience Queries

| # | Function | Signature |
|---|----------|-----------|
| 1 | `publications_by_doi` | `(session, *dois) → list[ResearchProduct]` |
| 2 | `publications_by_organization` | `(session, identifier, *, search_on, type, from_publication_date, to_publication_date, open_access_only, sort_by, limit) → list[ResearchProduct]` |
| 3 | `publications_by_author` | `(session, identifier, *, search_on, type, sort_by, limit) → list[ResearchProduct]` |
| 4 | `publications_by_project` | `(session, identifier, *, search_on, type, sort_by, limit) → list[ResearchProduct]` |
| 5 | `count_publications` | `(session, *, type, open_access_only, search, pid, author_orcid, rel_organization_id, rel_project_id) → int` |
| 6 | `projects_by_organization` | `(session, identifier, *, search_on, sort_by, limit) → list[Project]` |
| 7 | `citing_works` | `(session, doi, *, source_type, sort_by, limit) → list[ScholixRelationship]` |
| 8 | `related_datasets` | `(session, doi, *, sort_by, limit) → list[ScholixRelationship]` |
| 9 | `all_links` | `(session, doi, *, direction, sort_by, limit) → list[ScholixRelationship]` |
""")


if __name__ == "__main__":
    app.run()
