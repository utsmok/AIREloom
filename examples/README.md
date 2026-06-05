# AIREloom Example Scripts

This directory contains example scripts demonstrating how to use the AIREloom library. Every example is also a **marimo notebook** — they can be run as scripts, explored interactively, or embedded in documentation.

## Quick Start

- **`simple_example.py`** — Basic usage: searching research products, iterating results, and querying projects.
- **`comprehensive_analysis.py`** — Full data analysis pipeline: retrieves OpenAIRE research data, stores it in DuckDB, and generates visualizations and reports.

## Endpoint Examples

- **`02_scholix_link_discovery.py`** — Discover relationships between publications and datasets via the Scholix API.
- **`03_research_product_analysis.py`** — Deep-dive into research product metadata: authors, citations, open access, instances.
- **`04_organization_projects.py`** — Explore organizations and their associated projects and publications.
- **`05_advanced_filtering.py`** — Advanced filter combinations: multi-field, date ranges, sort, pagination.
- **`06_persons_discovery.py`** — Search for researchers, retrieve person records, explore co-authorship.

## Ergonomics Layer (v0.3+)

These examples showcase the ergonomics features added in v0.3.0: computed fields, safe types, convenience queries, and iterator helpers. Each is a marimo notebook.

- **`07_ergonomics_showcase.py`** — **Before & after comparison.** The same tasks done with raw API calls vs. the ergonomics layer side-by-side.
- **`08_iterator_helpers.py`** — `collect()`, `count()`, `first()` on all resource clients.
- **`09_computed_fields_and_safe_types.py`** — All 18 computed properties across entity models and SafeStr/SafeList defaults.
- **`10_convenience_queries.py`** — All 9 convenience query functions (`publications_by_doi`, `citing_works`, etc.).

## Running Examples

### As a script

```bash
uv run examples/07_ergonomics_showcase.py
```

### As an interactive marimo notebook

```bash
uv run marimo run examples/07_ergonomics_showcase.py
```

### Edit interactively

```bash
uv run marimo edit examples/07_ergonomics_showcase.py
```

### In WASM (browser, no Python needed)

```bash
marimo export html-wasm examples/07_ergonomics_showcase.py -o site/ergonomics --mode run
```

## Embedding in Documentation

### Via molab (recommended)

The easiest way to embed interactive notebooks in docs is via [molab](https://docs.marimo.io/guides/molab/). For notebooks hosted on GitHub:

```html
<iframe
    src="https://marimo.app/github/utsmok/aireloom/blob/main/examples/07_ergonomics_showcase.py/wasm?embed=true"
    sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms"
    width="100%"
    height="600"
    style="border: 1px solid #ddd; border-radius: 8px;"
></iframe>
```

### Via marimo islands

For embedding individual cell outputs (e.g., a computed fields table) directly in mkdocs pages:

```python
from marimo import MarimoIslandGenerator

generator = MarimoIslandGenerator.from_file(
    "examples/07_ergonomics_showcase.py",
    display_code=False,
)
html = generator.render_html()
```

See the [marimo islands docs](https://docs.marimo.io/guides/exporting/webassembly_html/#embed-marimo-outputs-in-html-using-islands) for full details.

### Via self-hosted WASM HTML

Export and serve the notebook as a self-contained HTML file:

```bash
marimo export html-wasm examples/07_ergonomics_showcase.py -o docs/examples/ergonomics.html --mode run
```

Then embed with an iframe in your mkdocs page.

## Credentials

The OpenAIRE Graph API works without authentication. All examples run without credentials. For higher rate limits, set up OAuth2 credentials in a `.env` file:

```
AIRELOOM_OPENAIRE_CLIENT_ID=your_client_id_here
AIRELOOM_OPENAIRE_CLIENT_SECRET=your_client_secret_here
```

---

## Comprehensive Analysis Details

`comprehensive_analysis.py` demonstrates the `AIREloom` package by executing a data analysis pipeline to retrieve, analyze, and visualize OpenAIRE research data:

- Data collection: Retrieves research outputs published 2024 and later by University of Twente authors
- Local storage: Stores data in an optimized DuckDB database
- Analytics: Generates detailed insights and visualizations
- Reporting: Produces summary reports with actionable insights
