"""Shared base for the OpenAIRE Graph V4 entity resources."""

import inspect
import logging
from collections.abc import AsyncIterator, Callable, Mapping, Sequence
from typing import Any, ClassVar
from urllib.parse import quote

from bibliofabric.exceptions import ConfigurationError
from bibliofabric.paging import QueryDialect
from bibliofabric.resources import OnError, ResourceClient
from pydantic import BaseModel

from ..dialect import GRAPH_DIALECT
from ..filters import GraphFilters, encode_filter_value

logger = logging.getLogger(__name__)


class _CursorComplete(Exception):
    """Internal signal: the API echoed the current cursor, so iteration is done."""


class GraphResource[E: BaseModel](ResourceClient[E]):
    """Base for the five V4 entity endpoints.

    Sends all filter criteria as one V4 ``filter`` expression, validates sort
    fields per entity, serves single-entity ``get()`` through the V3 by-id
    route (V4 has none), and exposes typed ``facets``/``group_by`` helpers.
    """

    dialect: ClassVar[QueryDialect] = GRAPH_DIALECT
    sort_fields: ClassVar[frozenset[str]] = frozenset({"relevance"})
    iterate_page_size: ClassVar[int] = 100

    def build_filter_params(
        self, filters: BaseModel | Mapping[str, Any] | None
    ) -> dict[str, str]:
        """Convert filter criteria into the single V4 ``filter`` parameter.

        A ``GraphFilters`` model or a plain mapping both become ``field:value``
        entries joined with commas; list values become pipe-separated ORs.
        """
        if filters is None:
            return {}
        if isinstance(filters, Mapping):
            expression = ",".join(
                f"{field}:{encode_filter_value(value)}"
                for field, value in filters.items()
                if value is not None
            )
            return {"filter": expression} if expression else {}
        if isinstance(filters, GraphFilters):
            return {"filter": filters.to_expression()}
        dumped = filters.model_dump(exclude_none=True, by_alias=True)
        expression = ",".join(
            f"{field}:{encode_filter_value(value)}" for field, value in dumped.items()
        )
        return {"filter": expression} if expression else {}

    def format_sort(self, sort: str | Sequence[str]) -> dict[str, str]:
        """Validate sort fields against the entity's allowed fields.

        Accepts ``"citation_count:desc"`` or a list of such entries; the
        direction is optional and defaults to the API default.
        """
        if self.dialect.sort_param is None:
            return {}
        entries = [sort] if isinstance(sort, str) else list(sort)
        normalized: list[str] = []
        for entry in entries:
            for raw in entry.split(","):
                piece = raw.strip()
                if not piece:
                    continue
                field, has_dir, direction = piece.partition(":")
                if field not in self.sort_fields:
                    valid = ", ".join(sorted(self.sort_fields))
                    raise ConfigurationError(
                        f"Invalid sort field {field!r} for {type(self).__name__}. "
                        f"Valid fields: {valid}."
                    )
                if has_dir and direction.strip().lower() not in ("asc", "desc"):
                    raise ConfigurationError(
                        f"Invalid sort direction {direction!r}; use asc or desc."
                    )
                normalized.append(
                    f"{field}:{direction.strip().lower()}" if has_dir else field
                )
        return {self.dialect.sort_param: ",".join(normalized)}

    def build_batch_params(self, field: str, values: Sequence[str]) -> dict[str, Any]:
        """Encode one batch chunk as a V4 OR expression: ``field:a|b|c``."""
        return {"filter": f"{field}:{'|'.join(values)}"}

    def item_path(self, id: str) -> str:
        """Return the V3 by-id path for ``id``; V4 has no by-id route.

        Colons stay unencoded: the V3 by-id routes expect the raw
        ``prefix::suffix`` identifiers and reject the percent-encoded form.
        """
        entity = self.path.partition("/")[2]
        return f"v3/{entity}/{quote(self.normalize_id(id), safe=':')}"

    def iterate(
        self,
        filters: BaseModel | Mapping[str, Any] | None = None,
        *,
        query: str | None = None,
        sort: str | Sequence[str] | None = None,
        select: Sequence[str] | None = None,
        page_size: int | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        on_error: OnError = "raise",
        failures: list[tuple[dict[str, Any], Exception]] | None = None,
        on_page: Callable[[int, str | None], Any] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> AsyncIterator[E]:
        """Iterate over all matching entities, 100 per page by default.

        Cursor mode stops when the API stops returning ``nextCursor`` or
        echoes the current cursor back. ``on_page(page_number, next_cursor)``
        checkpoints progress, and a saved cursor passed as ``cursor=``
        resumes the harvest.
        """

        async def _guard(page_number: int, next_cursor: str | None) -> None:
            if on_page is not None:
                result = on_page(page_number, next_cursor)
                if inspect.isawaitable(result):
                    await result
            if next_cursor is not None and next_cursor == state["cursor"]:
                raise _CursorComplete
            state["cursor"] = next_cursor

        state = {"cursor": cursor}
        parent = super().iterate(
            filters,
            query=query,
            sort=sort,
            select=select,
            page_size=page_size if page_size is not None else self.iterate_page_size,
            limit=limit,
            cursor=cursor,
            on_error=on_error,
            failures=failures,
            on_page=_guard,
            params=params,
        )

        async def _guarded() -> AsyncIterator[E]:
            try:
                async for entity in parent:
                    yield entity
            except _CursorComplete:
                return

        return _guarded()

    async def facets(
        self,
        *fields: str,
        filters: BaseModel | Mapping[str, Any] | None = None,
        query: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, dict[str, int]]:
        """Return facet counts per field: ``{field: {value: count}}``.

        Requests records plus aggregations, so pass ``page_size`` to bound
        the record part (the API default page size applies otherwise).
        """
        page = await self.search(
            filters,
            query=query,
            page_size=page_size,
            params={"facets": ",".join(fields)},
        )
        raw = page.meta.get("facets") or {}
        return {
            field: {value: int(count) for value, count in buckets.items()}
            for field, buckets in raw.items()
            if isinstance(buckets, dict)
        }

    async def group_by(
        self,
        field: str,
        *,
        filters: BaseModel | Mapping[str, Any] | None = None,
        query: str | None = None,
    ) -> dict[str, int]:
        """Return counts per value of ``field`` without fetching records.

        ``group_by`` is an aggregation-only mode: the response carries counts
        and an empty ``results`` list.
        """
        page = await self.search(
            filters, query=query, page_size=1, params={"group_by": field}
        )
        raw = (page.meta.get("facets") or {}).get(field)
        if not isinstance(raw, dict):
            return {}
        return {value: int(count) for value, count in raw.items()}
