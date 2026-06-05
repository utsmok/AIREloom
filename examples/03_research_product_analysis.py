#!/usr/bin/env python3
"""
Research Product Analysis — Streaming analysis of 'open science' publications.

This example searches for research products on a topic, streams through results
using iterate() (cursor-based pagination), extracts typed fields (DOIs, access
rights, impact indicators), and computes basic statistics.

Run with: uv run examples/03_research_product_analysis.py

What AIREloom provides over raw HTTP:
  - iterate() is an async generator that yields typed ResearchProduct objects
    with automatic cursor-based pagination — no manual page/cursor management.
  - Typed field access: product.bestAccessRight.label, product.indicators.citationImpact.citationCount
    etc. — IDE-autocompletable, validated by Pydantic.
  - Model validators: title is auto-populated from mainTitle; keywords strings
    are split into lists; PID objects expose scheme and value.
"""

import asyncio
import os
from collections import Counter

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aireloom import AireloomClient
from aireloom.endpoints import ResearchProductsFilters

console = Console()

SEARCH_TOPIC = "open science"
MAX_PRODUCTS = 500  # cap for demo


def _doi(product) -> str:
    """Extract first DOI from a ResearchProduct's pids list."""
    if product.pids:
        for pid in product.pids:
            if (pid.scheme or "").lower() == "doi":
                return pid.value or ""
    return "—"


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
            f"Streaming & analysing research products for: [bold cyan]{SEARCH_TOPIC}[/bold cyan]",
            title="Research Product Analysis",
            border_style="blue",
        )
    )

    # Typed filter model — extra='forbid' catches typos like 'tipe' or 'publishr'.
    filters = ResearchProductsFilters(
        search=SEARCH_TOPIC,
        type="publication",
        isPeerReviewed=True,
    )

    async with AireloomClient(
        client_id=client_id, client_secret=client_secret
    ) as client:
        # --- Phase 1: Get total count via single search ----------------------
        console.print("\n[yellow]1. Getting total result count[/yellow]")
        try:
            page1 = await client.research_products.search(
                page=1, page_size=1, filters=filters
            )
            total = page1.header.numFound or 0
        except Exception as exc:
            console.print(f"[red]search failed: {exc}[/red]")
            return

        console.print(
            f"   Total publications matching '{SEARCH_TOPIC}': [bold]{total:,}[/bold]"
        )
        cap = min(total, MAX_PRODUCTS)
        console.print(f"   Streaming up to {cap} for analysis...\n")

        # --- Phase 2: Stream via iterate() -----------------------------------
        # iterate() yields individual ResearchProduct objects — fully typed.
        access_counter: Counter[str] = Counter()
        publisher_counter: Counter[str] = Counter()
        citation_classes: Counter[str] = Counter()
        year_counter: Counter[str] = Counter()
        with_doi = 0
        total_citations = 0
        count = 0

        try:
            async for product in client.research_products.iterate(
                page_size=100, filters=filters, sort_by="publicationDate DESC"
            ):
                count += 1

                # Typed access to bestAccessRight.label — not dict['bestAccessRight']['label']
                access_label = (
                    product.bestAccessRight.label
                    if product.bestAccessRight
                    else "Unknown"
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

                if _doi(product) != "—":
                    with_doi += 1

                if count >= MAX_PRODUCTS:
                    break
        except Exception as exc:
            console.print(f"[red]iterate failed after {count} items: {exc}[/red]")

        if count == 0:
            console.print("[yellow]No products collected.[/yellow]")
            return

        # --- Phase 3: Display statistics ------------------------------------
        console.print(f"[bold]Collected {count:,} publications[/bold]\n")

        # Access rights table
        access_table = Table(title="Access Rights Distribution", border_style="dim")
        access_table.add_column("Access Right", style="cyan")
        access_table.add_column("Count", justify="right", style="green")
        access_table.add_column("%", justify="right", style="yellow")
        for label, cnt in access_counter.most_common():
            pct = cnt / count * 100
            style = "bold green" if "open" in label.lower() else None
            access_table.add_row(label, f"{cnt:,}", f"{pct:.1f}%", style=style)
        console.print(access_table)

        # Top publishers
        console.print("\n[bold]Top 10 Publishers:[/bold]")
        for pub, cnt in publisher_counter.most_common(10):
            console.print(f"  • {pub}: {cnt} ({cnt / count * 100:.1f}%)")

        # Citation class distribution
        if citation_classes:
            console.print(
                "\n[bold]Citation Impact Classes (C1=top … C5=lowest):[/bold]"
            )
            for cls in ["C1", "C2", "C3", "C4", "C5"]:
                cnt = citation_classes.get(cls, 0)
                if cnt:
                    console.print(f"  • {cls}: {cnt} ({cnt / count * 100:.1f}%)")

        # Publication year distribution (top years)
        if year_counter:
            console.print("\n[bold]Publication Years (top 10):[/bold]")
            for year, cnt in year_counter.most_common(10):
                console.print(f"  • {year}: {cnt}")

        # Summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"  • Products analysed: {count:,}")
        console.print(f"  • With DOI: {with_doi} ({with_doi / count * 100:.1f}%)")
        console.print(f"  • Total citations (of sampled): {total_citations:,}")
        console.print(f"  • Avg citations/product: {total_citations / count:.1f}")

        # Show typed field access on a single product for comparison
        console.print("\n[bold]Sample product — typed field access:[/bold]")
        console.print(
            "  [dim](vs raw JSON: product['bestAccessRight']['label'], "
            "product['indicator']['citationImpact']['citationCount'])[/dim]"
        )
        try:
            sample_page = await client.research_products.search(
                page=1, page_size=1, filters=filters
            )
            if sample_page.results:
                p = sample_page.results[0]
                console.print(f"  title             = {p.title!r}")
                console.print(f"  type              = {p.type!r}")
                console.print(
                    f"  bestAccessRight   = {p.bestAccessRight!r}"
                    if p.bestAccessRight
                    else "  bestAccessRight   = None"
                )
                console.print(f"  publisher         = {p.publisher!r}")
                console.print(f"  publicationDate   = {p.publicationDate!r}")
                console.print(f"  DOI               = {_doi(p)}")
                if p.indicators and p.indicators.citationImpact:
                    ci = p.indicators.citationImpact
                    console.print(f"  citationCount     = {ci.citationCount}")
                    console.print(f"  citationClass     = {ci.citationClass}")
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
