# aireloom/resources/_standard.py
"""Base class for standard CRUD resource clients with batch support."""

from bibliofabric import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)
from bibliofabric.log_config import logger

from ._batch import BatchMixin


class StandardResourceClient(
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
