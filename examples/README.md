# AIREloom Example Scripts

This directory contains example scripts demonstrating how to use the AIREloom library.

- **`simple_example.py`** — Basic usage: searching research products, iterating results, and querying projects. Run with `uv run examples/simple_example.py`.
- **`comprehensive_analysis.py`** — Full data analysis pipeline: retrieves OpenAIRE research data, stores it in DuckDB, and generates visualizations and reports. Run with `uv run examples/comprehensive_analysis.py`.

### Credentials

Both scripts optionally read OpenAIRE API credentials from a `.env` file in the project root:

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

### Database Schema

Research Outputs:
- Comprehensive metadata (title, type, publication date)
- Author information (names, counts, affiliations)
- Impact metrics (citations, influence, popularity)
- Access rights and open access information
- Subject classifications and keywords

Projects:
- Project metadata and funding information
- Timeline and budget details
- Open access mandates

Scholix Relationships:
- Cross-references between research entities
- Relationship types and metadata

## Results

### Runtime

- retrieval: ~35-40 seconds (4,824 research outputs)
- analysis: ~3-5 seconds
- total: ~40-45 seconds

### Outputs

Files:
- `output_distribution_analysis.png` - Research type and temporal distribution
- `temporal_trends_analysis.png`  - Time-series analysis and trends
- `subject_areas_analysis.png` - Subject area categorization
- `aireloom_analysis.db` (~4.5MB) - Complete structured dataset


Console output:
- Real-time progress tracking
- Executive summary table
- Key insights and recommendations


## Script overview

The script includes comprehensive error handling:

- Automatic throttling and retry logic
- Schema enforcement and data quality checks
- Connection timeout and retry mechanisms
- Proper cleanup of database connections

And includes these considerations for performance:
- Efficient data insertion (100 records per batch)
- Memory-efficient data retrieval using cursor indexing
- Optimized query performance w/ indexed sql db
- Async, non-blocking I/O for API calls
