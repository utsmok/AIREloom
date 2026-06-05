# AIREloom

**Async Python client for the [OpenAIRE Graph API](https://graph.openaire.eu/).**

[![PyPI](https://img.shields.io/pypi/v/aireloom)](https://pypi.org/project/aireloom/)

Built on [bibliofabric](https://github.com/afuetterer/bibliofabric), AIREloom provides a modern, typed interface to the OpenAIRE research graph — research products, projects, organizations, data sources, persons, and Scholix links.

## Features

- **Async/await first** -- native asyncio client with context-manager sessions
- **Typed models** -- Pydantic v2 for every response, with IDE autocomplete everywhere
- **Cursor pagination** -- `iterate()`, `collect()`, `count()`, `first()` on every resource
- **Ergonomics** -- computed properties, safe types (`SafeList`, `SafeStr`), convenience queries
- **Full coverage** -- research products, projects, organizations, data sources, persons, Scholix links

## Install

```bash
uv add aireloom
```

## Quick Start

<iframe src="https://marimo.app/github/utsmok/AIREloom/blob/main/examples/simple_example.py/wasm?embed=true&mode=read" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" style="width:100%;height:500px;border:none;border-radius:8px;"></iframe>

[Get started](getting_started.md)
