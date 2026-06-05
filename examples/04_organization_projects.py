#!/usr/bin/env python3
"""
Organization Projects — Find an organization, their research products, and projects.

This example looks up an organization by name (e.g., 'University of Twente'),
retrieves their research products and projects using relOrganizationId filters,
and displays funding info from typed Project models.

Run with: uv run examples/04_organization_projects.py

What AIREloom provides over raw HTTP:
  - Type-safe filter models: relOrganizationId is a validated field on both
    ResearchProductsFilters and ProjectsFilters. Typos like 'relOrgId' are
    caught by Pydantic's extra='forbid' BEFORE the API call.
  - Nested model access: project.fundings[0].shortName, project.granted.fundedAmount,
    project.granted.currency — all typed and autocompletable.
  - Reusable AireloomClient context: one auth session handles multiple resource
    clients (organizations, research_products, projects) with shared connection pooling.
"""

import asyncio
import os
from collections import Counter

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aireloom import AireloomClient
from aireloom.endpoints import (
    OrganizationsFilters,
    ProjectsFilters,
    ResearchProductsFilters,
)

console = Console()

ORG_NAME = "University of Twente"


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
            f"Looking up: [bold cyan]{ORG_NAME}[/bold cyan]",
            title="Organization → Research Products & Projects",
            border_style="blue",
        )
    )

    async with AireloomClient(
        client_id=client_id, client_secret=client_secret
    ) as client:
        # --- Step 1: Find the organization ------------------------------------
        console.print(f"\n[yellow]1. Searching for organization '{ORG_NAME}'[/yellow]")
        org_filters = OrganizationsFilters(search=ORG_NAME)

        try:
            org_response = await client.organizations.search(
                page=1, page_size=5, filters=org_filters
            )
        except Exception as exc:
            console.print(f"[red]Organization search failed: {exc}[/red]")
            return

        if not org_response.results:
            console.print("[red]No organizations found.[/red]")
            return

        org = org_response.results[0]
        org_id = org.id
        console.print(f"   Found: [bold]{org.legalName}[/bold] (id: {org_id})")
        if org.country:
            console.print(f"   Country: {org.country.label} ({org.country.code})")
        if org.websiteUrl:
            console.print(f"   Website: {org.websiteUrl}")

        # --- Step 2: Research products linked to this org --------------------
        console.print(
            f"\n[yellow]2. Research products linked to "
            f"{org.legalShortName or ORG_NAME}[/yellow]"
        )
        rp_filters = ResearchProductsFilters(
            relOrganizationId=org_id,
            type="publication",
            isPeerReviewed=True,
        )

        try:
            rp_response = await client.research_products.search(
                page=1,
                page_size=10,
                filters=rp_filters,
                sort_by="publicationDate DESC",
            )
        except Exception as exc:
            console.print(f"[red]Research products search failed: {exc}[/red]")
            rp_response = None

        if rp_response:
            total_rp = rp_response.header.numFound or 0
            console.print(f"   Total publications: [bold]{total_rp:,}[/bold]")

            rp_table = Table(title="Recent Publications", border_style="dim")
            rp_table.add_column("Title", style="cyan", max_width=60)
            rp_table.add_column("Year", style="green", width=6)
            rp_table.add_column("Access", style="magenta", max_width=18)
            rp_table.add_column("Type", style="yellow", width=12)

            for product in (rp_response.results or [])[:10]:
                title = (product.title or "—")[:60]
                year = (product.publicationDate or "—")[:4]
                access = (
                    product.bestAccessRight.label if product.bestAccessRight else "—"
                )
                ptype = product.type or "—"
                rp_table.add_row(title, year, access, ptype)

            console.print(rp_table)

        # --- Step 3: Projects linked to this org -----------------------------
        console.print(
            f"\n[yellow]3. Projects linked to {org.legalShortName or ORG_NAME}[/yellow]"
        )
        proj_filters = ProjectsFilters(
            relOrganizationId=org_id,
        )

        try:
            proj_response = await client.projects.search(
                page=1,
                page_size=20,
                filters=proj_filters,
                sort_by="startDate DESC",
            )
        except Exception as exc:
            console.print(f"[red]Projects search failed: {exc}[/red]")
            proj_response = None

        if proj_response:
            total_proj = proj_response.header.numFound or 0
            console.print(f"   Total projects: [bold]{total_proj:,}[/bold]")

            proj_table = Table(
                title="Recent Projects", border_style="dim", show_lines=True
            )
            proj_table.add_column("Acronym", style="cyan", max_width=14)
            proj_table.add_column("Title", style="cyan", max_width=45)
            proj_table.add_column("Funding", style="green", max_width=20)
            proj_table.add_column("Period", style="yellow", max_width=18)
            proj_table.add_column("Grant", style="magenta", max_width=18)

            # Collect funding statistics
            funder_counter: Counter[str] = Counter()
            total_funding = 0.0
            currency = "EUR"

            for project in (proj_response.results or [])[:20]:
                acronym = project.acronym or "—"
                title = (project.title or "—")[:45]
                period = f"{project.startDate or '?'} → {project.endDate or '?'}"

                # Typed nested model access — project.fundings[0].shortName
                funder = "—"
                if project.fundings:
                    for f in project.fundings:
                        if f.shortName:
                            funder = f.shortName
                            funder_counter[f.shortName] += 1
                            break

                # Typed grant access — project.granted.fundedAmount, .currency
                grant_str = "—"
                if project.granted:
                    currency = project.granted.currency or "EUR"
                    if project.granted.fundedAmount is not None:
                        total_funding += project.granted.fundedAmount
                        grant_str = f"{project.granted.fundedAmount:,.0f} {currency}"
                    elif project.granted.totalCost is not None:
                        grant_str = f"Cost: {project.granted.totalCost:,.0f} {currency}"

                proj_table.add_row(acronym, title, funder, period, grant_str)

            console.print(proj_table)

            # Funding summary from typed models
            if funder_counter:
                console.print(
                    "\n[bold]Funder distribution (of displayed projects):[/bold]"
                )
                for funder, cnt in funder_counter.most_common():
                    console.print(f"  • {funder}: {cnt} projects")

            if total_funding > 0:
                console.print(
                    f"\n[bold]Total funded amount (displayed):[/bold] "
                    f"{total_funding:,.0f} {currency}"
                )

        # --- Show filter type safety -----------------------------------------
        console.print("\n[bold]Type-safe filter models:[/bold]")
        console.print("  [dim]Valid field names are enforced by Pydantic.[/dim]")
        console.print("  [dim]This would raise ValidationError at instantiation:[/dim]")
        console.print(
            "  [red]  ResearchProductsFilters(relOrgId='...')"
            "[/red]  # typo: should be relOrganizationId"
        )
        console.print(
            "  [green]  ResearchProductsFilters(relOrganizationId='...')[/green]  ✓"
        )


if __name__ == "__main__":
    asyncio.run(main())
