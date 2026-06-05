# aireloom/resources/data_sources_client.py
"""Client for interacting with the OpenAIRE Data Sources API endpoint."""

from ..endpoints import DATA_SOURCES
from ..models import DataSource, DataSourceResponse
from ._standard import StandardResourceClient


class DataSourcesClient(StandardResourceClient):
    """Client for the OpenAIRE Data Sources API endpoint.

    Attributes:
        _entity_path (str): The API path for data sources.
        _entity_model (type[DataSource]): Pydantic model for a single data source.
        _search_response_model (type[DataSourceResponse]): Pydantic model for the
                                                            search response envelope.
    """

    _entity_path: str = DATA_SOURCES
    _entity_model: type[DataSource] = DataSource
    _search_response_model: type[DataSourceResponse] = DataSourceResponse
