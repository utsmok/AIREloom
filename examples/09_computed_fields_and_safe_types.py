"""Example: Computed Fields & Safe Types.

Demonstrates the computed properties and safe defaults added to all entity models.
These eliminate common patterns of null-checking and manual data extraction.

Run with: uv run examples/09_computed_fields_and_safe_types.py
"""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv(".env")

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from aireloom import AireloomClient  # noqa: E402
from aireloom.endpoints import ResearchProductsFilters  # noqa: E402

console = Console()


async def main():
    client_id = os.getenv("AIRELOOM_OPENAIRE_CLIENT_ID")
    client_secret = os.getenv("AIRELOOM_OPENAIRE_CLIENT_SECRET")
    if not client_id or not client_secret:
        console.print("[red]Missing credentials in .env[/red]")
        return

    async with AireloomClient(client_id=client_id, client_secret=client_secret) as client:
        # Fetch a well-known paper
        paper = await client.research_products.get(
            "doi_________::07ac7530e7435e29ba33e5a74bec687d"
        )
        if not paper:
            # Fallback: search by DOI
            results = await client.research_products.collect(
                filters=ResearchProductsFilters(
                    pid="10.1038/s41586-024-07386-0"
                ),
                limit=1,
            )
            paper = results[0] if results else None

        if not paper:
            console.print("[red]Could not fetch paper[/red]")
            return

        # ── Safe Types: no more None checks ───────────────────────
        console.rule("[bold magenta]Safe Types — No More None Checks[/bold magenta]")

        console.print("\n[bold]Before Safe Types:[/bold]")
        console.print("  title = paper.title or 'Untitled'  # guard against None")
        console.print("  for author in paper.authors or []:  # guard against None")
        console.print("  keywords = paper.keywords if paper.keywords else []")

        console.print("\n[bold]With Safe Types (SafeStr, SafeList):[/bold]")
        console.print(f"  paper.title    → {paper.title!r}  (SafeStr: always str, never None)")
        console.print(f"  paper.authors  → list with {len(paper.authors)} items  (SafeList: always list)")
        console.print(f"  paper.keywords → {paper.keywords[:3]}  (SafeList: always list)")
        console.print(f"  len(paper.authors) works directly: {len(paper.authors)}")
        console.print(f"  iterating paper.authors never raises: {paper.author_names[:2]}")

        # ── Computed Fields on ResearchProduct ─────────────────────
        console.rule("[bold magenta]ResearchProduct Computed Fields[/bold magenta]")

        table = Table(title="ResearchProduct Computed Properties")
        table.add_column("Property", style="bold")
        table.add_column("Value")
        table.add_column("What it replaces")

        table.add_row(
            "doi",
            str(paper.doi),
            "Loop through pids to find scheme='doi'",
        )
        table.add_row(
            "all_dois",
            str(paper.all_dois),
            "Collect all pids with scheme='doi'",
        )
        table.add_row(
            "is_open_access",
            str(paper.is_open_access),
            "Check bestAccessRight.label == 'OPEN'",
        )
        table.add_row(
            "open_access_url",
            str(paper.open_access_url),
            "Search instances for OA access URL",
        )
        table.add_row(
            "citation_count",
            str(paper.citation_count),
            "Navigate indicators.citationImpact.citationCount",
        )
        table.add_row(
            "publication_year",
            str(paper.publication_year),
            "Parse publicationDate[:4] with error handling",
        )
        table.add_row(
            "journal_name",
            str(paper.journal_name),
            "Guard container.name against None",
        )
        table.add_row(
            "author_names",
            str(paper.author_names[:3]),
            "List comprehension with None filtering",
        )
        table.add_row(
            "license",
            str(paper.license),
            "Search instances for first non-empty license",
        )

        console.print(table)

        # ── __str__ and __repr__ ───────────────────────────────────
        console.rule("[bold magenta]__str__ & __repr__ — Human-Readable Output[/bold magenta]")

        console.print(f"\n  repr(paper): {paper!r}")
        console.print(f"  str(paper):  {paper}")
        console.print("  → No need to manually format: print(f'{title} ({year}) DOI:{doi}')")

        # Fetch other entities to show their __str__
        org = await client.organizations.first(
            filters={"search": "University of Twente"},
        )
        if org:
            console.print(f"\n  str(org):  {org}")
            console.print(f"  repr(org): {org!r}")

        project = await client.projects.first(
            filters={"search": "European"},
        )
        if project:
            console.print(f"\n  str(project):  {project}")
            console.print(
                f"  funder_name: {project.funder_name}, "
                f"period: {project.start_year}–{project.end_year}"
            )

        person = await client.persons.first(
            filters={"search": "machine learning"},
        )
        if person:
            console.print(f"\n  str(person): {person}")
            console.print(f"  full_name:   {person.full_name}")
            console.print(f"  orcid:       {person.orcid}")

        ds = await client.data_sources.first(
            filters={"search": "Zenodo"},
        )
        if ds:
            console.print(f"\n  str(datasource): {ds}")
            console.print(f"  type_name:       {ds.type_name}")

        # ── Organization computed fields ───────────────────────────
        if org:
            console.rule("[bold magenta]Organization Computed Fields[/bold magenta]")
            console.print(f"  ror_id:      {org.ror_id}")
            console.print(f"  country_code: {org.country_code}")

        # ── Person computed fields ─────────────────────────────────
        if person:
            console.rule("[bold magenta]Person Computed Fields[/bold magenta]")
            console.print(f"  full_name: {person.full_name}")
            console.print(f"  orcid:     {person.orcid}")


if __name__ == "__main__":
    asyncio.run(main())
