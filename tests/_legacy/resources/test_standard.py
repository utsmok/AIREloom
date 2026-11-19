"""Unit tests for V3 filter-value quoting in `aireloom.resources._standard`.

V3 requires filter values containing spaces, parentheses, or bare logical
operators to be double-quoted. These tests cover the `quote_v3_filter_value`
helper and the `GraphV3FilterSerializationMixin` integration, including the
exclusion of meta keys (e.g. `logicalOperator`) and element-wise handling of
list-valued filters.
"""

import pytest

from aireloom.resources._standard import (
    GraphV3FilterSerializationMixin,
    quote_v3_filter_value,
)


class _StubParent:
    """Minimal parent whose `_serialize_filters` echoes its input dict."""

    def _serialize_filters(self, filters):
        return dict(filters)


class _SerializeMixin(GraphV3FilterSerializationMixin, _StubParent):
    """Mixin under test wired to the stub parent."""


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # Plain tokens pass through unchanged.
        ("publication", "publication"),
        ("ORCID", "ORCID"),  # bare operator as a substring is NOT a word match
        ("ORANGE", "ORANGE"),  # word-boundary: no false positive
        # Whitespace triggers quoting.
        ("Open Access", '"Open Access"'),
        ("FAIR Data", '"FAIR Data"'),
        ("a b c", '"a b c"'),
        # Bare logical operator as a full word triggers quoting.
        ("OR", '"OR"'),
        ("AND", '"AND"'),
        ("NOT", '"NOT"'),
        ("relevance OR impact", '"relevance OR impact"'),
        # Already-quoted / parenthesized expressions pass through verbatim
        # so user-authored boolean expressions are preserved.
        ('"Open Access"', '"Open Access"'),
        ('"US" OR "GB"', '"US" OR "GB"'),  # starts with " -> passthrough
        ('("US" OR "GB") AND NOT "DE"', '("US" OR "GB") AND NOT "DE"'),
    ],
)
def test_quote_v3_filter_value_strings(value, expected):
    assert quote_v3_filter_value(value) == expected


def test_quote_v3_filter_value_list_is_element_wise():
    # Mixed list: only the space-containing / operator elements are quoted.
    assert quote_v3_filter_value(["green energy", "ai", "OR"]) == [
        '"green energy"',
        "ai",
        '"OR"',
    ]


def test_quote_v3_filter_value_non_strings_unchanged():
    assert quote_v3_filter_value(42) == 42
    assert quote_v3_filter_value(True) is True
    assert quote_v3_filter_value(None) is None


def test_serialize_filters_quotes_spaces_and_skips_meta_keys():
    mixin = _SerializeMixin()
    filters = {
        "mainTitle": "Open Science",
        "type": "publication",
        "logicalOperator": "OR",  # meta key — must NOT be quoted
        "subjects": ["green energy", "ai"],
    }
    out = mixin._serialize_filters(filters)
    assert out == {
        "mainTitle": '"Open Science"',
        "type": "publication",
        "logicalOperator": "OR",
        "subjects": ['"green energy"', "ai"],
    }


def test_serialize_filters_passes_non_dict_through_unchanged():
    # If the parent returns a non-dict (e.g. already-built query string),
    # the mixin must not attempt to transform it.

    class _NonDictParent:
        def _serialize_filters(self, filters):
            return "already-serialized"

    class _M(GraphV3FilterSerializationMixin, _NonDictParent):
        pass

    assert _M()._serialize_filters({"anything": "value"}) == "already-serialized"
