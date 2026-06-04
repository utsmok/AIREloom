# aireloom/resources/data_sources_client.py
"""Client for interacting with the OpenAIRE Data Sources API endpoint.

This module provides the `DataSourcesClient`, which facilitates access to
OpenAIRE's data source information. It leverages generic mixins from
`bibliofabric.resources` for common API operations like retrieving individual
entities, searching, and iterating through result sets.
"""

from typing import TYPE_CHECKING

from bibliofabric.log_config import logger
from bibliofabric.resources import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)

if TYPE_CHECKING:
    from ..client import AireloomClient
from ..endpoints import DATA_SOURCES
from ..models import DataSource, DataSourceResponse


class DataSourcesClient(
    GettableMixin, SearchableMixin, CursorIterableMixin, BaseResourceClient
):
    """Client for the OpenAIRE Data Sources API endpoint.

    This client provides standardized methods (`get`, `search`, `iterate`) for
    accessing data source information, by inheriting from `bibliofabric` mixins.
    It is configured with the specific API path and Pydantic models relevant
    to OpenAIRE data sources.

    Attributes:
        _entity_path (str): The API path for data sources.
        _entity_model (type[DataSource]): Pydantic model for a single data source.
        _search_response_model (type[DataSourceResponse]): Pydantic model for the
                                                            search response envelope.
    """

    _entity_path: str = DATA_SOURCES
    _entity_model: type[DataSource] = DataSource
    _search_response_model: type[DataSourceResponse] = DataSourceResponse

    def __init__(self, api_client: "AireloomClient"):
        """Initializes the DataSourcesClient.

        Args:
            api_client: An instance of AireloomClient.
        """
        super().__init__(api_client)
        logger.debug(f"DataSourcesClient initialized for path: {self._entity_path}")

    # All get, search, and iterate methods are now provided by the mixins
