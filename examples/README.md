# AIREloom Example Scripts

This directory contains example scripts demonstrating how to use the AIREloom library.

## Quick Start

- **`simple_example.py`** — Basic usage: searching research products, iterating results, and querying projects. Run with `uv run examples/simple_example.py`.
- **`comprehensive_analysis.py`** — Full data analysis pipeline: retrieves OpenAIRE research data, stores it in DuckDB, and generates visualizations and reports. Run with `uv run examples/comprehensive_analysis.py`.

## Endpoint Examples

- **`02_scholix_link_discovery.py`** — Discover relationships between publications and datasets via the Scholix API.
- **`03_research_product_analysis.py`** — Deep-dive into research product metadata: authors, citations, open access, instances.
- **`04_organization_projects.py`** — Explore organizations and their associated projects and publications.
- **`05_advanced_filtering.py`** — Advanced filter combinations: multi-field, date ranges, sort, pagination.
- **`06_persons_discovery.py`** — Search for researchers, retrieve person records, explore co-authorship.

## Ergonomics Layer (v0.3+)

These examples showcase the ergonomics features added in v0.3.0: computed fields, safe types, convenience queries, and iterator helpers.

- **`07_ergonomics_showcase.py`** — **Before & after comparison.** Demonstrates the same tasks with raw API calls vs. the ergonomics layer side-by-side. Start here to understand what changed.
- **`08_iterator_helpers.py`** — `collect()`, `count()`, `first()` on all resource clients. Eliminates common pagination boilerplate.
- **`09_computed_fields_and_safe_types.py`** — Computed properties (`doi`, `is_open_access`, `citation_count`, etc.) and safe defaults (SafeStr, SafeList). No more `if x is not None` guards.
- **`10_convenience_queries.py`** — High-level query functions (`publications_by_doi`, `publications_by_organization`, `citing_works`, etc.) that compose client operations into single calls.

## Credentials

All scripts optionally read OpenAIRE API credentials from a `.env` file in the project root:

```
AIRELOOM_OPENAIRE_CLIENT_ID=your_client_id_here
AIRELOOM_OPENAIRE_CLIENT_SECRET=your_client_secret_here
```

Without credentials, the scripts use unauthenticated access with lower rate limits.

---

## Comprehensive Analysis Details

`comprehensive_analysis.py` demonstrates the `AIREloom` package by executing a data analysis pipeline to retrieve, analyze, and visualize OpenAIRE research data. The script performs an integrated workflow including:

- Data collection: Retrieves research outputs published 2024 and later by University of Twente authors
- Local storage: Stores data in an optimized DuckDB database
- Analytics: Generates detailed insights and visualizations
- Reporting: Produces summary reports with actionable insights

## Technical Implementation

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   OpenAIRE API  │───▶│  AIREloom Client │───▶│   Data Storage  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Visualizations │◀───│     Analytics    │◀───│   DuckDB Local  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```
