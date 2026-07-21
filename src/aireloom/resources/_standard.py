# aireloom/resources/_standard.py
"""Base class for standard CRUD resource clients with batch support.

Also provides the V3 filter-value quoting machinery: OpenAIRE Graph V3 requires
filter values containing spaces, parentheses, or logical operators to be
double-quoted (e.g. ``accessRightLabel="Open Access"``) and supports inline
``OR``/``AND``/``NOT`` expressions. ``GraphV3FilterSerializationMixin`` applies
that quoting automatically after the framework serializes the filter model.
"""

import re

from bibliofabric import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)
from bibliofabric.log_config import logger

from ._batch import BatchMixin

# V3 quotes values containing whitespace, parentheses, or a bare logical operator.
_V3_QUOTE_TRIGGER = re.compile(r"\b(OR|AND|NOT)\b|[\s()]")
# Filter keys that are meta/operators, not content values — never quoted.
_V3_META_FILTER_KEYS = frozenset({"logicalOperator"})


def quote_v3_filter_value(value):
    """Wrap a V3 Graph filter value in double quotes when required.

    V3 rejects values containing spaces, parentheses, or logical operators unless
    they are double-quoted. Values already wrapped (starting with ``"`` or ``(``)
    are passed through unchanged so user-supplied expressions such as
    ``("US" OR "GB") AND NOT "DE"`` are preserved. Lists are quoted element-wise;
    non-string values (bool, int) are returned unchanged.
    """
    if isinstance(value, list):
        return [quote_v3_filter_value(item) for item in value]
    if isinstance(value, str):
        if value.startswith(('"', "(")):
            return value
        if _V3_QUOTE_TRIGGER.search(value):
            return f'"{value}"'
    return value


class GraphV3FilterSerializationMixin:
    """Quote Graph V3 filter values during serialization."""

    def _serialize_filters(self, filters):
        params = super()._serialize_filters(filters)  # ty: ignore[unresolved-attribute]
        if not isinstance(params, dict):
            return params
        return {
            key: (
                value if key in _V3_META_FILTER_KEYS else quote_v3_filter_value(value)
            )
            for key, value in params.items()
        }


class StandardResourceClient(
    GraphV3FilterSerializationMixin,
    BatchMixin,
    GettableMixin,
    SearchableMixin,
    CursorIterableMixin,
    BaseResourceClient,
):
    """Base for simple CRUD resource clients that only differ in class attributes.

    Subclasses must set:
        _entity_path (str): The API path for the resource.
        _entity_model: Pydantic model for a single entity.
        _search_response_model: Pydantic model for the search response envelope.

    Subclasses may declare ``_batch_fields`` to auto-generate
    ``batch_get_by_<name>()`` convenience methods.
    """

    def __init__(self, api_client):  # noqa: ANN001 – accept generic api_client from bibliofabric
        """Initialize the resource client.

        Args:
            api_client: An instance of the parent API client.
        """
        super().__init__(api_client)
        logger.debug(
            f"{type(self).__name__} initialized for path: {self._entity_path}"  # ty: ignore[unresolved-attribute]
        )
