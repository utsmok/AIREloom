# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "aireloom",
#   "marimo",
# ]
#
# [tool.uv.sources]
# aireloom = { path = "..", editable = true }
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    """Header — Research Product Analysis."""
    import marimo as mo

    mo.md(
        """
    # Research Product Analysis

    Streaming analysis of **'open science'** publications using cursor-based pagination.

    This notebook searches for peer-reviewed publications on "open science",
    streams through results using `iterate()` (up to 500), and computes
    statistics on access rights, publishers, citation impact, and publication years.

    **What AIREloom provides over raw HTTP:**
    - `iterate()` is an async generator that yields typed `ResearchProduct` objects
      with automatic cursor-based pagination — no manual page/cursor management.
    - Typed field access: `product.bestAccessRight.label`,
      `product.indicators.citationImpact.citationCount` — IDE-autocompletable,
      validated by Pydantic.
    - Model validators: `title` is auto-populated from `mainTitle`; keywords strings
      are split into lists; PID objects expose `scheme` and `value`.

    *Switch to code view with Ctrl+. to see all code cells*
    """
    )
    return (mo,)


@app.cell
def _():
    """Setup — imports and constants."""
    from collections import Counter

    from aireloom import AireloomClient
    from aireloom.endpoints import ResearchProductsFilters

    SEARCH_TOPIC = "open science"
    MAX_PRODUCTS = 500

    filters = ResearchProductsFilters(
        search=SEARCH_TOPIC,
        type="publication",
        isPeerReviewed=True,
    )
    return AireloomClient, MAX_PRODUCTS, SEARCH_TOPIC, filters


@app.cell
async def _(AireloomClient, MAX_PRODUCTS, SEARCH_TOPIC, filters, mo):
    """Phase 1: Get total result count via single search."""
    mo.md("## 1. Getting total result count")

    async with AireloomClient() as client:
        page1 = await client.research_products.search(
            page=1, page_size=1, filters=filters
        )

    total = page1.header.numFound or 0

    mo.md(
        f"""
    **Total publications matching '{SEARCH_TOPIC}':** {total:,}

    Streaming up to {min(total, MAX_PRODUCTS):,} for analysis...
    """
    )
    return (total,)


@app.cell
async def _(AireloomClient, MAX_PRODUCTS, filters, mo):
    """Phase 2: Stream via iterate() and collect statistics."""
    mo.md("## 2. Streaming products and collecting statistics")

    from collections import Counter

    async with AireloomClient() as client:
        access_counter: Counter[str] = Counter()
        publisher_counter: Counter[str] = Counter()
        citation_classes: Counter[str] = Counter()
        year_counter: Counter[str] = Counter()
        with_doi = 0
        total_citations = 0
        count = 0

        async for product in client.research_products.iterate(
            page_size=100, filters=filters, sort_by="publicationDate DESC"
        ):
            count += 1

            access_label = (
                product.bestAccessRight.label if product.bestAccessRight else "Unknown"
            )
            access_counter[access_label] += 1

            if product.publisher:
                publisher_counter[product.publisher] += 1

            if product.indicators and product.indicators.citationImpact:
                ci = product.indicators.citationImpact
                if ci.citationCount is not None:
                    total_citations += ci.citationCount
                if ci.citationClass:
                    citation_classes[ci.citationClass] += 1

            if product.publicationDate and len(product.publicationDate) >= 4:
                year_counter[product.publicationDate[:4]] += 1

            has_doi = any(
                (pid.scheme or "").lower() == "doi" and pid.value
                for pid in (product.pids or [])
            )
            if has_doi:
                with_doi += 1

            if count >= MAX_PRODUCTS:
                break

    mo.md(f"**Collected {count:,} publications**")
    return (
        access_counter,
        citation_classes,
        count,
        publisher_counter,
        total_citations,
        with_doi,
        year_counter,
    )


@app.cell
def _(
    access_counter,
    citation_classes,
    count,
    mo,
    publisher_counter,
    total_citations,
    with_doi,
    year_counter,
):
    """Phase 3: Display statistics."""
    mo.md("## 3. Statistics")

    # Access rights table
    access_rows = [
        {
            "Access Right": label,
            "Count": cnt,
            "%": f"{cnt / count * 100:.1f}%",
        }
        for label, cnt in access_counter.most_common()
    ]
    access_table = mo.ui.table(access_rows, label="Access Rights Distribution")

    # Top publishers table
    publisher_rows = [
        {
            "Publisher": pub,
            "Count": cnt,
            "%": f"{cnt / count * 100:.1f}%",
        }
        for pub, cnt in publisher_counter.most_common(10)
    ]
    publisher_table = mo.ui.table(publisher_rows, label="Top 10 Publishers")

    # Citation class table
    citation_rows = [
        {
            "Class": cls,
            "Count": citation_classes.get(cls, 0),
            "%": f"{citation_classes.get(cls, 0) / count * 100:.1f}%",
        }
        for cls in ["C1", "C2", "C3", "C4", "C5"]
        if citation_classes.get(cls, 0)
    ]
    citation_table = (
        mo.ui.table(citation_rows, label="Citation Impact Classes (C1=top … C5=lowest)")
        if citation_rows
        else mo.md("*No citation class data available.*")
    )

    # Year distribution table
    year_rows = [
        {"Year": year, "Count": cnt} for year, cnt in year_counter.most_common(10)
    ]
    year_table = (
        mo.ui.table(year_rows, label="Publication Years (top 10)")
        if year_rows
        else mo.md("*No year data available.*")
    )

    # Summary
    summary = mo.md(
        f"""
    ### Summary
    - **Products analysed:** {count:,}
    - **With DOI:** {with_doi} ({with_doi / count * 100:.1f}%)
    - **Total citations (of sampled):** {total_citations:,}
    - **Avg citations/product:** {total_citations / count:.1f}
    """
    )

    mo.vstack(
        [
            mo.md("### Access Rights"),
            access_table,
            publisher_table,
            citation_table,
            year_table,
            summary,
        ]
    )
    return (
        access_table,
        citation_rows,
        citation_table,
        publisher_rows,
        publisher_table,
        summary,
        year_rows,
        year_table,
    )


@app.cell
async def _(AireloomClient, SEARCH_TOPIC, filters, mo):
    """Phase 4: Show sample product with typed field access."""
    mo.md("## 4. Sample product — typed field access")

    async with AireloomClient() as client:
        sample_page = await client.research_products.search(
            page=1, page_size=1, filters=filters
        )

    if not sample_page.results:
        mo.md("*No results found.*")
        return

    p = sample_page.results[0]

    fields = [
        ("title", repr(p.title)),
        ("type", repr(p.type)),
        (
            "bestAccessRight",
            repr(p.bestAccessRight) if p.bestAccessRight else "None",
        ),
        ("publisher", repr(p.publisher)),
        ("publicationDate", repr(p.publicationDate)),
        (
            "DOI",
            next(
                (
                    pid.value
                    for pid in (p.pids or [])
                    if (pid.scheme or "").lower() == "doi"
                ),
                "—",
            ),
        ),
    ]

    if p.indicators and p.indicators.citationImpact:
        ci = p.indicators.citationImpact
        fields.append(("citationCount", str(ci.citationCount)))
        fields.append(("citationClass", repr(ci.citationClass)))

    mo.md(
        "```\n"
        + "\n".join(f"  {name:<20s} = {value}" for name, value in fields)
        + "\n```\n\n"
        "*Compare to raw JSON: `product['bestAccessRight']['label']`, "
        "`product['indicator']['citationImpact']['citationCount']`*"
    )
    return (p,)


if __name__ == "__main__":
    app.run()
