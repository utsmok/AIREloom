#!/usr/bin/env python3
"""
Scholix Link Discovery — Discover datasets linked to a publication DOI.

This example queries the Scholix (Scholexplorer) API to find all datasets
linked to a specific publication DOI, then displays the relationships in a
rich table showing source→target, relationship type, and providers.

Run with: uv run examples/02_scholix_link_discovery.py

What AIREloom provides over raw HTTP:
  - Typed ScholixRelationship objects with nested ScholixEntity, identifiers,
    and relationship types — no manual dict traversal.
  - ScholixFilters with Pydantic validation (sourcePid/targetPid enforced,
    extra='forbid' catches typos before the API call).
  - Async iteration via iterate_links() with automatic pagination — no manual
    page tracking or cursor juggling.
"""

import asyncio
import os
from collections import Counter

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aireloom import AireloomClient
from aireloom.endpoints import ScholixFilters

console = Console()

# A well-known publication DOI with 118+ Scholix links to related entities.
SOURCE_DOI = "10.1016/j.respol.2021.104226"


def _pid_str(identifiers: list, scheme: str = "doi") -> str:
    """Extract the first identifier matching a scheme, or the first available."""
    for pid in identifiers:
        s = getattr(pid, "id_scheme", "") or ""
        if s.lower() == scheme:
            return getattr(pid, "id_val", "")
    if identifiers:
        return getattr(identifiers[0], "id_val", "")
    return "—"


async def main() -> None:
    load_dotenv(".env")
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print("[red]Missing AIRELOOM_OPENAIRE_CLIENT_ID / CLIENT_SECRET in .env[/red]")
        return

    console.print(
        Panel(
            f"Discovering Scholix links for publication DOI:\n[bold cyan]{SOURCE_DOI}[/bold cyan]",
            title="Scholix Link Discovery",
            border_style="blue",
        )
    )

    async with AireloomClient(client_id=client_id, client_secret=client_secret) as client:
        # --- Step 1: search_links (single-page snapshot) -----------------------
        # ScholixFilters requires sourcePid or targetPid — Pydantic validates
        # field names. A typo like 'sorucePid' raises ValidationError instantly.
        filters = ScholixFilters(sourcePid=SOURCE_DOI, targetType="Dataset")

        console.print("\n[yellow]1. Single-page search (up to 20 results)[/yellow]")
        try:
            response = await client.scholix.search_links(
                page=0, page_size=20, filters=filters
            )
        except Exception as exc:
            console.print(f"[red]search_links failed: {exc}[/red]")
            return

        # Typed response: .total_links, .result (list[ScholixRelationship])
        total = response.total_links
        console.print(f"   Total linked datasets reported by Scholix: [bold]{total}[/bold]")
        console.print(f"   Retrieved in this page: {len(response.result)}")

        # --- Step 2: iterate_links (async generator over ALL pages) -----------
        console.print(
            "\n[yellow]2. Streaming ALL linked datasets via iterate_links()[/yellow]"
        )
        console.print("   [dim](AIREloom handles pagination automatically)[/dim]")

        links = []
        rel_type_counts: Counter[str] = Counter()
        try:
            async for rel in client.scholix.iterate_links(
                page_size=50, filters=filters
            ):
                links.append(rel)
                # Typed access to relationship_type.name — no dict key guessing.
                rel_name = rel.relationship_type.name
                rel_type_counts[rel_name] += 1
                if len(links) >= 100:  # cap for demo
                    break
        except Exception as exc:
            console.print(f"[red]iterate_links failed: {exc}[/red]")

        if not links:
            console.print("[yellow]No linked datasets found.[/yellow]")
            return

        # --- Step 3: Display results in a rich table -------------------------
        table = Table(
            title=f"Linked Datasets for {SOURCE_DOI}",
            show_lines=True,
            border_style="dim",
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Target Title", style="cyan", max_width=55)
        table.add_column("Target DOI", style="green", max_width=38)
        table.add_column("Relationship", style="magenta")
        table.add_column("Providers", style="yellow", max_width=30)

        for i, rel in enumerate(links[:20], 1):
            target = rel.target
            title = (target.title or "—")[:55]
            doi = _pid_str(target.identifier, "doi")
            rel_name = rel.relationship_type.name
            providers = ", ".join(
                p.name for p in (rel.link_provider or [])
            )[:30]
            table.add_row(str(i), title, doi, rel_name, providers)

        console.print(table)
        if len(links) > 20:
            console.print(f"   [dim]... and {len(links) - 20} more (capped for display)[/dim]")

        # --- Step 4: Summary statistics from typed model fields ---------------
        console.print("\n[bold]Relationship type distribution:[/bold]")
        for rel_name, count in rel_type_counts.most_common():
            console.print(f"  • {rel_name}: {count}")

        console.print(f"\n[bold]Total links collected:[/bold] {len(links)}")

        # Show a single link's structure to highlight typed access
        sample = links[0]
        console.print("\n[bold]Sample link — typed field access vs raw dict:[/bold]")
        console.print(f"  source.type       = {sample.source.type!r}")
        console.print(f"  source.title      = {sample.source.title!r}")
        console.print(f"  target.type       = {sample.target.type!r}")
        console.print(f"  relationship_type = {sample.relationship_type.name!r}")
        src_ids = sample.source.identifier
        if src_ids:
            console.print(
                f"  source PID        = {src_ids[0].id_scheme}:{src_ids[0].id_val}"
            )


if __name__ == "__main__":
    asyncio.run(main())
