# Installation

## Recommended: Using `uv`

The preferred way to install AIREloom is using [`uv`](https://docs.astral.sh/uv/), a fast Python package installer and resolver.

Add AIREloom as a project dependency:

```bash
uv add aireloom
```

Or install it into the current environment:

```bash
uv pip install aireloom
```

Run a one-off script without installing:

```bash
uv run --with aireloom python your_script.py
```

This will install the latest stable version from PyPI.

## Alternative: Using `pip`

You can also install AIREloom using `pip`:

```bash
pip install aireloom
```

## From Source (for Development)

If you want to contribute to AIREloom or need the very latest (potentially unreleased) changes, you can install it from a local clone of the repository.

**Clone the repository:**

```bash
git clone https://github.com/utsmok/aireloom.git
cd aireloom
```

**Set up the environment and install with `uv`:**

AIREloom uses `uv` for environment and dependency management.

```bash
uv sync --all-extras
```

This reads `pyproject.toml` and installs AIREloom in editable mode plus all optional dependency groups (`dev`, `test`, `docs`). Changes to the source code are reflected immediately in your environment.

Run tests with `uv run pytest` and format/lint with `uv run ruff format .` and `uv run ruff check --fix .`.
