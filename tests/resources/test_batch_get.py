"""Tests for BatchMixin batch retrieval functionality."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aireloom.resources._batch import (
    BATCH_GET_SIZE,
    BatchMixin,
    _extract_results,
    _match_pid_entity,
    _normalize_id,
    _resolve_key,
)


# ── Simple test entities ──────────────────────────────────────────────────


@dataclass
class FakePid:
    scheme: str = ""
    value: str = ""


@dataclass
class FakeEntity:
    id: str = ""
    pids: list[FakePid] = field(default_factory=list)
    code: str | None = None
    originalIds: list[str] | None = None
    originalId: list[str] | None = None


# ── Unit tests: _normalize_id ─────────────────────────────────────────────


class TestNormalizeId:
    def test_bare_doi(self):
        assert _normalize_id("10.1038/nature12373") == "10.1038/nature12373"

    def test_doi_url(self):
        assert (
            _normalize_id("https://doi.org/10.1038/nature12373")
            == "10.1038/nature12373"
        )

    def test_http_doi_url(self):
        assert (
            _normalize_id("http://doi.org/10.1038/nature12373") == "10.1038/nature12373"
        )

    def test_ror_url(self):
        assert _normalize_id("https://ror.org/0576by029") == "0576by029"

    def test_uppercase_normalized(self):
        assert _normalize_id("10.1038/NATURE12373") == "10.1038/nature12373"

    def test_whitespace_stripped(self):
        assert _normalize_id("  10.1038/nature12373  ") == "10.1038/nature12373"


# ── Unit tests: _extract_results ──────────────────────────────────────────


class TestExtractResults:
    def test_dict_with_results(self):
        assert _extract_results({"results": [1, 2, 3]}) == [1, 2, 3]

    def test_empty_results(self):
        assert _extract_results({"results": None}) == []

    def test_no_results_key(self):
        assert _extract_results({"other": 1}) == []


# ── Unit tests: _resolve_key ──────────────────────────────────────────────


class TestResolveKey:
    def test_id_filter(self):
        entity = FakeEntity(id="doi_dedup___::abc123")
        key = _resolve_key(entity, "id", None, [])
        assert key == "doi_dedup___::abc123"

    def test_code_filter(self):
        entity = FakeEntity(code="894010")
        key = _resolve_key(entity, "code", None, [])
        assert key == "894010"

    def test_pid_filter_matches_input(self):
        entity = FakeEntity(pids=[FakePid("doi", "10.1038/nature12373")])
        key = _resolve_key(
            entity, "pid", None, ["10.1038/nature12373", "10.1038/nature12374"]
        )
        assert key == "10.1038/nature12373"

    def test_originalId_filter(self):
        entity = FakeEntity(originalIds=["0000-0002-3411-2884"])
        key = _resolve_key(entity, "originalId", None, [])
        assert key == "0000-0002-3411-2884"

    def test_custom_key_fn(self):
        entity = FakeEntity(id="abc")
        key = _resolve_key(entity, "anything", lambda e: "custom", [])
        assert key == "custom"


# ── Unit tests: _match_pid_entity ─────────────────────────────────────────


class TestMatchPidEntity:
    def test_match_from_pids(self):
        entity = FakeEntity(pids=[FakePid("doi", "10.1038/nature12373")])
        result = _match_pid_entity(entity, ["10.1038/nature12373", "10.1038/other"])
        assert result == "10.1038/nature12373"

    def test_match_doi_url_normalized(self):
        entity = FakeEntity(pids=[FakePid("doi", "10.1038/nature12373")])
        result = _match_pid_entity(entity, ["https://doi.org/10.1038/nature12373"])
        assert result == "10.1038/nature12373"

    def test_no_match(self):
        entity = FakeEntity(pids=[FakePid("doi", "10.1038/other")])
        result = _match_pid_entity(entity, ["10.1038/nature12373"])
        assert result is None


# ── Integration tests: BatchMixin.batch_get ───────────────────────────────


class _FakeClient(BatchMixin):
    """Minimal client for testing batch_get without real API calls."""

    _entity_model = None
    _batch_fields = {"doi": "pid", "openaire_id": "id"}

    async def search(self, page=1, page_size=20, filters=None, **kwargs):
        """Mock search that returns entities matching filter values."""
        if filters is None:
            filters = {}
        pid_val = filters.get("pid", "")
        id_val = filters.get("id", "")
        results = []

        if pid_val:
            for doi in pid_val.split(","):
                results.append(
                    FakeEntity(
                        id=f"doi_dedup___::{doi[:8]}",
                        pids=[FakePid("doi", doi)],
                    )
                )

        if id_val:
            for oid in id_val.split(","):
                results.append(FakeEntity(id=oid))

        resp = {"results": results}
        return resp


class TestBatchGet:
    @pytest.mark.asyncio
    async def test_batch_get_empty(self):
        client = _FakeClient()
        result = await client.batch_get([])
        assert result == {}

    @pytest.mark.asyncio
    async def test_batch_get_single(self):
        client = _FakeClient()
        result = await client.batch_get(["10.1038/nature12373"], filter_param="pid")
        assert len(result) == 1
        assert "10.1038/nature12373" in result

    @pytest.mark.asyncio
    async def test_batch_get_multiple(self):
        client = _FakeClient()
        dois = [f"10.1038/nature{i}" for i in range(5)]
        result = await client.batch_get(dois, filter_param="pid")
        assert len(result) == 5

    @pytest.mark.asyncio
    async def test_batch_get_by_doi_auto(self):
        client = _FakeClient()
        result = await client.batch_get_by_doi(
            ["10.1038/nature12373", "10.1038/nature12374"]
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_batch_get_by_openaire_id_auto(self):
        client = _FakeClient()
        result = await client.batch_get_by_openaire_id(
            ["doi_dedup___::abc", "doi_dedup___::def"]
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_batch_size_clamped(self):
        client = _FakeClient()
        result = await client.batch_get(
            ["10.1038/a"], filter_param="pid", batch_size=100
        )
        assert len(result) == 1


# ── Auto-generation tests ─────────────────────────────────────────────────


class TestAutoGeneration:
    def test_batch_fields_generates_methods(self):
        """Subclass with _batch_fields gets auto-generated methods."""
        assert hasattr(_FakeClient, "batch_get_by_doi")
        assert hasattr(_FakeClient, "batch_get_by_openaire_id")

    def test_no_batch_fields_no_methods(self):
        """Subclass without _batch_fields gets no extra methods."""

        class NoBatch(BatchMixin):
            _entity_model = None
            _batch_fields = {}

        assert not hasattr(NoBatch, "batch_get_by_doi")

    @pytest.mark.asyncio
    async def test_manual_override_not_replaced(self):
        """If a subclass manually defines the method, it's not overwritten."""

        class Manual(BatchMixin):
            _entity_model = None
            _batch_fields = {"doi": "pid"}

            async def batch_get_by_doi(self, ids):
                return "manual"

        result = await Manual().batch_get_by_doi([])
        assert result == "manual"

    def test_batch_get_size_constant(self):
        assert BATCH_GET_SIZE == 10
