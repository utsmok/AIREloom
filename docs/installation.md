# Installation

AIREloom is available on [PyPI](https://pypi.org/project/aireloom/).

## uv (recommended)

Add as a project dependency:

```bash
uv add aireloom
```

Install into the current environment:

```bash
uv pip install aireloom
```

One-off script without installing:

```bash
uv run --with aireloom python your_script.py
```

## pip (alternative)

```bash
pip install aireloom
```

## From source (development only)

```bash
git clone https://github.com/utsmok/aireloom.git
cd aireloom
uv sync --all-extras
```

This installs AIREloom in editable mode with all dev, test, and docs dependencies.
