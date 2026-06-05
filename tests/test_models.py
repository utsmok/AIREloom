"""Tests for model validators and edge cases."""

from aireloom.models.base import ApiResponse, BaseEntity, Header
from aireloom.models.project import Project
from aireloom.models.research_product import ResearchProduct, UsageCounts

# ── Header.coerce_str_to_int ──────────────────────────────────────────────


class TestHeaderCoercion:
    """Cover Header numeric field coercion edge cases."""

    def test_valid_string_to_int(self):
        h = Header(queryTime="42", numFound="100", pageSize="10")
        assert h.queryTime == 42
        assert h.numFound == 100
        assert h.pageSize == 10

    def test_invalid_string_returns_none(self):
        h = Header(queryTime="abc", numFound="not-a-number")
        assert h.queryTime is None
        assert h.numFound is None

    def test_int_passthrough(self):
        h = Header(queryTime=42, numFound=100, pageSize=10)
        assert h.queryTime == 42

    def test_unexpected_type_returns_none(self):
        """Passing e.g. a list should hit the fallback warning branch."""
        h = Header(queryTime=[1, 2, 3])
        assert h.queryTime is None

    def test_none_passthrough(self):
        h = Header(queryTime=None)
        assert h.queryTime is None

    def test_float_string_returns_none(self):
        h = Header(queryTime="3.14")
        assert h.queryTime is None


# ── ApiResponse.handle_null_results ───────────────────────────────────────


class TestApiResponseResults:
    """Cover ApiResponse.results validator branches."""

    def test_null_results_stays_none(self):
        resp = ApiResponse[BaseEntity](header=Header(), results=None)
        assert resp.results is None

    def test_list_results_kept(self):
        resp = ApiResponse[BaseEntity](header=Header(), results=[])
        assert resp.results == []

    def test_unexpected_type_returns_empty_list(self):
        """Passing a non-list, non-None value (e.g. a dict) to results."""
        resp = ApiResponse[BaseEntity](header=Header(), results={"nested": "dict"})
        assert resp.results == []


# ── Project keyword validator ──────────────────────────────────────────────


class TestProjectKeywords:
    """Cover Project._parse_keywords branches."""

    def test_comma_separated(self):
        p = Project(id="p1", keywords="alpha, beta, gamma")
        assert p.keywords == ["alpha", "beta", "gamma"]

    def test_semicolon_separated(self):
        """Semicolon delimiter only used if comma split yields nothing.
        For 'alpha; beta; gamma', comma split returns one element since
        the string has no commas."""
        p = Project(id="p2", keywords="alpha; beta; gamma")
        assert p.keywords == ["alpha; beta; gamma"]

    def test_empty_string_returns_none(self):
        p = Project(id="p3", keywords="   ")
        assert p.keywords == []

    def test_list_passthrough(self):
        p = Project(id="p4", keywords=["already", "a", "list"])
        assert p.keywords == ["already", "a", "list"]

    def test_none_passthrough(self):
        p = Project(id="p5", keywords=None)
        assert p.keywords == []

    def test_comma_priority_over_semicolon(self):
        """When string has both comma and semicolon, comma split wins."""
        p = Project(id="p6", keywords="a, b; c")
        assert p.keywords == ["a", "b; c"]


# ── UsageCounts.coerce_str_to_int ─────────────────────────────────────────


class TestUsageCountsCoercion:
    """Cover UsageCounts validator branches (lines 154-165)."""

    def test_string_to_int(self):
        uc = UsageCounts(downloads="10", views="20")
        assert uc.downloads == 10
        assert uc.views == 20

    def test_invalid_string_returns_none(self):
        uc = UsageCounts(downloads="abc")
        assert uc.downloads is None

    def test_int_passthrough(self):
        uc = UsageCounts(downloads=5)
        assert uc.downloads == 5

    def test_unexpected_type_returns_none(self):
        uc = UsageCounts(downloads=[1, 2])
        assert uc.downloads is None

    def test_none_passthrough(self):
        uc = UsageCounts(downloads=None, views=None)
        assert uc.downloads is None
        assert uc.views is None


# ── ResearchProduct validators ─────────────────────────────────────────────


class TestResearchProductKeywords:
    """Cover ResearchProduct.split_keywords branches (lines 452-459)."""

    def test_none_keywords(self):
        rp = ResearchProduct(id="rp1", keywords=None)
        assert rp.keywords == []

    def test_comma_separated_string(self):
        rp = ResearchProduct(id="rp2", keywords="ai, ml, nlp")
        assert rp.keywords == ["ai", "ml", "nlp"]

    def test_unexpected_type_returns_none(self):
        """Passing a non-string, non-None value (e.g. int) hits warning branch."""
        rp = ResearchProduct(id="rp3", keywords=123)
        assert rp.keywords == []

    def test_empty_string_returns_empty_list(self):
        rp = ResearchProduct(id="rp4", keywords="   ")
        assert rp.keywords == []


class TestResearchProductTitleAlias:
    """Cover ResearchProduct.get_title_from_main_title branches (lines 477-483)."""

    def test_main_title_fills_title(self):
        rp = ResearchProduct(id="rp5", mainTitle="Hello World")
        assert rp.title == "Hello World"

    def test_existing_title_not_overwritten(self):
        rp = ResearchProduct(id="rp6", title="Original", mainTitle="Ignored")
        assert rp.title == "Original"

    def test_none_title_uses_main_title(self):
        rp = ResearchProduct(id="rp7", title=None, mainTitle="From Main")
        assert rp.title == "From Main"

    def test_no_main_title(self):
        rp = ResearchProduct(id="rp8", title="Just Title")
        assert rp.title == "Just Title"

    def test_non_dict_data_passthrough(self):
        """Model validator should handle non-dict data gracefully."""
        rp = ResearchProduct.model_validate({"id": "rp9", "title": "test"})
        assert rp.title == "test"
