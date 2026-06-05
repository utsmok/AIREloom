"""Example: Iterator Helpers — collect(), count(), first().

Demonstrates the iterator helpers added to all resource clients via bibliofabric.
These helpers build on top of iterate() and search() to provide common patterns
with less boilerplate.

Run with: uv run examples/08_iterator_helpers.py
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
    ProjectsFilters,
    ResearchProductsFilters,
)

console = Console()


async def main():
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print("[red]Missing credentials in .env[/red]")
        return

    async with AireloomClient(client_id=client_id, client_secret=client_secret) as client:
        # ── count() — zero-download tallying ──────────────────────
        console.rule("[bold cyan]count() — Get totals without downloading results[/bold cyan]")

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

        console.print(f"  Total publications:      {total_pubs:>10,}")
        console.print(f"  Total datasets:          {total_datasets:>10,}")
        console.print(f"  Open Access publications: {total_oa:>10,}")
        console.print(f"  Machine learning results: {total_ml:>10,}")
        console.print(
            f"  OA ratio: {total_oa / total_pubs:.1%}"
            if total_pubs
            else "  OA ratio: N/A"
        )

        # ── first() — grab exactly one result ─────────────────────
        console.rule("[bold cyan]first() — Get the top result[/bold cyan]")

        paper = await client.research_products.first(
            filters=ResearchProductsFilters(
                search="transformer architecture",
                type="publication",
            ),
            sort_by="publicationDate desc",
        )
        if paper:
            console.print(f"  Latest transformer paper: {paper}")
            console.print(f"  DOI:     {paper.doi}")
            console.print(f"  Year:    {paper.publication_year}")
            console.print(f"  Authors: {', '.join(paper.author_names[:3])}")
        else:
            console.print("  [yellow]No results found[/yellow]")

        org = await client.organizations.first(
            filters=OrganizationsFilters(search="CERN"),
        )
        if org:
            console.print(f"\n  Top CERN match: {org}")
            console.print(f"  Country: {org.country_code}")
            console.print(f"  ROR:     {org.ror_id}")

        project = await client.projects.first(
            filters=ProjectsFilters(search="quantum computing"),
            sort_by="startDate desc",
        )
        if project:
            console.print(f"\n  Latest quantum project: {project}")
            console.print(f"  Funder:  {project.funder_name}")
            console.print(f"  Period:  {project.start_year}–{project.end_year}")

        # ── collect() — materialize iteration into a list ──────────
        console.rule("[bold cyan]collect() — Materialize results with optional limit[/bold cyan]")

        # Collect up to 5 recent software products
        software = await client.research_products.collect(
            filters=ResearchProductsFilters(
                type="software",
                fromPublicationDate="2024-01-01",
            ),
            sort_by="publicationDate desc",
            limit=5,
        )
        console.print(f"  Collected {len(software)} software packages:")
        for sw in software:
            name = sw.title[:50]
            lang = sw.programmingLanguage or "unknown"
            repo = sw.codeRepositoryUrl or "no repo"
            console.print(f"    {name} ({lang})")
            console.print(f"      Repo: {repo}")

        # Collect projects for an organization
        dutch_projects = await client.projects.collect(
            filters=ProjectsFilters(search="artificial intelligence"),
            limit=5,
        )
        console.print(f"\n  AI-related projects ({len(dutch_projects)}):")
        for proj in dutch_projects:
            console.print(f"    {proj}")

        # ── Summary table ─────────────────────────────────────────
        console.rule("[bold cyan]Summary[/bold cyan]")

        table = Table(title="Iterator Helper API")
        table.add_column("Helper", style="bold")
        table.add_column("Returns", style="cyan")
        table.add_column("Use case")
        table.add_row("count()", "int", "Get total results without downloading data")
        table.add_row("first()", "Entity | None", "Grab the single top match")
        table.add_row(
            "collect()",
            "list[Entity]",
            "Materialize iteration into a list, with optional limit",
        )
        table.add_row(
            "iterate()",
            "AsyncIterator[Entity]",
            "Stream results one-by-one (cursor or page-based)",
        )
        table.add_row("search()", "ApiResponse", "Paginated search with header metadata")
        table.add_row("get()", "Entity", "Fetch a single entity by ID")

        console.print(table)


if __name__ == "__main__":
    asyncio.run(main())
