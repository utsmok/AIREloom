#!/usr/bin/env python3
"""Comprehensive analysis of University of Twente research output (2023-2025).

Fetches ALL publications, projects, and Scholix links for UT from the
OpenAIRE Graph API, stores them in DuckDB, runs analytics, and produces
matplotlib visualisations.

Run with:
    uv run --group analysis examples/comprehensive_analysis.py
"""

from __future__ import annotations

import asyncio
import statistics
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import polars as pl
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from aireloom import AireloomSession, Project, ResearchProduct, ScholixRelationship
from aireloom.endpoints import ResearchProductsFilters

# ── Configuration ──────────────────────────────────────────────────────────

UT_ORG_ID = "openorgs____::604881198363fedbb5d5478f465305f2"
DATE_FROM = "2023-01-01"
DATE_TO = "2025-12-31"
SCHOLIX_CONCURRENCY = 10
SCHOLIX_LIMIT_PER_PAPER = 50

OUTPUT_DIR = Path("output")
DB_PATH = OUTPUT_DIR / "analysis.duckdb"

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
    keywords        VARCHAR,
    countries       VARCHAR,
    funding         VARCHAR"""

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
    id              INTEGER DEFAULT nextval('scholix_seq'),
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
        con.execute(f"DROP TABLE IF EXISTS {name}")
        con.execute(f"CREATE TABLE {name} ({schema})")


def _pub_to_row(p: ResearchProduct) -> dict:
    subjects = "; ".join(
        s.subject.get("value", "")
        if isinstance(s.subject, dict)
        else str(s.subject or "")
        for s in p.subjects
        if s.subject
    )
    countries = "; ".join(c.code for c in p.countries if c.code)
    return {
        "id": p.id,
        "title": p.title[:500],
        "doi": p.doi or "",
        "type": str(p.type or ""),
        "publication_date": p.publicationDate or "",
        "publication_year": p.publication_year or 0,
        "publisher": p.publisher or "",
        "language": p.language.code if p.language else "",
        "is_open_access": p.is_open_access or False,
        "open_access_url": p.open_access_url or "",
        "citation_count": p.citation_count or 0,
        "journal_name": p.journal_name or "",
        "license": p.license or "",
        "author_names": "; ".join(p.author_names),
        "subjects": subjects,
        "keywords": subjects,
        "countries": countries,
        "funding": "",
    }


def _proj_to_row(pr: Project) -> dict:
    funders = "; ".join(
        f.shortName or f.name or "" for f in pr.fundings if f.shortName or f.name
    )
    return {
        "id": pr.id,
        "title": pr.title[:500],
        "code": pr.code or "",
        "acronym": pr.acronym or "",
        "start_date": pr.startDate or "",
        "end_date": pr.endDate or "",
        "start_year": pr.start_year or 0,
        "end_year": pr.end_year or 0,
        "summary": (pr.summary or "")[:1000],
        "funder_name": pr.funder_name or "",
        "funders": funders,
        "keywords": "; ".join(pr.keywords),
        "oa_mandate_pub": pr.openAccessMandateForPublications or False,
        "oa_mandate_data": pr.openAccessMandateForDataset or False,
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
    cols = ", ".join(df.columns)
    con.execute(f"INSERT INTO {table}({cols}) SELECT * FROM df")


def _store_scholix(
    con: duckdb.DuckDBPyConnection,
    links: list[ScholixRelationship],
    publication_doi: str,
) -> None:
    rows = []
    for lk in links:
        source_dois = "; ".join(
            i.id_val for i in lk.source.identifier if i.id_scheme == "doi"
        )
        target_dois = "; ".join(
            i.id_val for i in lk.target.identifier if i.id_scheme == "doi"
        )
        rows.append(
            {
                "source_doi": source_dois,
                "source_type": lk.source.type,
                "source_title": lk.source.title[:300],
                "target_doi": target_dois,
                "target_type": lk.target.type,
                "target_title": lk.target.title[:300],
                "relationship": str(lk.relationship_type.name),
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
            # ── Counts ──
            t = progress.add_task("Counting UT publications (2023-2025)…", total=None)
            base_filters = ResearchProductsFilters(
                relOrganizationId=UT_ORG_ID,
                fromPublicationDate=DATE_FROM,
                toPublicationDate=DATE_TO,
            )
            total_pubs = await session.research_products.count(filters=base_filters)
            oa_filters = ResearchProductsFilters(
                relOrganizationId=UT_ORG_ID,
                fromPublicationDate=DATE_FROM,
                toPublicationDate=DATE_TO,
                bestOpenAccessRightLabel="OPEN",
            )
            total_oa = await session.research_products.count(filters=oa_filters)
            progress.update(
                t,
                completed=1,
                total=1,
                description=f"UT 2023-2025: {total_pubs:,} pubs ({total_oa:,} OA)",
            )
            data["total_publications"] = total_pubs
            data["total_open_access"] = total_oa

            # ── Publications (ALL, cursor-paginated) ──
            t = progress.add_task(
                f"Fetching all {total_pubs:,} publications (this may take a few minutes)…",
                total=None,
            )
            filters = ResearchProductsFilters(
                relOrganizationId=UT_ORG_ID,
                fromPublicationDate=DATE_FROM,
                toPublicationDate=DATE_TO,
            )
            publications = await session.research_products.collect(
                filters=filters,
                page_size=100,
            )
            progress.update(
                t,
                completed=1,
                total=1,
                description=f"Got {len(publications):,} publications",
            )
            data["publications"] = publications

            # ── Projects (ALL for UT) ──
            t = progress.add_task("Fetching all UT projects…", total=None)
            projects = await session.queries.projects_by_organization(
                UT_ORG_ID,
                search_on="openaire_id",
                sort_by="startDate DESC",
            )
            progress.update(
                t,
                completed=1,
                total=1,
                description=f"Got {len(projects):,} projects",
            )
            data["projects"] = projects

            # ── Scholix links for ALL publications with DOIs ──
            dois = sorted(
                [(p.doi, p.citation_count or 0) for p in publications if p.doi],
                key=lambda x: x[1],
                reverse=True,
            )
            all_dois = [d[0] for d in dois]
            n_dois = len(all_dois)
            n_cited = sum(1 for _, c in dois if c > 0)
            console.print(
                f"[bold]Scholix: querying {n_dois:,} DOIs ({n_cited:,} with citations)[/bold]"
            )

            sem = asyncio.Semaphore(SCHOLIX_CONCURRENCY)
            all_scholix: list[ScholixRelationship] = []

            async def _scholix_for_doi(doi: str) -> list[ScholixRelationship]:
                async with sem:
                    citing = await session.queries.citing_works(
                        doi, limit=SCHOLIX_LIMIT_PER_PAPER
                    )
                    datasets = await session.queries.related_datasets(
                        doi, limit=SCHOLIX_LIMIT_PER_PAPER
                    )
                    return citing + datasets

            t = progress.add_task("Scholix links…", total=n_dois)
            stored = 0
            for i in range(0, n_dois, SCHOLIX_CONCURRENCY):
                chunk = all_dois[i : i + SCHOLIX_CONCURRENCY]
                results = await asyncio.gather(*[_scholix_for_doi(d) for d in chunk])
                for doi, links in zip(chunk, results, strict=False):
                    if links:
                        _store_scholix(con, links, doi)
                        all_scholix.extend(links)
                stored += len(chunk)
                progress.update(
                    t,
                    completed=stored,
                    description=f"Scholix: {stored}/{n_dois} DOIs ({len(all_scholix):,} links)",
                )

            data["scholix_links"] = all_scholix
            progress.update(
                t,
                completed=n_dois,
                total=n_dois,
                description=f"Scholix done: {len(all_scholix):,} links from {n_dois:,} DOIs",
            )

        # Persist main tables
        _store_batch(con, "publications", [_pub_to_row(p) for p in publications])
        _store_batch(con, "projects", [_proj_to_row(p) for p in projects])

    return data


# ── Analytics ──────────────────────────────────────────────────────────────


def run_analytics(con: duckdb.DuckDBPyConnection) -> dict:
    """Run SQL analytics on the stored data."""
    r: dict = {}

    # Publication type distribution
    r["type_dist"] = con.execute("""
        SELECT type, count(*) as n FROM publications
        GROUP BY type ORDER BY n DESC
    """).fetchall()

    # Year trends
    r["year_trends"] = con.execute("""
        SELECT publication_year, count(*) as n FROM publications
        WHERE publication_year > 0
        GROUP BY publication_year ORDER BY publication_year
    """).fetchall()

    # Top authors
    r["top_authors"] = con.execute("""
        SELECT t.author, count(*) as n
        FROM publications, unnest(string_split(author_names, '; ')) AS t(author)
        WHERE t.author != ''
        GROUP BY t.author ORDER BY n DESC LIMIT 15
    """).fetchall()

    # Open access stats
    oa = con.execute("""
        SELECT count(*), sum(CASE WHEN is_open_access THEN 1 ELSE 0 END)
        FROM publications
    """).fetchone()
    r["oa_stats"] = {"total": oa[0], "oa": oa[1]}

    # Top cited
    r["top_cited"] = con.execute("""
        SELECT title, doi, citation_count, publication_year FROM publications
        WHERE citation_count > 0 ORDER BY citation_count DESC LIMIT 10
    """).fetchall()

    # Top keywords / subjects
    r["top_keywords"] = con.execute("""
        SELECT lower(trim(t.kw)) as keyword, count(*) as n
        FROM publications, unnest(string_split(keywords, '; ')) AS t(kw)
        WHERE t.kw != '' GROUP BY keyword ORDER BY n DESC LIMIT 20
    """).fetchall()

    # ── Project analytics ──
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
        WHERE start_year > 0 GROUP BY start_year ORDER BY start_year
    """).fetchall()

    # ── Scholix analytics ──
    r["scholix_summary"] = con.execute("""
        SELECT relationship, count(*) as n FROM scholix_links
        GROUP BY relationship ORDER BY n DESC
    """).fetchall()

    r["scholix_type_dist"] = con.execute("""
        SELECT target_type, count(*) as n FROM scholix_links
        GROUP BY target_type ORDER BY n DESC
    """).fetchall()

    # ── NEW: OA trend by year ──
    r["oa_trend"] = con.execute("""
        SELECT publication_year,
               count(*) as total,
               sum(CASE WHEN is_open_access THEN 1 ELSE 0 END) as oa_count,
               round(100.0 * sum(CASE WHEN is_open_access THEN 1 ELSE 0 END) / count(*), 1) as oa_pct
        FROM publications
        WHERE publication_year > 0
        GROUP BY publication_year ORDER BY publication_year
    """).fetchall()

    # ── NEW: Top publishers ──
    r["top_publishers"] = con.execute("""
        SELECT publisher, count(*) as n FROM publications
        WHERE publisher IS NOT NULL AND publisher != ''
        GROUP BY publisher ORDER BY n DESC LIMIT 10
    """).fetchall()

    # ── NEW: Country collaboration ──
    r["country_collab"] = con.execute("""
        SELECT t.cc, count(*) as n
        FROM publications, unnest(string_split(countries, '; ')) AS t(cc)
        WHERE t.cc != ''
        GROUP BY t.cc ORDER BY n DESC LIMIT 15
    """).fetchall()

    # ── NEW: Top publication venues (journals) ──
    r["top_journals"] = con.execute("""
        SELECT journal_name, count(*) as n FROM publications
        WHERE journal_name IS NOT NULL AND journal_name != ''
        GROUP BY journal_name ORDER BY n DESC LIMIT 15
    """).fetchall()

    # ── NEW: Type by year cross-tab ──
    r["type_by_year"] = con.execute("""
        SELECT publication_year, type, count(*) as n
        FROM publications
        WHERE publication_year > 0
        GROUP BY publication_year, type
        ORDER BY publication_year, n DESC
    """).fetchall()

    # ── NEW: Citation statistics ──
    citation_rows = con.execute("""
        SELECT citation_count FROM publications
        WHERE citation_count IS NOT NULL AND citation_count > 0
    """).fetchall()
    all_cites = [row[0] for row in citation_rows]

    cite_by_type = con.execute("""
        SELECT type,
               count(*) as n,
               round(avg(citation_count), 1) as mean_cites,
               max(citation_count) as max_cites
        FROM publications
        WHERE citation_count IS NOT NULL AND citation_count > 0
        GROUP BY type ORDER BY mean_cites DESC
    """).fetchall()

    median_cite = statistics.median(all_cites) if all_cites else 0
    mean_cite = statistics.mean(all_cites) if all_cites else 0
    max_cite = max(all_cites) if all_cites else 0
    r["citation_stats"] = {
        "overall": {
            "n_with_citations": len(all_cites),
            "mean": round(mean_cite, 1),
            "median": round(median_cite, 1),
            "max": max_cite,
        },
        "by_type": cite_by_type,
        "_raw_citations": all_cites,
    }

    # ── Language distribution ──
    r["lang_dist"] = con.execute("""
        SELECT language, count(*) as n FROM publications
        WHERE language IS NOT NULL AND language != ''
        GROUP BY language ORDER BY n DESC LIMIT 10
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
    palette = ["#2563eb", "#7c3aed", "#059669", "#dc2626", "#d97706", "#0891b2"]

    # 1 — Publications by year
    year_data = analytics["year_trends"]
    if year_data:
        years, counts = zip(*year_data, strict=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([str(y) for y in years], counts, color="#2563eb", edgecolor="white")
        ax.set_xlabel("Year")
        ax.set_ylabel("Publications")
        ax.set_title("UT Publications by Year (2023-2025)")
        for y, c in zip(years, counts, strict=False):
            ax.annotate(
                str(c),
                (str(y), c),
                textcoords="offset points",
                xytext=(0, 4),
                ha="center",
                fontsize=9,
            )
        paths.append(_save(fig, "publications_by_year.png"))

    # 2 — Type + Open Access overview
    type_data = analytics["type_dist"]
    oa = analytics["oa_stats"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    if type_data:
        labels, vals = zip(*type_data, strict=False)
        ax1.barh(labels, vals, color=palette[: len(labels)])
        ax1.set_xlabel("Count")
        ax1.set_title("Publication Types")
        for i, v in enumerate(vals):
            ax1.text(v + 1, i, f"{v:,}", va="center", fontsize=9)

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

    fig.suptitle(
        "Publication Overview — University of Twente (2023-2025)", fontweight="bold"
    )
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
            ax.text(v + 1, i, f"{v:,}", va="center", fontsize=8)
        paths.append(_save(fig, "top_cited.png"))

    # 4 — Project funders + status
    funder_data = analytics["funder_dist"]
    status_data = analytics["project_status"]
    if funder_data or status_data:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        if funder_data:
            funders, fvals = zip(*funder_data[:8], strict=False)
            ax1.barh(funders, fvals, color="#2563eb")
            ax1.set_xlabel("Projects")
            ax1.set_title("Projects by Funder")
            for i, v in enumerate(fvals):
                ax1.text(v + 0.3, i, str(v), va="center", fontsize=8)

        if status_data:
            slabels, svals = zip(*status_data, strict=False)
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

    # 5 — OA trend by year
    oa_trend = analytics.get("oa_trend", [])
    if oa_trend:
        years, totals, oa_counts, oa_pcts = zip(*oa_trend, strict=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            [str(y) for y in years],
            oa_pcts,
            "o-",
            color="#059669",
            linewidth=2,
            markersize=8,
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Open Access %")
        ax.set_title("Open Access Trend by Year")
        ax.set_ylim(0, 100)
        for y, pct, n_oa, n_tot in zip(years, oa_pcts, oa_counts, totals, strict=False):
            ax.annotate(
                f"{pct}%\n({n_oa:,}/{n_tot:,})",
                (str(y), pct),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=9,
            )
        paths.append(_save(fig, "oa_trend.png"))

    # 6 — Top publishers
    top_publishers = analytics.get("top_publishers", [])
    if top_publishers:
        pub_names, pub_vals = zip(*top_publishers, strict=False)
        # Truncate long names
        pub_labels = [n[:50] + "…" if len(n) > 50 else n for n in pub_names]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(pub_labels, pub_vals, color="#0891b2")
        ax.set_xlabel("Publications")
        ax.set_title("Top 10 Publishers")
        ax.invert_yaxis()
        for i, v in enumerate(pub_vals):
            ax.text(v + 1, i, f"{v:,}", va="center", fontsize=9)
        paths.append(_save(fig, "top_publishers.png"))

    # 7 — Type distribution pie
    if type_data:
        labels, vals = zip(*type_data, strict=False)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            vals,
            labels=labels,
            autopct="%1.1f%%",
            colors=palette[: len(labels)],
            startangle=90,
        )
        ax.set_title("Publication Type Distribution")
        paths.append(_save(fig, "type_distribution.png"))

    # 8 — Citation distribution histogram
    cite_raw = analytics.get("citation_stats", {}).get("_raw_citations", [])
    cite_overall = analytics.get("citation_stats", {}).get("overall", {})
    n_with = cite_overall.get("n_with_citations", 0)
    if n_with > 0 and cite_raw:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(cite_raw, bins=50, color="#7c3aed", edgecolor="white")
        ax.set_xlabel("Citation Count")
        ax.set_ylabel("Number of Publications")
        ax.set_title("Citation Count Distribution")
        if max(cite_raw) > 100:
            ax.set_yscale("log")
        paths.append(_save(fig, "citation_distribution.png"))

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
    for name, style in zip(col_names, styles, strict=False):
        t.add_column(name, style=style, justify="right" if style != "cyan" else "left")
    for row in rows:
        t.add_row(*(str(c) for c in row))
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
            f"[bold]University of Twente — OpenAIRE Research Analytics (2023-2025)[/bold]\n\n"
            f"  Total publications in OpenAIRE (2023-2025): {total:,}\n"
            f"  Total open access:                          {total_oa:,} ({oa_pct:.1f}%)\n"
            f"  Publications fetched:                       {fetched:,}\n"
            f"  Projects fetched:                           {n_proj:,}\n"
            f"  Scholix links (all DOIs):                   {n_scholix:,}",
            title="Executive Summary",
            border_style="blue",
        )
    )

    console.print(
        _table(
            "Publication Types",
            [(t, f"{n:,}") for t, n in analytics.get("type_dist", [])],
            ["Type", "Count"],
        )
    )

    console.print(
        _table(
            "Publications by Year",
            [(str(y), f"{n:,}") for y, n in analytics.get("year_trends", [])],
            ["Year", "Count"],
        )
    )

    console.print(
        _table(
            "Top Authors",
            [(a, f"{n:,}") for a, n in analytics.get("top_authors", [])[:10]],
            ["Author", "Pubs"],
        )
    )

    console.print(
        _table(
            "Top-Cited Publications",
            [
                (t[:60], str(y or ""), f"{c:,}")
                for t, doi, c, y in analytics.get("top_cited", [])[:10]
            ],
            ["Title", "Year", "Citations"],
            ["cyan", "green", "yellow"],
        )
    )

    console.print(
        _table(
            "Top Keywords / Subjects",
            [(kw, f"{n:,}") for kw, n in analytics.get("top_keywords", [])[:15]],
            ["Keyword", "Count"],
        )
    )

    # OA trend
    oa_trend = analytics.get("oa_trend", [])
    if oa_trend:
        console.print(
            _table(
                "Open Access Trend by Year",
                [
                    (str(y), f"{tot:,}", f"{oa_n:,}", f"{pct}%")
                    for y, tot, oa_n, pct in oa_trend
                ],
                ["Year", "Total", "OA Count", "OA %"],
                ["cyan", "green", "yellow", "magenta"],
            )
        )

    # Top publishers
    top_publishers = analytics.get("top_publishers", [])
    if top_publishers:
        console.print(
            _table(
                "Top Publishers",
                [(p[:60], f"{n:,}") for p, n in top_publishers],
                ["Publisher", "Pubs"],
            )
        )

    # Country collaboration
    country_collab = analytics.get("country_collab", [])
    if country_collab:
        console.print(
            _table(
                "Country Collaboration (Top 15)",
                [(c, f"{n:,}") for c, n in country_collab],
                ["Country", "Pubs"],
            )
        )

    # Top journals
    top_journals = analytics.get("top_journals", [])
    if top_journals:
        console.print(
            _table(
                "Top Publication Venues (Top 15)",
                [(j[:60], f"{n:,}") for j, n in top_journals],
                ["Journal", "Pubs"],
            )
        )

    # Type by year
    type_by_year = analytics.get("type_by_year", [])
    if type_by_year:
        console.print(
            _table(
                "Publication Type by Year",
                [(str(y), t, f"{n:,}") for y, t, n in type_by_year],
                ["Year", "Type", "Count"],
            )
        )

    # Citation statistics
    cite_stats = analytics.get("citation_stats", {})
    cite_overall = cite_stats.get("overall", {})
    if cite_overall:
        console.print(
            _table(
                "Citation Statistics",
                [
                    (
                        "Papers with citations",
                        f"{cite_overall.get('n_with_citations', 0):,}",
                    ),
                    ("Mean citations", str(cite_overall.get("mean", 0))),
                    ("Median citations", str(cite_overall.get("median", 0))),
                    ("Max citations", f"{cite_overall.get('max', 0):,}"),
                ],
                ["Metric", "Value"],
            )
        )

    cite_by_type = cite_stats.get("by_type", [])
    if cite_by_type:
        console.print(
            _table(
                "Citation Statistics by Type",
                [
                    (t, f"{n:,}", str(mean), f"{mx:,}")
                    for t, n, mean, mx in cite_by_type
                ],
                ["Type", "Papers", "Mean Citations", "Max Citations"],
                ["cyan", "green", "yellow", "magenta"],
            )
        )

    # Language distribution
    lang_dist = analytics.get("lang_dist", [])
    if lang_dist:
        console.print(
            _table(
                "Top Languages",
                [(lang, f"{n:,}") for lang, n in lang_dist],
                ["Language", "Pubs"],
            )
        )

    # Project analytics
    console.print(
        _table(
            "Projects by Funder",
            [(f, f"{n:,}") for f, n in analytics.get("funder_dist", [])[:10]],
            ["Funder", "Projects"],
        )
    )

    console.print(
        _table(
            "Project Status",
            [(s, f"{n:,}") for s, n in analytics.get("project_status", [])],
            ["Status", "Count"],
        )
    )

    scholix_summary = analytics.get("scholix_summary", [])
    if scholix_summary:
        console.print(
            _table(
                "Scholix Relationships (all publications)",
                [(rel, f"{n:,}") for rel, n in scholix_summary],
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
            "University of Twente (2023-2025) — OpenAIRE Graph + Scholix",
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
