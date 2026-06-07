"""BatchMixin — batch retrieval for OpenAIRE Graph API resource clients.

OpenAIRE supports comma-separated filter values with OR semantics::

    ?pid=10.1038/a,10.1038/b,10.1038/c

The maximum practical batch size is **10** identifiers per request.

Subclasses that declare ``_batch_fields`` (a dict mapping a friendly name
to an OpenAIRE filter parameter) automatically get ``batch_get_by_<name>()``
convenience methods at class-creation time.

Example::

    class ResearchProductsClient(BatchMixin, ...):
        _batch_fields = {
            "doi": "pid",
            "openaire_id": "id",
            "original_id": "originalId",
        }


    # Auto-generated:
    #   await client.batch_get_by_doi(["10.1038/a", "10.1038/b"])
    #   await client.batch_get_by_openaire_id(["doi_dedup___::xxx"])
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

#: Maximum identifiers per comma-separated filter (OpenAIRE practical limit).
BATCH_GET_SIZE = 10


def _normalize_id(raw: str) -> str:
    """Lowercase and strip common URL prefixes for consistent key matching."""
    key = raw.strip().lower()
    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "https://ror.org/",
        "http://ror.org/",
    ):
        key = key.removeprefix(prefix)
    return key


def _make_batch_getter(suffix: str, filter_param: str) -> Any:
    """Return an async method that delegates to :meth:`batch_get`."""

    async def _batch_get_by(
        self: BatchMixin, identifiers: list[str], **kwargs: Any
    ) -> dict[str, Any]:
        return await self.batch_get(identifiers, filter_param=filter_param, **kwargs)

    _batch_get_by.__name__ = f"batch_get_by_{suffix}"
    _batch_get_by.__qualname__ = f"batch_get_by_{suffix}"
    return _batch_get_by


class BatchMixin:
    """Mixin providing ``batch_get()`` and auto-generated convenience methods.

    Subclasses must:
    - Also inherit from a ``SearchableMixin`` provider (from bibliofabric).
    - Set ``_entity_model`` to the Pydantic model class for a single entity.
    - Optionally declare ``_batch_fields`` for auto-generated methods.
    """

    _batch_fields: dict[str, str] = {}
    _entity_model: type[BaseModel] | None = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for suffix, filter_param in getattr(cls, "_batch_fields", {}).items():
            method_name = f"batch_get_by_{suffix}"
            if not hasattr(cls, method_name):
                setattr(cls, method_name, _make_batch_getter(suffix, filter_param))

    async def batch_get(
        self,
        identifiers: list[str],
        *,
        filter_param: str = "pid",
        key_fn: Callable[[Any], str | None] | None = None,
        batch_size: int = BATCH_GET_SIZE,
    ) -> dict[str, Any]:
        """Retrieve multiple entities by identifier in batched queries.

        Splits *identifiers* into groups of *batch_size* (default 10, the
        OpenAIRE practical maximum) and issues one ``search`` per group
        using comma-separated OR filter syntax.

        Results are returned as ``{normalized_identifier: entity}``;
        identifiers not found are omitted.

        Args:
            identifiers: Values to look up (DOIs, OpenAIRE IDs, etc.).
            filter_param: Filter parameter name (``"pid"``, ``"id"``,
                ``"originalId"``, ``"code"``).
            key_fn: Optional function to extract the lookup key from a
                parsed entity. Defaults to a scheme-aware resolver.
            batch_size: Max identifiers per API call (1–10).

        Returns:
            Dict mapping each *identifier* to its parsed entity (Pydantic model).
        """
        if not identifiers:
            return {}
        batch_size = max(1, min(batch_size, BATCH_GET_SIZE))
        results: dict[str, Any] = {}
        for i in range(0, len(identifiers), batch_size):
            batch = identifiers[i : i + batch_size]
            comma_value = ",".join(batch)
            response = await self.search(  # ty: ignore[unresolved-attribute]
                page=1,
                page_size=batch_size,
                filters={filter_param: comma_value},
            )
            entities = _extract_results(response)
            for entity in entities:
                key = _resolve_key(entity, filter_param, key_fn, identifiers)
                if key is not None:
                    results[key] = entity
        return results


def _extract_results(response: Any) -> list[Any]:
    """Pull the results list from a search response (model or raw dict)."""
    if isinstance(response, BaseModel) and hasattr(response, "results"):
        return list(response.results or [])
    if isinstance(response, dict):
        return list(response.get("results") or [])
    return []


def _resolve_key(
    entity: Any,
    filter_param: str,
    key_fn: Callable[[Any], str | None] | None,
    input_identifiers: list[str],
) -> str | None:
    """Derive the lookup key from a parsed entity."""
    if key_fn is not None:
        return key_fn(entity)

    if filter_param == "id":
        # OpenAIRE id → entity.id directly
        raw = getattr(entity, "id", None)
        if raw is None and isinstance(entity, dict):
            raw = entity.get("id")
        return _normalize_id(str(raw)) if raw else None

    if filter_param == "pid":
        # pid filter is matched against entity.pids[].value
        # We need to find which input identifier matches this entity
        return _match_pid_entity(entity, input_identifiers)

    if filter_param == "code":
        raw = getattr(entity, "code", None)
        if raw is None and isinstance(entity, dict):
            raw = entity.get("code")
        return str(raw).strip() if raw else None

    if filter_param == "originalId":
        # Match against originalId/originalIds
        raw_ids = getattr(entity, "originalId", None) or getattr(
            entity, "originalIds", None
        )
        if raw_ids is None and isinstance(entity, dict):
            raw_ids = entity.get("originalId") or entity.get("originalIds")
        if isinstance(raw_ids, list) and raw_ids:
            return _normalize_id(str(raw_ids[0]))
        return None

    # Generic: try entity.<filter_param>
    raw = getattr(entity, filter_param, None)
    if raw is None and isinstance(entity, dict):
        raw = entity.get(filter_param)
    if raw is None:
        return None
    if isinstance(raw, list):
        raw = raw[0] if raw else None
        if raw is None:
            return None
    return _normalize_id(str(raw))


def _match_pid_entity(entity: Any, input_identifiers: list[str]) -> str | None:
    """Find which input identifier matches an entity's pids or id field.

    OpenAIRE's pid filter matches against the entity's pid/pids values.
    We normalize all input identifiers and check if any match.
    """
    # Build set of normalized inputs for O(1) lookup
    normalized_inputs = {_normalize_id(id_) for id_ in input_identifiers}

    # Check pids field (list of Pid objects with scheme/value)
    pids = getattr(entity, "pids", None)
    if pids:
        for pid in pids:
            value = getattr(pid, "value", None)
            if value:
                nv = _normalize_id(str(value))
                if nv in normalized_inputs:
                    return nv

    # Check pid field (single or list)
    pid = getattr(entity, "pid", None)
    if pid:
        if isinstance(pid, list):
            for p in pid:
                v = getattr(p, "value", None) or (p if isinstance(p, str) else None)
                if v:
                    nv = _normalize_id(str(v))
                    if nv in normalized_inputs:
                        return nv
        else:
            nv = _normalize_id(str(pid))
            if nv in normalized_inputs:
                return nv

    # Fallback: check entity.id (OpenAIRE IDs like doi_dedup___::hash)
    eid = getattr(entity, "id", None)
    if eid:
        neid = _normalize_id(str(eid))
        if neid in normalized_inputs:
            return neid

    return None
