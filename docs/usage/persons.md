# Persons

Individual researcher profiles in the OpenAIRE Graph — names, ORCID identifiers, co-authors, and research indicators.

!!! info "v1-only endpoint"
    This endpoint is only available on the v1 API. AIREloom routes it automatically.

## Access

```python
async with AireloomSession() as session:
    client = session.persons  # PersonsResource
```

## Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | Keyword search |
| `id` | `str` | OpenAIRE identifier |
| `originalId` | `str` | Original identifier (e.g. ORCID) |
| `givenName` | `str` | Given (first) name |
| `lastName` | `str` | Family (last) name |
| `logicalOperator` | `str` | `AND` or `OR` (default `AND`) |

!!! warning "API limitation"
    The `givenName` and `lastName` filters currently cause HTTP 500 errors. Use `search` for name-based queries until this is resolved.

See [Basic Usage](../usage_basics.md) for common search/iterate/collect patterns.

## Sort Fields

`relevance`, `startDate`, `endDate`. Use `"field asc"` or `"field desc"`.

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `givenName` | `str` | Given (first) name |
| `familyName` | `str` | Family (last) name |
| `originalId` | `SafeList[str]` | Source identifiers (ORCID, etc.) |
| `alternativeNames` | `SafeList[str]` | Other known names |
| `biography` | `str` | Biography text |
| `subject` | `SafeList[str]` | Research subjects |
| `indicator` | `dict \| None` | Metrics (hIndex, citationCount, etc.) |
| `coAuthors` | `SafeList[str]` | Co-author names |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `full_name` | `str` | Combined given + family name |
| `orcid` | `str \| None` | ORCID extracted from `originalId` or `id` |

See [Features](../ergonomics.md) for an overview of computed properties and `SafeList`.

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/06_persons_discovery.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
