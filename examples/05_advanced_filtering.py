#!/usr/bin/env python3
"""
Advanced Filtering — Complex filter combinations with Pydantic validation.

This example demonstrates building complex queries with multiple filter fields,
combining type/date/access/subject constraints, using sort parameters, and
showing how Pydantic validation catches mistakes before hitting the API.

Run with: uv run examples/05_advanced_filtering.py

What AIREloom provides over raw HTTP:
  - Pydantic filter models with extra='forbid': typos like 'fromDate' instead of
    'fromPublicationDate' raise ValidationError IMMEDIATELY — no silent 400 or
    unexpected empty results from the API.
  - Type-coerced fields: date fields accept datetime.date objects, bools are
    validated, Literal types constrain values to valid options.
  - Sort parameter validation via the library's endpoint definitions.
  - Multiple resource clients share one authenticated session — no manual token
    management or header injection.
"""

import asyncio
import os
from datetime import date

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aireloom import AireloomClient
from aireloom.endpoints import ProjectsFilters, ResearchProductsFilters, ScholixFilters

console = Console()


async def demo_research_products(client: AireloomClient) -> None:
    """Complex ResearchProductsFilters: type + date range + open access + subject."""
    console.print(
        "\n[bold cyan]━━━ Research Products: Multi-Field Filter ━━━[/bold cyan]"
    )

    # Build a complex filter combining multiple dimensions.
    # Each field is type-checked by Pydantic. 'fromPublicationDate' accepts date objects.
    # 'bestOpenAccessRightLabel' constrains to known labels.
    filters = ResearchProductsFilters(
        search="machine learning",
        type="publication",
        fromPublicationDate=date(2023, 1, 1),
        toPublicationDate=date(2024, 12, 31),
        bestOpenAccessRightLabel="OPEN",
        isPeerReviewed=True,
        subjects=["computer science"],
    )

    console.print("  [dim]Filters:[/dim]")
    console.print("    search = 'machine learning'")
    console.print("    type = 'publication'")
    console.print("    fromPublicationDate = 2023-01-01")
    console.print("    toPublicationDate = 2024-12-31")
    console.print("    bestOpenAccessRightLabel = 'OPEN'")
    console.print("    isPeerReviewed = True")
    console.print("    subjects = ['computer science']")

    try:
        response = await client.research_products.search(
            page=1,
            page_size=10,
            filters=filters,
            sort_by="publicationDate DESC",
        )
    except Exception as exc:
        console.print(f"[red]Search failed: {exc}[/red]")
        return

    total = response.header.numFound or 0
    console.print(f"\n  Results: [bold]{total:,}[/bold] matching publications\n")

    table = Table(title="Open Access ML Publications (2023-2024)", border_style="dim")
    table.add_column("Title", style="cyan", max_width=55)
    table.add_column("DOI", style="green", max_width=32)
    table.add_column("Date", style="yellow", width=12)
    table.add_column("Publisher", style="magenta", max_width=22)

    for product in (response.results or [])[:10]:
        title = (product.title or "—")[:55]
        doi = "—"
        if product.pids:
            for pid in product.pids:
                if (pid.scheme or "").lower() == "doi":
                    doi = pid.value or "—"
                    break
        pub_date = product.publicationDate or "—"
        publisher = (product.publisher or "—")[:22]
        table.add_row(title, doi, pub_date, publisher)

    console.print(table)

    # Show how iterate() works with these filters (brief sample)
    console.print("\n  [dim]Streaming first 5 via iterate() with same filters:[/dim]")
    count = 0
    try:
        async for product in client.research_products.iterate(
            page_size=50, filters=filters, sort_by="publicationDate DESC"
        ):
            count += 1
            console.print(f"    {count}. {product.title}")
            if count >= 5:
                break
    except Exception as exc:
        console.print(f"    [red]iterate error: {exc}[/red]")


