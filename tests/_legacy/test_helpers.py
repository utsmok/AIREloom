"""Tests for _helpers module to cover computed-field helper functions."""

import pytest

from aireloom._helpers import (
    extract_all_pids_by_scheme,
    extract_orcid,
    extract_pid_by_scheme,
)
from aireloom.models.research_product import Pid


class TestExtractPidByScheme:
    """Tests for extract_pid_by_scheme."""

    def test_basic_scheme_match(self):
        pids = [Pid(scheme="doi", value="10.1234/test")]
        assert extract_pid_by_scheme(pids, "doi") == "10.1234/test"

    def test_case_insensitive_match(self):
        pids = [Pid(scheme="DOI", value="10.1234/test")]
        assert extract_pid_by_scheme(pids, "doi") == "10.1234/test"

    def test_no_match_returns_none(self):
        pids = [Pid(scheme="pmid", value="12345")]
        assert extract_pid_by_scheme(pids, "doi") is None

    def test_empty_pids_returns_none(self):
        assert extract_pid_by_scheme([], "doi") is None

    def test_pydantic_extra_branch(self):
        """Cover the __pydantic_extra__ fallback path (lines 29-34)."""
        # Create a Pid and inject __pydantic_extra__ with scheme/value
        pid = Pid.model_construct(scheme="something", value="ignored")
        pid.__pydantic_extra__ = {"scheme": "doi", "value": "10.5678/extra"}
        assert extract_pid_by_scheme([pid], "doi") == "10.5678/extra"

    def test_pydantic_extra_no_match(self):
        pid = Pid.model_construct(scheme="x", value="y")
        pid.__pydantic_extra__ = {"scheme": "pmid", "value": "999"}
        assert extract_pid_by_scheme([pid], "doi") is None


class TestExtractAllPidsByScheme:
    """Tests for extract_all_pids_by_scheme (lines 40-46)."""

    def test_returns_all_matching(self):
        pids = [
            Pid(scheme="doi", value="10.1/a"),
            Pid(scheme="doi", value="10.1/b"),
            Pid(scheme="pmid", value="123"),
        ]
        result = extract_all_pids_by_scheme(pids, "doi")
        assert result == ["10.1/a", "10.1/b"]

    def test_no_match_returns_empty(self):
        pids = [Pid(scheme="pmid", value="123")]
        assert extract_all_pids_by_scheme(pids, "doi") == []

    def test_empty_pids(self):
        assert extract_all_pids_by_scheme([], "doi") == []

    def test_case_insensitive(self):
        pids = [Pid(scheme="DOI", value="10.1/a")]
        assert extract_all_pids_by_scheme(pids, "doi") == ["10.1/a"]


class TestExtractOrcid:
    """Tests for extract_orcid (lines 49-65)."""

    def test_from_original_ids(self):
        result = extract_orcid(["0000-0002-1825-0097"], None)
        assert result == "0000-0002-1825-0097"

    def test_from_entity_id(self):
        """Cover the entity_id branch (lines 61-64)."""
        result = extract_orcid(None, "orcid_______::0000-0001-2345-6789")
        assert result == "0000-0001-2345-6789"

    def test_entity_id_no_orcid_prefix(self):
        result = extract_orcid(None, "doi_________::10.1234")
        assert result is None

    def test_empty_original_ids_and_entity_id(self):
        assert extract_orcid([], None) is None

    def test_original_ids_no_orcid(self):
        assert extract_orcid(["some-id-123"], None) is None

    def test_entity_id_with_orcid_prefix_but_invalid(self):
        result = extract_orcid(None, "orcid_______::not-an-orcid")
        assert result is None
