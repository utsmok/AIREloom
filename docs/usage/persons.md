# Persons

The Persons endpoint provides access to individual researcher profiles in the OpenAIRE Graph — including names, ORCID identifiers, co-authors, and research indicators. This is a **v1-only** endpoint, routed automatically by AIREloom.

## Accessing the Client

```python
from aireloom import AireloomSession
from aireloom.endpoints import PersonsFilters

async with AireloomSession() as session:
    response = await session.persons.search(
        filters=PersonsFilters(search="dijkstra"),
        page_size=10,
    )
```

## Fetch a Single Person

```python
async with AireloomSession() as session:
    person = await session.persons.get(
        "30openaire____::5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f"
    )
    print(person.full_name)
    print(person.orcid)
```

## Search with Filters

```python
from aireloom.endpoints import PersonsFilters

filters = PersonsFilters(search="feynman")

async with AireloomSession() as session:
    response = await session.persons.search(
        filters=filters, sort_by="relevance desc"
    )
    for person in response.results:
        print(person.full_name, person.orcid)
```

### Filter Reference

| Field | Type | Description |
|-------|------|-------------|
| `search` | `str` | Keyword search |
| `id` | `str` | OpenAIRE identifier |
| `originalId` | `str` | Original identifier (e.g. ORCID) |
| `givenName` | `str` | Given (first) name |
| `lastName` | `str` | Family (last) name |
| `logicalOperator` | `str` | `AND` or `OR` (default `AND`) |

!!! warning "API limitation"
    The `givenName` and `lastName` filters currently cause HTTP 500 errors from the OpenAIRE API. Use `search` for name-based queries until this is resolved.

### Sort Fields

Persons support sorting by: `relevance`, `startDate`, `endDate`.

## Iterate Over Results

```python
from aireloom.endpoints import PersonsFilters

filters = PersonsFilters(search="knuth")

async with AireloomSession() as session:
    async for person in session.persons.iterate(filters=filters):
        print(person.full_name, person.orcid)
```

## Model Overview

Each result is a `Person` instance. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | OpenAIRE identifier |
| `givenName` | `str` | Given (first) name |
| `familyName` | `str` | Family (last) name |
| `originalId` | `SafeList[str]` | Source identifiers (ORCID, etc.) |
| `alternativeNames` | `SafeList[str]` | Other known names |
| `biography` | `str` | Biography text |
| `subject` | `SafeList[str]` | Research subjects |
| `indicator` | `dict \| None` | Metrics (hIndex, citationCount, etc.) |
| `context` | `dict \| None` | Affiliation info |
| `coAuthors` | `SafeList[str]` | Co-author names |
| `consent` | `bool \| None` | Data processing consent |

## Computed Properties

| Property | Return | Description |
|----------|--------|-------------|
| `full_name` | `str` | Combined given + family name |
| `orcid` | `str \| None` | ORCID extracted from `originalId` or `id` |

All `SafeList` fields (`originalId`, `alternativeNames`, `subject`, `coAuthors`) default to an empty list — never `None`.

## Example Notebook

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/06_persons_discovery.py/wasm?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>
