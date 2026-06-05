# tests/resources/test_data_sources_client.py
from unittest.mock import AsyncMock

import httpx
import pytest
from bibliofabric.exceptions import BibliofabricError

from aireloom.client import AireloomClient
from aireloom.constants import DEFAULT_PAGE_SIZE
from aireloom.endpoints import DATA_SOURCES, DataSourcesFilters
from aireloom.models import DataSource, Header
from aireloom.resources import DataSourcesClient
from aireloom.unwrapper import OpenAireUnwrapper


@pytest.fixture
def mock_api_client_fixture():
    """Fixture to create a mock AireloomClient."""
    mock_client = AsyncMock(spec=AireloomClient)
    mock_client._response_unwrapper = OpenAireUnwrapper()
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = {
        "header": {
            "numFound": 0,
            "pageSize": 10,
            "pageNumber": 1,
            "totalPages": 0,
            "nextCursor": None,
        },
        "results": [],
    }
    mock_client.request.return_value = mock_http_response
    return mock_client


@pytest.fixture
def data_sources_client(mock_api_client_fixture: AsyncMock) -> DataSourcesClient:
    """Fixture to create a DataSourcesClient with a mocked API client."""
    return DataSourcesClient(api_client=mock_api_client_fixture)


@pytest.mark.asyncio
async def test_get_data_source(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test getting a single data source."""
    ds_id = "ds_test_id_101"
    expected_ds_data_dict = {
        "id": ds_id,
        "officialName": "Official Test Data Source Name",
        "dataSourceTypeName": "repository",
        "type": {
            "name": "repository",
            "value": "repository",
        },  # Add both name and value for ControlledField
    }
    expected_data_source = DataSource.model_validate(expected_ds_data_dict)

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    # Use search response format with results array
    mock_http_response.json.return_value = {
        "results": [expected_ds_data_dict],
        "header": {"numFound": 1, "pageSize": 1},
    }
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    data_source = await data_sources_client.get(ds_id)

    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        DATA_SOURCES,
        params={"id": ds_id, "pageSize": 1},
        base_url_override=None,
    )
    assert data_source == expected_data_source
    assert data_source.type and data_source.type.value == "repository"


@pytest.mark.asyncio
async def test_get_data_source_not_found(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test getting a non-existent data source."""
    ds_id = "non_existent_ds_id"

    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.request = httpx.Request("GET", f"/{DATA_SOURCES}/{ds_id}")
    mock_response.json.return_value = {"error": "data source not found"}

    mock_api_client_fixture.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            message=f"Client error '404 Not Found' for url /{DATA_SOURCES}/{ds_id}",
            request=mock_response.request,
            response=mock_response,
        )
    )

    with pytest.raises(BibliofabricError) as exc_info:
        await data_sources_client.get(ds_id)

    assert f"Unexpected error fetching entity {ds_id}" in str(exc_info.value)
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        DATA_SOURCES,
        params={"id": ds_id, "pageSize": 1},
        base_url_override=None,
    )


@pytest.mark.asyncio
async def test_search_data_sources_no_filters(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test searching data sources with no filters."""
    expected_results_data = [{"id": "ds1", "officialName": "DataSource One"}]
    expected_header_data = {
        "numFound": 1,
        "pageSize": DEFAULT_PAGE_SIZE,
        "pageNumber": 1,
        "totalPages": 1,
    }
    mock_response_json = {
        "results": expected_results_data,
        "header": expected_header_data,
    }

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_response_json
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    response = await data_sources_client.search(page=1, page_size=DEFAULT_PAGE_SIZE)

    expected_params = {"page": 1, "pageSize": DEFAULT_PAGE_SIZE}
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        DATA_SOURCES,
        params=expected_params,
        base_url_override=None,
    )
    assert response.results == [
        DataSource.model_validate(item) for item in expected_results_data
    ]
    assert response.header == Header.model_validate(expected_header_data)


@pytest.mark.asyncio
async def test_search_data_sources_with_filters_and_sort(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test searching data sources with filters and sorting."""
    filters_model = DataSourcesFilters(
        officialName="OpenAIRE Nexus",
        dataSourceTypeName="aggregator",
        contentTypes=["publications"],
    )
    sort_by = "relevance desc"
    page = 1
    page_size = 5

    expected_results_data = [
        {
            "id": "openaire_nexus_ds",
            "officialName": "OpenAIRE Nexus Aggregator",
            "dataSourceTypeName": "aggregator",
        }
    ]
    expected_header_data = {
        "numFound": 1,
        "pageSize": page_size,
        "pageNumber": page,
        "totalPages": 1,
    }
    mock_response_json = {
        "results": expected_results_data,
        "header": expected_header_data,
    }

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_response_json
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    response = await data_sources_client.search(
        filters=filters_model, sort_by=sort_by, page=page, page_size=page_size
    )

    expected_params = {
        "officialName": "OpenAIRE Nexus",
        "dataSourceTypeName": "aggregator",
        "contentTypes": ["publications"],
        "sortBy": sort_by,
        "page": page,
        "pageSize": page_size,
    }

    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        DATA_SOURCES,
        params=expected_params,
        base_url_override=None,
    )
    assert response.results == [
        DataSource.model_validate(item) for item in expected_results_data
    ]
    assert response.header == Header.model_validate(expected_header_data)


