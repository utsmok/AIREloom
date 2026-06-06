#!/usr/bin/env python3
"""Comprehensive analysis of University of Twente research output via OpenAIRE.

Fetches publications, projects, and Scholix links for UT, stores them in
DuckDB, runs analytics, and produces matplotlib visualisations.

Run with:
    uv run --group analysis examples/comprehensive_analysis.py
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import polars as pl
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from aireloom import AireloomSession, Project, ResearchProduct, ScholixRelationship
from aireloom.queries import count_publications

# ── Configuration ──────────────────────────────────────────────────────────

UT_ORG_ID = "openorgs____::604881198363fedbb5d5478f465305f2"
OUTPUT_DIR = Path("output")
DB_PATH = OUTPUT_DIR / "analysis.duckdb"
PUBLICATION_LIMIT = 500
PROJECT_LIMIT = 200
TOP_CITED_SAMPLE = 5
SCHOLIX_LIMIT_PER_PAPER = 50

console = Console()

# ── DuckDB schema & storage ────────────────────────────────────────────────

_PUB_SCHEMA = """
    id              VARCHAR PRIMARY KEY,
    title           VARCHAR,
    doi             VARCHAR,
    type            VARCHAR,
    publication_date VARCHAR,
    publication_year INTEGER,
    publisher       VARCHAR,
    language        VARCHAR,
    is_open_access  BOOLEAN,
    open_access_url VARCHAR,
    citation_count  INTEGER,
    journal_name    VARCHAR,
    license         VARCHAR,
    author_names    VARCHAR,
    subjects        VARCHAR,
    keywords        VARCHAR"""

_PROJ_SCHEMA = """
    id              VARCHAR PRIMARY KEY,
    title           VARCHAR,
    code            VARCHAR,
    acronym         VARCHAR,
    start_date      VARCHAR,
    end_date        VARCHAR,
    start_year      INTEGER,
    end_year        INTEGER,
    summary         VARCHAR,
    funder_name     VARCHAR,
    funders         VARCHAR,
    keywords        VARCHAR,
    oa_mandate_pub  BOOLEAN,
    oa_mandate_data BOOLEAN"""

_SCHOLIX_SCHEMA = """
    id              INTEGER PRIMARY KEY DEFAULT nextval('scholix_seq'),
    source_doi      VARCHAR,
    source_type     VARCHAR,
    source_title    VARCHAR,
    target_doi      VARCHAR,
    target_type     VARCHAR,
    target_title    VARCHAR,
    relationship    VARCHAR,
    link_provider   VARCHAR,
    publication_doi VARCHAR"""


def _init_db(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("CREATE SEQUENCE IF NOT EXISTS scholix_seq START 1")
    for name, schema in [
        ("publications", _PUB_SCHEMA),
        ("projects", _PROJ_SCHEMA),
        ("scholix_links", _SCHOLIX_SCHEMA),
    ]:
        con.execute(f"CREATE TABLE IF NOT EXISTS {name} ({schema})")


def _pub_to_row(p: ResearchProduct) -> dict:
    subjects = "; ".join(
        " ".join(s.subject.values()) if isinstance(s.subject, dict) else ""
        for s in p.subjects
        if s.subject
    )
    return {
        "id": p.id,
        "title": p.title[:500],
        "doi": p.doi,
        "type": p.type,
        "publication_date": p.publicationDate or "",
        "publication_year": p.publication_year,
        "publisher": p.publisher,
        "language": p.language.code,
        "is_open_access": p.is_open_access,
        "open_access_url": p.open_access_url,
        "citation_count": p.citation_count,
        "journal_name": p.journal_name,
        "license": p.license,
        "author_names": "; ".join(p.author_names),
        "subjects": subjects,
        "keywords": "; ".join(p.keywords),
    }


def _proj_to_row(pr: Project) -> dict:
    funders = "; ".join(
        f.shortName or f.name or "" for f in pr.fundings if f.shortName or f.name
    )
    return {
        "id": pr.id,
        "title": pr.title[:500],
        "code": pr.code or "",
        "acronym": pr.acronym,
        "start_date": pr.startDate or "",
        "end_date": pr.endDate or "",
        "start_year": pr.start_year,
        "end_year": pr.end_year,
        "summary": pr.summary[:1000],
        "funder_name": pr.funder_name,
        "funders": funders,
        "keywords": "; ".join(pr.keywords),
        "oa_mandate_pub": pr.openAccessMandateForPublications,
        "oa_mandate_data": pr.openAccessMandateForDataset,
    }


def _store_batch(
    con: duckdb.DuckDBPyConnection,
    table: str,
    rows: list[dict],
    clear: bool = True,
) -> None:
    if not rows:
        return
    df = pl.DataFrame(rows)
    if clear:
        con.execute(f"DELETE FROM {table}")
    con.execute(f"INSERT INTO {table} SELECT * FROM df")


def _store_scholix(
    con: duckdb.DuckDBPyConnection,
    links: list[ScholixRelationship],
    publication_doi: str,
) -> None:
    rows = []
    for lk in links:
        rows.append(
            {
                "source_doi": "; ".join(i.id_val for i in lk.source.identifier),
                "source_type": lk.source.type,
                "source_title": lk.source.title[:300],
                "target_doi": "; ".join(i.id_val for i in lk.target.identifier),
                "target_type": lk.target.type,
                "target_title": lk.target.title[:300],
                "relationship": lk.relationship_type.name,
                "link_provider": "; ".join(
                    lp.name for lp in (lk.link_provider or []) if lp.name
                ),
                "publication_doi": publication_doi,
            }
        )
    _store_batch(con, "scholix_links", rows, clear=False)


# ── Data retrieval ─────────────────────────────────────────────────────────


async def fetch_data(con: duckdb.DuckDBPyConnection) -> dict:
    """Fetch all data from OpenAIRE / Scholix and persist to DuckDB."""
    data: dict = {}

    async with AireloomSession() as session:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=console,
        ) as progress:
            # Quick counts
            t = progress.add_task("Counting UT publications…", total=None)
            total_pubs = await count_publications(
                session, rel_organization_id=UT_ORG_ID
            )
            total_oa = await count_publications(
                session, rel_organization_id=UT_ORG_ID, open_access_only=True
            )
            progress.update(
                t,
                completed=1,
                total=1,
                description=f"UT: {total_pubs:,} pubs ({total_oa:,} OA)",
            )
            data["total_publications"] = total_pubs
            data["total_open_access"] = total_oa

            # Publications
            t = progress.add_task(
                f"Fetching {PUBLICATION_LIMIT} publications…", total=None
            )
            publications = await session.queries.publications_by_organization(
                UT_ORG_ID,
                search_on="openaire_id",
                from_publication_date="2024-01-01",
                sort_by="publicationDate desc",
                limit=PUBLICATION_LIMIT,
            )
            progress.update(
                t, completed=1, total=1, description=f"Got {len(publications)} pubs"
            )
            data["publications"] = publications

            # Projects
            t = progress.add_task(f"Fetching {PROJECT_LIMIT} projects…", total=None)
            projects = await session.queries.projects_by_organization(
                UT_ORG_ID,
                search_on="openaire_id",
                sort_by="startDate desc",
                limit=PROJECT_LIMIT,
            )
            progress.update(
                t, completed=1, total=1, description=f"Got {len(projects)} projects"
            )
            data["projects"] = projects

            # Scholix links for top-cited papers
            by_citations = sorted(
                [p for p in publications if p.citation_count],
                key=lambda p: p.citation_count,  # ty: ignore[union-attr]
                reverse=True,
            )[:TOP_CITED_SAMPLE]

            all_scholix: list[ScholixRelationship] = []
            for pub in by_citations:
                if not pub.doi:
                    continue
                t = progress.add_task(f"Scholix: {pub.doi[:40]}…", total=None)
                citing = await session.queries.citing_works(
                    pub.doi, limit=SCHOLIX_LIMIT_PER_PAPER
                )
                datasets = await session.queries.related_datasets(
                    pub.doi, limit=SCHOLIX_LIMIT_PER_PAPER
                )
                links = citing + datasets
                _store_scholix(con, links, pub.doi)
                all_scholix.extend(links)
                progress.update(t, completed=1, total=1)

            data["scholix_links"] = all_scholix

        # Persist main tables
        _store_batch(con, "publications", [_pub_to_row(p) for p in publications])
        _store_batch(con, "projects", [_proj_to_row(p) for p in projects])

    return data


# ── Analytics ──────────────────────────────────────────────────────────────


def run_analytics(con: duckdb.DuckDBPyConnection) -> dict:
    """Run SQL analytics on the stored data."""
    r: dict = {}

    r["type_dist"] = con.execute("""
        SELECT type, count(*) as n FROM publications
        GROUP BY type ORDER BY n DESC
    """).fetchall()

    r["year_trends"] = con.execute("""
        SELECT publication_year, count(*) as n FROM publications
        WHERE publication_year IS NOT NULL
        GROUP BY publication_year ORDER BY publication_year
    """).fetchall()

    r["top_authors"] = con.execute("""
        SELECT unnest(string_split(author_names, '; ')) as author, count(*) as n
        FROM publications WHERE author_names != ''
        GROUP BY author ORDER BY n DESC LIMIT 15
    """).fetchall()

    oa = con.execute("""
        SELECT count(*), sum(CASE WHEN is_open_access THEN 1 ELSE 0 END)
        FROM publications
    """).fetchone()
    r["oa_stats"] = {"total": oa[0], "oa": oa[1]}

    r["top_cited"] = con.execute("""
        SELECT title, doi, citation_count, publication_year FROM publications
        WHERE citation_count IS NOT NULL ORDER BY citation_count DESC LIMIT 10
    """).fetchall()

    r["top_keywords"] = con.execute("""
        SELECT lower(trim(kw)) as keyword, count(*) as n
        FROM publications, unnest(string_split(keywords, '; ')) as kw
        WHERE keywords != '' GROUP BY keyword ORDER BY n DESC LIMIT 20
    """).fetchall()

    r["project_status"] = con.execute("""
        SELECT CASE WHEN end_date >= CAST(current_date AS VARCHAR) THEN 'Active'
                    ELSE 'Completed' END as status, count(*) as n
        FROM projects WHERE start_date IS NOT NULL AND end_date IS NOT NULL
        GROUP BY status
    """).fetchall()

    r["funder_dist"] = con.execute("""
        SELECT funder_name, count(*) as n FROM projects
        WHERE funder_name IS NOT NULL AND funder_name != ''
        GROUP BY funder_name ORDER BY n DESC LIMIT 10
    """).fetchall()

    r["project_year_range"] = con.execute("""
        SELECT start_year, count(*) as n FROM projects
        WHERE start_year IS NOT NULL GROUP BY start_year ORDER BY start_year
    """).fetchall()

    r["scholix_summary"] = con.execute("""
        SELECT relationship, count(*) as n FROM scholix_links
        GROUP BY relationship ORDER BY n DESC
    """).fetchall()

    r["scholix_type_dist"] = con.execute("""
        SELECT target_type, count(*) as n FROM scholix_links
        GROUP BY target_type ORDER BY n DESC
    """).fetchall()

    return r


# ── Visualisation ──────────────────────────────────────────────────────────


def _save(fig: plt.Figure, name: str) -> Path:
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_plots(analytics: dict) -> list[Path]:
    """Generate matplotlib plots and return saved file paths."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    # 1 — Publications by year
    year_data = analytics["year_trends"]
    if year_data:
        years, counts = zip(*year_data)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([str(y) for y in years], counts, color="#2563eb", edgecolor="white")
        ax.set_xlabel("Year")
        ax.set_ylabel("Publications")
        ax.set_title("UT Publications by Year (from 2024)")
        ax.tick_params(axis="x", rotation=45)
        for y, c in zip(years, counts):
            ax.annotate(
                str(c),
                (str(y), c),
                textcoords="offset points",
                xytext=(0, 4),
                ha="center",
                fontsize=8,
            )
        paths.append(_save(fig, "publications_by_year.png"))

    # 2 — Type + Open Access overview
    type_data = analytics["type_dist"]
    oa = analytics["oa_stats"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    if type_data:
        labels, vals = zip(*type_data)
        ax1.barh(
            labels,
            vals,
            color=["#2563eb", "#7c3aed", "#059669", "#dc2626", "#d97706"][
                : len(labels)
            ],
        )
        ax1.set_xlabel("Count")
        ax1.set_title("Publication Types")
        for i, v in enumerate(vals):
            ax1.text(v + 1, i, str(v), va="center", fontsize=9)

    if oa["total"]:
        oa_pct = oa["oa"] / oa["total"] * 100
        ax2.pie(
            [oa_pct, 100 - oa_pct],
            labels=["Open Access", "Other"],
            autopct="%1.1f%%",
            colors=["#059669", "#94a3b8"],
            startangle=90,
        )
        ax2.set_title(f"Open Access ({oa['oa']:,} / {oa['total']:,})")

    fig.suptitle("Publication Overview — University of Twente", fontweight="bold")
    paths.append(_save(fig, "publication_overview.png"))

    # 3 — Top-cited publications
    top_cited = analytics["top_cited"]
    if top_cited:
        titles = [r[0][:55] + ("…" if len(r[0]) > 55 else "") for r in top_cited]
        cites = [r[2] for r in top_cited]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(range(len(titles)), cites, color="#7c3aed")
        ax.set_yticks(range(len(titles)))
        ax.set_yticklabels(titles, fontsize=8)
        ax.set_xlabel("Citations")
        ax.set_title("Top-10 Cited Publications")
        ax.invert_yaxis()
        for i, v in enumerate(cites):
            ax.text(v + 1, i, str(v), va="center", fontsize=8)
        paths.append(_save(fig, "top_cited.png"))

    # 4 — Project funders + status
    funder_data = analytics["funder_dist"]
    status_data = analytics["project_status"]
    if funder_data or status_data:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        if funder_data:
            funders, fvals = zip(*funder_data[:8])
            ax1.barh(funders, fvals, color="#2563eb")
            ax1.set_xlabel("Projects")
            ax1.set_title("Projects by Funder")
            for i, v in enumerate(fvals):
                ax1.text(v + 0.3, i, str(v), va="center", fontsize=8)

        if status_data:
            slabels, svals = zip(*status_data)
            ax2.pie(
                svals,
                labels=slabels,
                autopct="%1.0f%%",
                colors=["#059669", "#94a3b8", "#dc2626"][: len(slabels)],
                startangle=90,
            )
            ax2.set_title("Project Status")

        fig.suptitle("Project Overview — University of Twente", fontweight="bold")
        paths.append(_save(fig, "project_overview.png"))

    return paths


# ── Reporting ──────────────────────────────────────────────────────────────


def _table(
    title: str,
    rows: list[tuple],
    col_names: list[str],
    col_styles: list[str] | None = None,
) -> Table:
    """Build a Rich table with uniform styling."""
    t = Table(title=title, show_lines=False)
    styles = col_styles or (["cyan"] + ["green"] * (len(col_names) - 1))
    for name, style in zip(col_names, styles):
        t.add_column(name, style=style, justify="right" if style != "cyan" else "left")
    for row in rows:
        t.add_row(*row)
    return t


def print_report(data: dict, analytics: dict, plot_paths: list[Path]) -> None:
    """Print executive summary to Rich console."""
    total = data.get("total_publications", 0)
    total_oa = data.get("total_open_access", 0)
    oa_pct = total_oa / total * 100 if total else 0
    fetched = len(data.get("publications", []))
    n_proj = len(data.get("projects", []))
    n_scholix = len(data.get("scholix_links", []))

    console.print(
        Panel(
            f"[bold]University of Twente — OpenAIRE Research Analytics[/bold]\n\n"
            f"  Total publications in OpenAIRE:   {total:,}\n"
            f"  Total open access:                {total_oa:,} ({oa_pct:.1f}%)\n"
            f"  Publications fetched (2024+):      {fetched:,}\n"
            f"  Projects fetched:                 {n_proj:,}\n"
            f"  Scholix links (top-cited sample):  {n_scholix:,}",
            title="Executive Summary",
            border_style="blue",
        )
    )

    fmt_n = lambda n: f"{n:,}"
    fmt_s = str

    console.print(
        _table(
            "Publication Types",
            [(t, fmt_n(n)) for t, n in analytics.get("type_dist", [])],
            ["Type", "Count"],
        )
    )

    console.print(
        _table(
            "Publications by Year",
            [(str(y), fmt_n(n)) for y, n in analytics.get("year_trends", [])],
            ["Year", "Count"],
        )
    )

    console.print(
        _table(
            "Top Authors",
            [(a, fmt_s(n)) for a, n in analytics.get("top_authors", [])[:10]],
            ["Author", "Pubs"],
        )
    )

    console.print(
        _table(
            "Top-Cited Publications",
            [
                (t[:60], str(y or ""), str(c or 0))
                for t, doi, c, y in analytics.get("top_cited", [])[:10]
            ],
            ["Title", "Year", "Citations"],
            ["cyan", "green", "yellow"],
        )
    )

    console.print(
        _table(
            "Top Keywords",
            [(kw, fmt_s(n)) for kw, n in analytics.get("top_keywords", [])[:15]],
            ["Keyword", "Count"],
        )
    )

    console.print(
        _table(
            "Projects by Funder",
            [(f, fmt_s(n)) for f, n in analytics.get("funder_dist", [])[:10]],
            ["Funder", "Projects"],
        )
    )

    console.print(
        _table(
            "Project Status",
            [(s, fmt_s(n)) for s, n in analytics.get("project_status", [])],
            ["Status", "Count"],
        )
    )

    scholix_summary = analytics.get("scholix_summary", [])
    if scholix_summary:
        console.print(
            _table(
                "Scholix Relationships (sampled papers)",
                [(rel, fmt_s(n)) for rel, n in scholix_summary],
                ["Relationship", "Count"],
            )
        )

    console.print("\n[bold]Generated outputs:[/bold]")
    console.print(f"  Database:  {DB_PATH}")
    for p in plot_paths:
        console.print(f"  Plot:      {p}")
    console.print()


# ── Main ───────────────────────────────────────────────────────────────────


async def main() -> None:
    console.print(
        Panel(
            "[bold]AIREloom Comprehensive Analysis[/bold]\n"
            "University of Twente — OpenAIRE Graph + Scholix",
            border_style="blue",
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    _init_db(con)

    try:
        data = await fetch_data(con)
        analytics = run_analytics(con)
        plot_paths = generate_plots(analytics)
        print_report(data, analytics, plot_paths)
    finally:
        con.close()

    console.print("[bold green]Analysis complete.[/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
