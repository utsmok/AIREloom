"""Example: AIREloom Ergonomics Layer — Before & After.

Demonstrates the difference between raw API usage and the ergonomics layer
(computed fields, safe types, convenience queries, iterator helpers).

Run with: uv run examples/07_ergonomics_showcase.py
"""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv(".env")

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from aireloom import AireloomClient  # noqa: E402
from aireloom.endpoints import (  # noqa: E402
    OrganizationsFilters,
    ResearchProductsFilters,
)
from aireloom.session import AireloomSession  # noqa: E402

console = Console()
DOI = "10.1038/s41586-024-07386-0"  # A real paper to query


async def raw_api_usage(client: AireloomClient) -> None:
    """Traditional API usage — manually handling missing data, building filters."""
    console.rule("[bold red]Traditional API Usage[/bold red]")

    # --- Fetch a paper by DOI ---
    console.print("\n[bold]1. Fetch a paper by DOI[/bold]")
    resp = await client.research_products.search(
        page=1,
        page_size=1,
        filters=ResearchProductsFilters(pid=DOI),
    )
    results = resp.results or []
    if not results:
        console.print("  [red]No results found[/red]")
        return

    paper = results[0]

    # Manually extract DOI from pids list
    doi = None
    for pid in (paper.pids or []):
        if (pid.scheme or "").lower() == "doi" and pid.value:
            doi = pid.value
            break
    console.print(f"  DOI (manual extraction): {doi}")

    # Manually check open access
    is_oa = (
        paper.bestAccessRight
        and paper.bestAccessRight.label
        and paper.bestAccessRight.label.upper() == "OPEN"
    )
    console.print(f"  Is Open Access (manual check): {is_oa}")

    # Manually find open access URL
    oa_url = None
    for inst in (paper.instances or []):
        if (
            inst.accessRight
            and inst.accessRight.label
            and inst.accessRight.label.upper() == "OPEN"
            and inst.urls
        ):
            oa_url = inst.urls[0]
            break
    console.print(f"  OA URL (manual search): {oa_url}")

    # Manually extract citation count (deeply nested, each level may be None)
    citation_count = None
    if paper.indicators:  # noqa: SIM102
        if paper.indicators.citationImpact:
            citation_count = paper.indicators.citationImpact.citationCount
    console.print(f"  Citation count (manual nesting): {citation_count}")

    # Manually get author names
    author_names = []
    for author in (paper.authors or []):
        if author.fullName:
            author_names.append(author.fullName)  # noqa: PERF401
    console.print(f"  Authors (manual loop): {author_names[:3]}")

    # Manually extract journal name
    journal = None
    if paper.container and paper.container.name:
        journal = paper.container.name
    console.print(f"  Journal (manual guard): {journal}")

    # --- Fetch publications for an organization ---
    console.print("\n[bold]2. Publications by organization[/bold]")
    org_resp = await client.organizations.search(
        page=1,
        page_size=1,
        filters=OrganizationsFilters(search="University of Twente"),
    )
    orgs = org_resp.results or []
    if orgs:
        org_id = orgs[0].id
        pub_resp = await client.research_products.search(
            page=1,
            page_size=5,
            filters=ResearchProductsFilters(
                relOrganizationId=org_id,
                type="publication",
                fromPublicationDate="2024-01-01",
            ),
        )
        pubs = pub_resp.results or []
        console.print(f"  Found {pub_resp.header.numFound if pub_resp.header else 0} publications")
        for pub in pubs[:3]:
            # Manual title extraction (may be None)
            title = pub.title or pub.mainTitle or "Untitled"
            console.print(f"  - {title[:60]}")


