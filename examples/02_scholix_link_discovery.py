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
        """
    # Scholix Link Discovery

    Discover datasets linked to a publication DOI via the Scholix (Scholexplorer) API.

    **Switch to code view with Ctrl+. to see all code cells**
    """
    )
    return (mo,)


@app.cell
def _():
    from collections import Counter

    from aireloom import AireloomClient
    from aireloom.endpoints import ScholixFilters

    SOURCE_DOI = "10.1016/j.respol.2021.104226"

    client = AireloomClient()
    return AireloomClient, Counter, ScholixFilters, SOURCE_DOI, client


@app.cell
def _pid_str():
    def _pid_str(identifiers: list, scheme: str = "doi") -> str:
        """Extract the first identifier matching a scheme, or the first available."""
        for pid in identifiers:
            s = getattr(pid, "id_scheme", "") or ""
            if s.lower() == scheme:
                return getattr(pid, "id_val", "")
        if identifiers:
            return getattr(identifiers[0], "id_val", "")
        return "—"

    return (_pid_str,)


@app.cell
def _():
    return


@app.cell
async def _(ScholixFilters, SOURCE_DOI, client, mo):
    filters = ScholixFilters(sourcePid=SOURCE_DOI, targetType="Dataset")

    mo.md(
        f"""
    ## 1. Single-page search (up to 20 results)

    Querying Scholix for datasets linked to DOI `{SOURCE_DOI}` …
    """
    )
    return (filters,)


@app.cell
async def _(SOURCE_DOI, client, filters, mo):
    try:
        response = await client.scholix.search_links(
            page=0, page_size=20, filters=filters
        )
        total = response.total_links
        page_count = len(response.result)
    except Exception as exc:
        total = 0
        page_count = 0
        response = None

    mo.md(
        f"""
    **Total linked datasets reported by Scholix:** {total}
    **Retrieved in this page:** {page_count}
    """
    )
    return page_count, response, total


@app.cell
async def _(SOURCE_DOI, client, filters, mo):
    mo.md("## 2. Streaming ALL linked datasets via `iterate_links()`")

    links = []
    try:
        async for rel in client.scholix.iterate_links(page_size=50, filters=filters):
            links.append(rel)
            if len(links) >= 100:
                break
    except Exception:
        pass

    mo.md(f"Collected **{len(links)}** links (capped at 100 for demo).")
    return (links,)


@app.cell
async def _(links, mo):
    if not links:
        mo.stop(True, mo.md("**No linked datasets found.**"))


@app.cell
def _(SOURCE_DOI, links, mo, _pid_str):
    if not links:
        mo.md("")

    # Build table data
    rows = []
    for i, rel in enumerate(links[:20], 1):
        target = rel.target
        title = (target.title or "—")[:55]
        doi = _pid_str(target.identifier, "doi")
        rel_name = rel.relationship_type.name
        providers = ", ".join(p.name for p in (rel.link_provider or []))[:30]
        rows.append(
            {
                "#": i,
                "Target Title": title,
                "Target DOI": doi,
                "Relationship": rel_name,
                "Providers": providers,
            }
        )

    table = mo.ui.table(
        data=rows,
        label=f"Linked Datasets for {SOURCE_DOI} (first 20 shown)",
    )

    remaining = len(links) - 20 if len(links) > 20 else 0
    footer = f"… and {remaining} more (capped for display)" if remaining > 0 else ""

    mo.md(f"{table}\n{footer}")
    return


@app.cell
def _(Counter, links, mo):
    rel_type_counts = Counter(rel.relationship_type.name for rel in links)

    lines = ["## 3. Relationship type distribution\n"]
    for rel_name, count in rel_type_counts.most_common():
        lines.append(f"- **{rel_name}**: {count}")
    lines.append(f"\n**Total links collected:** {len(links)}")

    mo.md("\n".join(lines))
    return


@app.cell
def _(links, mo):
    if not links:
        mo.md("")

    sample = links[0]
    src_ids = sample.source.identifier
    src_pid = f"{src_ids[0].id_scheme}:{src_ids[0].id_val}" if src_ids else "—"

    mo.md(
        f"""
    ## 4. Sample link — typed field access

    | Field | Value |
    |---|---|
    | `source.type` | `{sample.source.type!r}` |
    | `source.title` | `{sample.source.title!r}` |
    | `target.type` | `{sample.target.type!r}` |
    | `relationship_type` | `{sample.relationship_type.name!r}` |
    | `source PID` | `{src_pid}` |
    """
    )
    return


@app.cell
async def _(client):
    await client.aclose()
    return


if __name__ == "__main__":
    app.run()
