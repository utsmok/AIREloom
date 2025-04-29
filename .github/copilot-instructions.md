# Tooling
- manage python environment with [uv](https://docs.astral.sh/uv/), like so:
```bash
> uv add polars   # add dependencies to the project
> uv remove polars # remove dependencies
> uv run main.py # run script main.py using the local venv
> uvx ruff check --fix # lint & fix all files in the dir
> uvx ruff format # format all files in dir
```
- format & lint code using [Ruff](https://docs.astral.sh/ruff/)
- use [pre-commit](https://pre-commit.com/) to run ruff before each commit and integrate it into github's CI.
- use python 3.9+ style type hints (see also [PEP 484 - Type Hints](https://peps.python.org/pep-0484/) and [PEP 526 – Syntax for Variable Annotations](https://peps.python.org/pep-0526/))
- use google-style docstrings:
    - every file should contain license boilerplate.
    - files should start with a docstring describing the contents and usage of the module.
    - a docstring is mandatory for every function that is part of a public API; is of nontrivial size; or has non-obvious logic.
    - docstrings should be descriptive (e.g. 'Fetches rows from a Bigtable', not 'Fetch rows from a Bigtable')



    - function docstrings should be formatted like so:
        - heading line ending with colon
        - blank line
        - description of functionality
        - 'Args:' followed by list of args w/ indent 4
        - 'Returns:'/'Yields:' semantics of the return value, including any missing type info.
        - 'Raises:' all exceptions that are relevant to the interface followed by a description.
        - example:
        ```python
        def fetch_smalltable_rows(
            table_handle: smalltable.Table,
            keys: Sequence[bytes | str],
            require_all_keys: bool = False,
        ) -> Mapping[bytes, tuple[str, ...]]:
            """Fetches rows from a Smalltable.

            Retrieves rows pertaining to the given keys from the Table instance
            represented by table_handle.  String keys will be UTF-8 encoded.

            Args:
            table_handle:
                An open smalltable.Table instance.
            keys:
                A sequence of strings representing the key of each table row to
                fetch.  String keys will be UTF-8 encoded.
            require_all_keys:
                If True only rows with values set for all keys will be returned.

            Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:

            {b'Serak': ('Rigel VII', 'Preparer'),
            b'Zim': ('Irk', 'Invader'),
            b'Lrrr': ('Omicron Persei 8', 'Emperor')}

            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).

            Raises:
            IOError: An error occurred accessing the smalltable.
            """
        ```
    - Classes docstrings below the class definition; describe the class. Start with a 1 line summary. Document public attributes, similar to 'Args:' in a function.

- use [pytest](http://pytest.org/) for testing.
- add the [pytest-randomly](https://pypi.org/project/pytest-randomly/) plugin to *pytest* to prevent test errors due to sequentialism, and [pytest-cov](https://pytest-cov.readthedocs.io/) plugin to check coverage.
- use [loguru](https://loguru.readthedocs.io/) for logging

# Codestyle & libraries
- use [polars](https://pola.rs/) for dataframes
- use [typer](https://typer.tiangolo.com/) for command line interfaces
- use [textual](https://textual.textualize.io/) for text-based UIs
- use [srsly](https://github.com/explosion/srsly) for json serializing & validation
- use dataclasses for custom data objects using either [Pydantic](https://docs.pydantic.dev/) or  built-in [data classes](https://docs.python.org/3/library/dataclasses.html) .
- use [loguru](https://loguru.readthedocs.io/) for diagnostic messages, not print()
- Use [pathlib](https://docs.python.org/3/library/pathlib.html) objects whenever you need to work with file and directory pathnames.
- replace os functions with [the pathlib equivalents](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module).
- run external commands with [subprocess](https://docs.python.org/3/library/subprocess.html)
- use [httpx](https://www.python-httpx.org/) for Web client applications; in [async](https://www.python-httpx.org/async/) form where it makes sense
- use [TOML](https://toml.io/) files for configuration (using built-in module *tomllib*)
- use JSON files for data
- use enums for immutable sets of key-value pairs, make use class inheritance where it makes sense.
- when merging dictionaries, use the union operator
- use the builtin methods from the itertools module for common tasks on iterables rather than creating code to achieve the same result
- use f-strings for string formatting.
- use Use aware *datetime* objects with the UTC time zone for timestamps, logs and other internal features.
    Use the **zoneinfo** module or datetime.now() for this, e.g.:
    ```python
    from datetime import datetime, timezone

    dt = datetime.now(timezone.utc)
    ```
- Avoid using *date* objects, except where the time of day is completely irrelevant.
- use collections.abc for custom collection types
- use breakpoint() for debugging
- Only use async where it makes sense: for I/O bound functions.Code that uses asynchronous I/O must not call *any* function that uses synchronous I/O
