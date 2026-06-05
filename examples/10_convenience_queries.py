"""Example: Convenience Queries — High-Level Research Workflows.

Demonstrates the convenience query functions in aireloom.queries, accessed via
session.queries. These compose the low-level client operations into common
research workflows with a single function call.

Run with: uv run examples/10_convenience_queries.py
"""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv(".env")

from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.table import Table  # noqa: E402

from aireloom.session import AireloomSession  # noqa: E402

console = Console()


async def main():
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print("[red]Missing credentials in .env[/red]")
        return

    async with AireloomSession(
        client_id=client_id, client_secret=client_secret
    ) as session:
        q = session.queries

        # ── 1. Look up papers by DOI ──────────────────────────────
        console.print(
            Panel(
                "[bold]queries.publications_by_doi[/bold]\n"
                "Fetch research products by one or more DOIs.",
                title="1. DOI Lookup",
                border_style="blue",
            )
        )
        papers = await q.publications_by_doi(
            session,
            "10.1038/s41586-024-07386-0",
            "10.1038/s41586-024-07891-0",
        )
        for paper in papers:
            console.print(f"  {paper}")
            console.print(
                f"    OA: {paper.is_open_access} | "
                f"Citations: {paper.citation_count} | "
                f"License: {paper.license}"
            )

        # ── 2. Publications by organization ───────────────────────
        console.print(
            Panel(
                "[bold]queries.publications_by_organization[/bold]\n"
                "Fetch publications for an organization, with type and date filters.\n"
                "search_on controls how the identifier is interpreted.",
                title="2. Org Publications",
                border_style="blue",
            )
        )
        pubs = await q.publications_by_organization(
            session,
            "University of Twente",
            search_on="name",
            type="publication",
            from_publication_date="2024-01-01",
            open_access_only=True,
            sort_by="publicationDate desc",
            limit=5,
        )
        console.print(f"  Found {len(pubs)} recent OA publications:")
        for pub in pubs:
            console.print(f"    {pub}")

        # ── 3. Publications by author ─────────────────────────────
        console.print(
            Panel(
                "[bold]queries.publications_by_author[/bold]\n"
                "Find publications by name or ORCID.\n"
                "search_on='orcid' uses authorOrcid filter.",
                title="3. Author Publications",
                border_style="blue",
            )
        )
        pubs = await q.publications_by_author(
            session,
            "0000-0002-3639-3956",
            search_on="orcid",
            limit=5,
        )
        console.print("  Publications by ORCID:0000-0002-3639-3956:")
        for pub in pubs:
            console.print(f"    {pub}")

        # ── 4. Publications by project ────────────────────────────
        console.print(
            Panel(
                "[bold]queries.publications_by_project[/bold]\n"
                "Find publications linked to a project by name, code, or ID.",
                title="4. Project Publications",
                border_style="blue",
            )
        )
        pubs = await q.publications_by_project(
            session,
            "OpenAIRE-Nexus",
            search_on="name",
            limit=3,
        )
        console.print("  Publications from OpenAIRE-Nexus:")
        for pub in pubs:
            console.print(f"    {pub}")

        # ── 5. Count publications ─────────────────────────────────
        console.print(
            Panel(
                "[bold]queries.count_publications[/bold]\n"
                "Count matching publications without downloading them.",
                title="5. Count",
                border_style="blue",
            )
        )

        counts_table = Table(title="Publication Counts")
        counts_table.add_column("Query", style="bold")
        counts_table.add_column("Count", justify="right", style="cyan")

        scenarios = [
            ("All publications", dict(type="publication")),
            ("All datasets", dict(type="dataset")),
            ("Open Access publications", dict(type="publication", open_access_only=True)),
            ("Machine learning", dict(search="machine learning")),
            ("Deep learning 2024+", dict(search="deep learning", type="publication")),
        ]
        for label, kwargs in scenarios:
            n = await q.count_publications(session, **kwargs)
            counts_table.add_row(label, f"{n:,}")
        console.print(counts_table)

        # ── 6. Projects by organization ───────────────────────────
        console.print(
            Panel(
                "[bold]queries.projects_by_organization[/bold]\n"
                "Fetch projects associated with an organization.",
                title="6. Org Projects",
                border_style="blue",
            )
        )
        projects = await q.projects_by_organization(
            session,
            "University of Twente",
            limit=5,
        )
        console.print(f"  UT projects ({len(projects)}):")
        for proj in projects:
            console.print(
                f"    {proj}  "
                f"[{proj.start_year}–{proj.end_year}]"
            )

        # ── 7. Citing works (Scholix) ─────────────────────────────
        console.print(
            Panel(
                "[bold]queries.citing_works[/bold]\n"
                "Find works that cite a given DOI, via Scholix.",
                title="7. Citing Works",
                border_style="blue",
            )
        )
        citations = await q.citing_works(
            session,
            "10.1038/s41586-024-07386-0",
            limit=5,
        )
        console.print(f"  Works citing the paper ({len(citations)}):")
        for cite in citations:
            console.print(f"    {cite}")

        # ── 8. Related datasets (Scholix) ─────────────────────────
        console.print(
            Panel(
                "[bold]queries.related_datasets[/bold]\n"
                "Find datasets linked to a publication DOI, via Scholix.",
                title="8. Related Datasets",
                border_style="blue",
            )
        )
        datasets = await q.related_datasets(
            session,
            "10.1038/s41586-024-07386-0",
            limit=5,
        )
        console.print(f"  Related datasets ({len(datasets)}):")
        for ds in datasets:
            console.print(f"    {ds}")

        # ── 9. All Scholix links ──────────────────────────────────
        console.print(
            Panel(
                "[bold]queries.all_links[/bold]\n"
                "Fetch all Scholix links for a DOI (as source, target, or both).",
                title="9. All Links",
                border_style="blue",
            )
        )
        links = await q.all_links(
            session,
            "10.1038/s41586-024-07386-0",
            direction="both",
            limit=10,
        )
        console.print(f"  Total Scholix links: {len(links)}")


if __name__ == "__main__":
    asyncio.run(main())