async def demo_ec_projects(client: AireloomClient) -> None:
    """ProjectsFilters: fundingShortName + date range + sort."""
    console.print(
        "\n[bold cyan]━━━ Projects: EC Funding with Date Range ━━━[/bold cyan]"
    )

    # Filter for European Commission-funded projects started in 2023+
    filters = ProjectsFilters(
        fundingShortName="EC",
        fromStartDate=date(2023, 1, 1),
        toStartDate=date(2024, 12, 31),
    )

    console.print("  [dim]Filters:[/dim]")
    console.print("    fundingShortName = 'EC'")
    console.print("    fromStartDate = 2023-01-01")
    console.print("    toStartDate = 2024-12-31")

    try:
        response = await client.projects.search(
            page=1, page_size=10, filters=filters, sort_by="startDate DESC"
        )
    except Exception as exc:
        console.print(f"[red]Search failed: {exc}[/red]")
        return

    total = response.header.numFound or 0
    console.print(
        f"\n  Results: [bold]{total:,}[/bold] EC-funded projects starting 2023-2024\n"
    )

    table = Table(
        title="Recent EC-Funded Projects", border_style="dim", show_lines=True
    )
    table.add_column("Acronym", style="cyan", max_width=14)
    table.add_column("Title", style="cyan", max_width=50)
    table.add_column("Code", style="green", max_width=14)
    table.add_column("Start → End", style="yellow", width=22)
    table.add_column("Funded", style="magenta", max_width=16)

    for project in (response.results or [])[:10]:
        acronym = project.acronym or "—"
        title = (project.title or "—")[:50]
        code = project.code or "—"
        period = f"{project.startDate or '?'} → {project.endDate or '?'}"
        funded = "—"
        if project.granted and project.granted.fundedAmount is not None:
            curr = project.granted.currency or "EUR"
            funded = f"{project.granted.fundedAmount:,.0f} {curr}"
        table.add_row(acronym, title, code, period, funded)

    console.print(table)


async def demo_validation_errors() -> None:
    """Show that Pydantic catches invalid filter values at instantiation."""
    console.print(
        "\n[bold cyan]━━━ Pydantic Validation: Catching Errors Early ━━━[/bold cyan]"
    )

    # --- Typo in field name ---
    console.print("\n  [yellow]1. Typo in filter field name:[/yellow]")
    console.print('    ResearchProductsFilters(tipe="publication")  # wrong key')
    try:
        ResearchProductsFilters(tipe="publication")  # type: ignore[call-arg]
    except Exception as exc:
        console.print(f"    [green]✓ Caught instantly:[/green] {type(exc).__name__}")
        console.print(f"    [dim]{exc}[/dim]")

    # --- Invalid literal value ---
    console.print("\n  [yellow]2. Invalid literal value for 'type':[/yellow]")
    console.print('    ResearchProductsFilters(type="journal")  # not a valid type')
    try:
        ResearchProductsFilters(type="journal")  # type: ignore[call-arg]
    except Exception as exc:
        console.print(f"    [green]✓ Caught instantly:[/green] {type(exc).__name__}")
        console.print(f"    [dim]{exc}[/dim]")

    # --- Invalid date type ---
    console.print("\n  [yellow]3. Wrong type for date field:[/yellow]")
    console.print('    ResearchProductsFilters(fromPublicationDate="last year")')
    try:
        ResearchProductsFilters(fromPublicationDate="last year")  # type: ignore[arg-type]
    except Exception as exc:
        console.print(f"    [green]✓ Caught instantly:[/green] {type(exc).__name__}")
        console.print(f"    [dim]{exc}[/dim]")

    # --- Extra field (forbidden by config) ---
    console.print("\n  [yellow]4. Unknown field (extra='forbid'):[/yellow]")
    console.print('    ScholixFilters(sourceDOI="10.1234/x")  # should be sourcePid')
    try:
        ScholixFilters(sourceDOI="10.1234/x")  # type: ignore[call-arg]
    except Exception as exc:
        console.print(f"    [green]✓ Caught instantly:[/green] {type(exc).__name__}")
        console.print(f"    [dim]{exc}[/dim]")

    console.print(
        "\n  [bold green]All invalid inputs caught BEFORE any API call.[/bold green]"
    )
    console.print("  With raw HTTP, these would either silently return empty results")
    console.print("  or produce confusing 400 errors from the server.")


async def main() -> None:
    load_dotenv(".env")
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print(
            "[red]Missing AIRELOOM_OPENAIRE_CLIENT_ID / CLIENT_SECRET in .env[/red]"
        )
        return

    console.print(
        Panel(
            "Complex filters + sort + Pydantic validation",
            title="Advanced Filtering Demo",
            border_style="blue",
        )
    )

    async with AireloomClient(
        client_id=client_id, client_secret=client_secret
    ) as client:
        await demo_research_products(client)
        await demo_ec_projects(client)

    # Validation demo doesn't need a client
    await demo_validation_errors()


if __name__ == "__main__":
    asyncio.run(main())