async def ergonomics_usage(session: AireloomSession) -> None:
    """Ergonomics layer — computed fields, safe defaults, convenience queries."""
    console.rule("[bold green]Ergonomics Layer Usage[/bold green]")

    # --- Fetch papers by DOI with convenience query ---
    console.print("\n[bold]1. Fetch a paper by DOI[/bold]")
    papers = await session.queries.publications_by_doi(session, DOI)
    if not papers:
        console.print("  [red]No results found[/red]")
        return

    paper = papers[0]

    # Computed fields — no manual extraction needed
    console.print(f"  DOI:           {paper.doi}")
    console.print(f"  Is Open Access: {paper.is_open_access}")
    console.print(f"  OA URL:        {paper.open_access_url}")
    console.print(f"  Citation count: {paper.citation_count}")
    console.print(f"  Authors:       {paper.author_names[:3]}")
    console.print(f"  Journal:       {paper.journal_name}")
    console.print(f"  Year:          {paper.publication_year}")
    console.print(f"  License:       {paper.license}")

    # Safe defaults — title is always a string, never None
    console.print(f"\n  Title (safe):  {paper.title[:60]}")

    # __str__ gives a human-readable summary
    console.print(f"  str():         {paper}")

    # --- Convenience queries ---
    console.print("\n[bold]2. Publications by organization[/bold]")
    pubs = await session.queries.publications_by_organization(
        session,
        "University of Twente",
        type="publication",
        from_publication_date="2024-01-01",
        limit=5,
    )
    console.print(f"  Retrieved {len(pubs)} publications")
    for pub in pubs[:3]:
        # Computed fields + __str__ make this trivial
        console.print(f"  - {pub}")

    # --- Count ---
    console.print("\n[bold]3. Count publications[/bold]")
    count = await session.queries.count_publications(
        session,
        type="publication",
        open_access_only=True,
        search="machine learning",
    )
    console.print(f"  Open Access ML publications: {count:,}")

    # --- Author lookup ---
    console.print("\n[bold]4. Publications by author ORCID[/bold]")
    pubs = await session.queries.publications_by_author(
        session,
        "0000-0002-3639-3956",
        search_on="orcid",
        limit=3,
    )
    for pub in pubs:
        console.print(f"  - {pub}")

    # --- Scholix links ---
    console.print("\n[bold]5. Related datasets for a paper[/bold]")
    datasets = await session.queries.related_datasets(session, DOI, limit=5)
    console.print(f"  Found {len(datasets)} related datasets")
    for ds in datasets[:3]:
        console.print(f"  - {ds}")


async def side_by_side(client: AireloomClient, session: AireloomSession) -> None:
    """Side-by-side comparison table."""
    console.rule("[bold yellow]Side-by-Side Comparison[/bold yellow]")

    table = Table(title="Raw API vs Ergonomics Layer")
    table.add_column("Task", style="bold")
    table.add_column("Raw API", style="red")
    table.add_column("Ergonomics", style="green")

    table.add_row(
        "Get DOI",
        "for pid in pids:\n    if pid.scheme == 'doi'...",
        "paper.doi",
    )
    table.add_row(
        "Check OA",
        "bestAccessRight and\nbestAccessRight.label\n== 'OPEN'",
        "paper.is_open_access",
    )
    table.add_row(
        "OA URL",
        "for inst in instances:\n    if inst.accessRight...",
        "paper.open_access_url",
    )
    table.add_row(
        "Citations",
        "indicators and\nindicators.citationImpact\nand .citationCount",
        "paper.citation_count",
    )
    table.add_row(
        "Authors",
        "[a.fullName for a in\nauthors if a.fullName]",
        "paper.author_names",
    )
    table.add_row(
        "Journal",
        "container and\ncontainer.name or None",
        "paper.journal_name",
    )
    table.add_row(
        "Year",
        "int(publicationDate[:4])\nwith try/except",
        "paper.publication_year",
    )
    table.add_row(
        "License",
        "for inst in instances:\n    if inst.license...",
        "paper.license",
    )
    table.add_row(
        "Org pubs",
        "search org → get id\n→ search products\nwith filters",
        "queries.publications_by_\norganization(session, name)",
    )
    table.add_row(
        "Count",
        "search with pageSize=0\n→ header.numFound",
        "queries.count_publications(\nsession, ...)",
    )
    table.add_row(
        "Display",
        "product.title or\n'Untitled'",
        "str(product)",
    )
    table.add_row(
        "Null safety",
        "if x is not None:\n    for item in x or []:",
        "SafeList defaults to []\nSafeStr defaults to ''",
    )

    console.print(table)


async def main():
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print("[red]Missing credentials in .env[/red]")
        return

    # Both approaches use the same client under the hood
    async with AireloomClient(client_id=client_id, client_secret=client_secret) as client:
        session = AireloomSession(client_id=client_id, client_secret=client_secret)
        try:
            await raw_api_usage(client)
            console.print()
            await ergonomics_usage(session)
            console.print()
            await side_by_side(client, session)
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(main())
