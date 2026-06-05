# AIREloom

**Async Python client for the [OpenAIRE Graph API](https://graph.openaire.eu/).**

Built on [bibliofabric](https://github.com/afuetterer/bibliofabric), AIREloom provides a modern, typed interface to the OpenAIRE research graph — research products, projects, organizations, data sources, persons, and Scholix links.

## Features

:rocket: &nbsp;**Async/await first** — native `asyncio` client with context-manager sessions  
:gear: &nbsp;**Typed models** — Pydantic v2 models for every response, with IDE autocomplete everywhere  
:arrows_counterclockwise: &nbsp;**Cursor pagination** — automatic page handling via `iterate()`, `collect()`, `count()`, `first()`  
:wrench: &nbsp;**Ergonomics layer** — computed properties (`product.doi`, `product.is_open_access`), `SafeList`/`SafeStr` types, convenience queries  
:link: &nbsp;**Scholix & Links** — Scholexplorer API integration plus research-product relations  
:bust_in_silhouette: &nbsp;**Persons endpoint** — OpenAIRE Graph API v1 person entities  

## Install

```bash
pip install aireloom
```

## Quick Start

```python
from aireloom import AireloomSession

async with AireloomSession() as session:
    product = await session.queries.search_by_doi("10.5281/zenodo.7664304")
    print(product.mainTitle)
```

→ **[Get started →](getting_started.md)**