@pytest.mark.asyncio
async def test_search_sort_field_passed_through(
    data_sources_client: DataSourcesClient,
    mock_api_client_fixture: AsyncMock,
):
    """Test that sort fields are passed through to the API without client-side validation.

    Since client-side sort validation was removed in the mixin migration,
    sort fields are passed directly to the API for server-side validation.
    """
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = {"results": [], "header": {"numFound": 0}}
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    # Even a non-standard sort field is accepted client-side and passed to the API
    await data_sources_client.search(sort_by="customField asc")
    call_args = mock_api_client_fixture.request.call_args
    assert call_args.kwargs.get("params", {}).get("sortBy") == "customField asc"


@pytest.mark.asyncio
async def test_iterate_data_sources(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating through data sources using cursor pagination."""
    filters_model = DataSourcesFilters(dataSourceTypeName="journal")
    page_size = 1
    sort_by = "relevance desc"

    # Page 1
    page1_results_data = [
        {
            "id": "journal_abc",
            "officialName": "Journal of ABC",
            "dataSourceTypeName": "journal",
        }
    ]
    page1_header_data = {
        "numFound": 2,
        "pageSize": page_size,
        "nextCursor": "cursor_ds_next",
    }
    mock_response_page1_json = {
        "results": page1_results_data,
        "header": page1_header_data,
    }

    # Page 2
    page2_results_data = [
        {
            "id": "journal_xyz",
            "officialName": "Journal of XYZ",
            "dataSourceTypeName": "journal",
        }
    ]
    page2_header_data = {"numFound": 2, "pageSize": page_size, "nextCursor": None}
    mock_response_page2_json = {
        "results": page2_results_data,
        "header": page2_header_data,
    }

    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json.return_value = mock_response_page1_json

    mock_http_response_page2 = AsyncMock(spec=httpx.Response)
    mock_http_response_page2.status_code = 200
    mock_http_response_page2.json.return_value = mock_response_page2_json

    # Ensure mock responses return data properly, not coroutines
    mock_http_response_page1.json = lambda: mock_response_page1_json
    mock_http_response_page2.json = lambda: mock_response_page2_json

    mock_api_client_fixture.request = AsyncMock(
        side_effect=[
            mock_http_response_page1,
            mock_http_response_page2,
        ]
    )

    iterated_ds = []
    async for ds_item in data_sources_client.iterate(
        filters=filters_model, page_size=page_size, sort_by=sort_by
    ):
        iterated_ds.append(ds_item)

    assert len(iterated_ds) == 2
    assert iterated_ds[0] == DataSource.model_validate(page1_results_data[0])
    assert iterated_ds[1] == DataSource.model_validate(page2_results_data[0])

    # Verify the mock was called the expected number of times
    assert mock_api_client_fixture.request.call_count == 2


@pytest.mark.asyncio
async def test_iterate_data_sources_no_results(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating data sources when the search yields no results."""
    filters_model = DataSourcesFilters(officialName="NonExistent DS")
    page_size = 3

    expected_header_data = {"numFound": 0, "pageSize": page_size, "nextCursor": None}
    mock_response_json = {"results": [], "header": expected_header_data}

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_response_json
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    count = 0
    async for _ in data_sources_client.iterate(
        filters=filters_model, page_size=page_size
    ):
        count += 1

    assert count == 0
    expected_params = {
        "officialName": "NonExistent DS",
        "pageSize": page_size,
        "cursor": "*",
    }
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        DATA_SOURCES,
        params=expected_params,
        base_url_override=None,
    )


@pytest.mark.asyncio
async def test_iterate_data_sources_api_error(
    data_sources_client: DataSourcesClient, mock_api_client_fixture: AsyncMock
):
    """Test API error during data source iteration."""
    filters_model = DataSourcesFilters(dataSourceTypeName="thematic_repository")
    page_size = 1

    # Page 1 - success
    page1_results_data = [
        {
            "id": "thematic_1",
            "officialName": "Thematic Repo 1",
            "dataSourceTypeName": "thematic_repository",
        }
    ]
    page1_header_data = {
        "numFound": 2,
        "pageSize": page_size,
        "nextCursor": "cursor_thematic_p2",
    }
    mock_response_page1_json = {
        "results": page1_results_data,
        "header": page1_header_data,
    }

    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json.return_value = mock_response_page1_json

    # Page 2 - error
    error_response_mock = AsyncMock(spec=httpx.Response)
    error_response_mock.status_code = 401  # Unauthorized
    error_response_mock.request = httpx.Request("GET", f"/{DATA_SOURCES}")
    error_response_mock.json.return_value = {"error": "auth error"}

    # Ensure mock response returns data properly, not coroutines
    mock_http_response_page1.json = lambda: mock_response_page1_json

    mock_api_client_fixture.request = AsyncMock(
        side_effect=[
            mock_http_response_page1,
            httpx.HTTPStatusError(
                message="Unauthorized '401'",
                request=error_response_mock.request,
                response=error_response_mock,
            ),
        ]
    )

    iterated_ds = []
    with pytest.raises(BibliofabricError) as exc_info:
        async for ds_item in data_sources_client.iterate(
            filters=filters_model, page_size=page_size
        ):
            iterated_ds.append(ds_item)

    assert len(iterated_ds) == 1  # Only first page
    assert iterated_ds[0] == DataSource.model_validate(page1_results_data[0])
    assert "Unexpected error during iteration" in str(exc_info.value)

    # Verify the mock was called the expected number of times
    assert mock_api_client_fixture.request.call_count == 2
