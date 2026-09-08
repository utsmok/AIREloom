# tests/resources/test_scholix_client.py
from unittest.mock import AsyncMock, call

import httpx
import pytest
from bibliofabric.exceptions import BibliofabricError, ValidationError

from aireloom.client import AireloomClient
from aireloom.constants import DEFAULT_PAGE_SIZE, OPENAIRE_SCHOLIX_API_BASE_URL
from aireloom.endpoints import SCHOLIX, ScholixFilters
from aireloom.models import (
    ScholixRelationship,
    ScholixResponse,
    ScholixV1Link,
)
from aireloom.resources import ScholixClient
from aireloom.unwrapper import OpenAireUnwrapper


@pytest.fixture
def mock_api_client_fixture():
    """Fixture to create a mock AireloomClient."""
    mock_client = AsyncMock(spec=AireloomClient)
    mock_client._response_unwrapper = OpenAireUnwrapper()
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    # Default Scholix response for mock
    mock_http_response.json.return_value = {
        "currentPage": 0,
        "totalPages": 0,
        "totalLinks": 0,
        "result": [],
    }
    mock_client.request.return_value = mock_http_response
    return mock_client


@pytest.fixture
def scholix_client(mock_api_client_fixture: AsyncMock) -> ScholixClient:
    """Fixture to create a ScholixClient with a mocked API client."""
    return ScholixClient(api_client=mock_api_client_fixture)


# Helper to create ScholixRelationship test data
def create_mock_scholix_link_data(
    source_pid: str, target_pid: str, rel_type: str = "References"
) -> dict:
    return {
        "LinkProvider": [{"Name": "Test Provider"}],
        "LinkPublicationDate": "2023-01-01T00:00:00Z",
        "RelationshipType": {"Name": rel_type},
        "Source": {
            "Identifier": [{"ID": source_pid, "IDScheme": "doi"}],
            "Type": "publication",
        },
        "Target": {
            "Identifier": [{"ID": target_pid, "IDScheme": "doi"}],
            "Type": "dataset",
        },
    }


@pytest.mark.asyncio
async def test_search_scholix_links(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Test searching for Scholix links."""
    source_pid_val = "10.1234/source.pid"
    target_pid_val = "10.5678/target.pid"
    page_size = 5
    page_number = 0  # Scholix is 0-indexed

    mock_link_dict = create_mock_scholix_link_data(source_pid_val, target_pid_val)
    expected_results_data = [mock_link_dict]
    expected_link_model = ScholixRelationship.model_validate(mock_link_dict)

    mock_api_response_dict = {
        "currentPage": page_number,
        "totalPages": 1,
        "totalLinks": 1,
        "result": expected_results_data,
    }
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_api_response_dict
    mock_api_client_fixture.request.return_value = mock_http_response

    filters = ScholixFilters(sourcePid=source_pid_val)
    response = await scholix_client.search_links(
        filters=filters, page=page_number, page_size=page_size
    )

    expected_params = {
        "sourcePid": source_pid_val,
        "page": page_number,
        "size": page_size,
    }
    mock_api_client_fixture.request.assert_called_once_with(
        method="GET",
        path=SCHOLIX,
        params=expected_params,
        base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
        data=None,  # Added missing args
        json_data=None,  # Added missing args
    )
    assert response is not None
    assert response.result is not None
    assert len(response.result) == 1
    assert response.result[0] == expected_link_model
    assert response.current_page == page_number
    assert response.total_links == 1
    assert response.total_pages == 1


@pytest.mark.asyncio
async def test_search_scholix_links_missing_pid_filter(scholix_client: ScholixClient):
    """Test search_links raises ValueError if no PID filter is provided."""
    with pytest.raises(ValueError) as exc_info:
        await scholix_client.search_links(filters=ScholixFilters())  # Empty filters
    assert "Either sourcePid or targetPid must be provided" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info_none:
        await scholix_client.search_links(filters=None)  # No filters
    assert "Either sourcePid or targetPid must be provided" in str(exc_info_none.value)


@pytest.mark.asyncio
async def test_iterate_scholix_links(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating through Scholix links."""
    target_pid_val = "10.9876/target.pid"
    page_size = 1

    link1_dict = create_mock_scholix_link_data(
        "10.111/source1", target_pid_val, "IsReferencedBy"
    )
    link2_dict = create_mock_scholix_link_data(
        "10.222/source2", target_pid_val, "IsSupplementTo"
    )

    expected_link1_model = ScholixRelationship.model_validate(link1_dict)
    expected_link2_model = ScholixRelationship.model_validate(link2_dict)

    page1_response_dict = {
        "currentPage": 0,
        "totalPages": 2,
        "totalLinks": 2,
        "result": [link1_dict],
    }
    page2_response_dict = {
        "currentPage": 1,
        "totalPages": 2,
        "totalLinks": 2,
        "result": [link2_dict],
    }

    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json.return_value = page1_response_dict

    mock_http_response_page2 = AsyncMock(spec=httpx.Response)
    mock_http_response_page2.status_code = 200
    mock_http_response_page2.json.return_value = page2_response_dict

    mock_api_client_fixture.request.side_effect = [
        mock_http_response_page1,
        mock_http_response_page2,
    ]

    iterated_links = []
    filters = ScholixFilters(targetPid=target_pid_val)
    async for link in scholix_client.iterate_links(
        filters=filters, page_size=page_size
    ):
        iterated_links.append(link)

    assert len(iterated_links) == 2
    assert iterated_links[0] == expected_link1_model
    assert iterated_links[1] == expected_link2_model

    expected_calls = [
        call(
            method="GET",
            path=SCHOLIX,
            params={"targetPid": target_pid_val, "size": page_size, "page": 0},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
            data=None,
            json_data=None,
        ),
        call(
            method="GET",
            path=SCHOLIX,
            params={"targetPid": target_pid_val, "size": page_size, "page": 1},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
            data=None,
            json_data=None,
        ),
    ]
    mock_api_client_fixture.request.assert_has_calls(expected_calls)
    assert mock_api_client_fixture.request.call_count == 2


@pytest.mark.asyncio
async def test_iterate_scholix_links_no_results(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating Scholix links when the search yields no results."""
    source_pid_val = "10.000/no.links.here"
    page_size = DEFAULT_PAGE_SIZE

    mock_api_response_dict = {
        "currentPage": 0,
        "totalPages": 0,
        "totalLinks": 0,
        "result": [],
    }
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_api_response_dict
    mock_api_client_fixture.request.return_value = mock_http_response

    count = 0
    filters = ScholixFilters(sourcePid=source_pid_val)
    async for _ in scholix_client.iterate_links(filters=filters, page_size=page_size):
        count += 1

    assert count == 0
    expected_params = {"sourcePid": source_pid_val, "page": 0, "size": page_size}
    mock_api_client_fixture.request.assert_called_once_with(
        method="GET",
        path=SCHOLIX,
        params=expected_params,
        base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
        data=None,
        json_data=None,
    )


@pytest.mark.asyncio
async def test_iterate_scholix_links_zero_total_pages_with_results(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Test iteration when API returns results but total_pages=0 (lines 214-218)."""
    source_pid_val = "10.1234/zero.pages"
    page_size = 5

    link_data = create_mock_scholix_link_data("10.src/a", "10.tgt/b")
    mock_api_response_dict = {
        "currentPage": 0,
        "totalPages": 0,
        "totalLinks": 0,
        "result": [link_data],  # Non-empty result, but total_pages=0
    }
    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_api_response_dict
    mock_api_client_fixture.request.return_value = mock_http_response

    collected = []
    filters = ScholixFilters(sourcePid=source_pid_val)
    async for link in scholix_client.iterate_links(
        filters=filters, page_size=page_size
    ):
        collected.append(link)

    # Should yield the one result from the page, then break due to total_pages==0
    assert len(collected) == 1


@pytest.mark.asyncio
async def test_iterate_scholix_links_bibliofabric_reraise(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """BibliofabricError from search_links is re-raised by iterate (lines 227-228)."""
    source_pid_val = "10.1234/biblio.iter.err"
    page_size = 5

    # search_links wraps RuntimeError into BibliofabricError, which iterate re-raises
    mock_api_client_fixture.request.side_effect = RuntimeError("boom")

    filters = ScholixFilters(sourcePid=source_pid_val)
    with pytest.raises(BibliofabricError):
        async for _ in scholix_client.iterate_links(
            filters=filters, page_size=page_size
        ):
            pass


@pytest.mark.asyncio
async def test_search_scholix_links_bibliofabric_error_reraise(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """BibliofabricError during search_links is re-raised directly (line 152)."""
    source_pid_val = "10.1234/biblio.err"
    page_size = 5

    mock_api_client_fixture.request.side_effect = BibliofabricError("direct error")

    filters = ScholixFilters(sourcePid=source_pid_val)
    with pytest.raises(BibliofabricError, match="direct error"):
        await scholix_client.search_links(filters=filters, page=0, page_size=page_size)


@pytest.mark.asyncio
async def test_search_scholix_links_validation_error_reraise(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """ValidationError during search_links is re-raised directly (line 152)."""
    source_pid_val = "10.1234/val.err"
    page_size = 5

    mock_api_client_fixture.request.side_effect = ValidationError("validation failed")

    filters = ScholixFilters(sourcePid=source_pid_val)
    with pytest.raises(ValidationError, match="validation failed"):
        await scholix_client.search_links(filters=filters, page=0, page_size=page_size)


@pytest.mark.asyncio
async def test_search_scholix_links_unexpected_error(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Non-library error during search_links is wrapped in BibliofabricError."""
    source_pid_val = "10.1234/unexpected.err"
    page_size = 5

    mock_api_client_fixture.request.side_effect = RuntimeError("unexpected")

    filters = ScholixFilters(sourcePid=source_pid_val)
    with pytest.raises(BibliofabricError, match="Unexpected error searching"):
        await scholix_client.search_links(filters=filters, page=0, page_size=page_size)


def test_scholix_subtype_aliases():
    link = ScholixRelationship.model_validate(
        {
            "RelationshipType": {
                "Name": "References",
                "subType": "citation",
                "subTypeSchema": "datacite",
            },
            "Source": {
                "Identifier": [{"id": "10.1234/source", "idScheme": "doi"}],
                "Type": "publication",
                "subType": "Article",
            },
            "Target": {
                "Identifier": [{"id": "10.1234/target", "idScheme": "doi"}],
                "Type": "dataset",
                "subType": "Dataset",
            },
        }
    )

    assert link.relationship_type.sub_type == "citation"
    assert link.relationship_type.sub_type_schema == "datacite"
    assert link.source.sub_type == "Article"
    assert link.source.identifier[0].id_val == "10.1234/source"


def test_scholix_response_normalizes_legacy_shapes():
    link = create_mock_scholix_link_data("10.1234/source", "10.1234/target")

    assert ScholixResponse.model_validate([link]).result
    assert ScholixResponse.model_validate({"links": [link]}).result


def test_scholix_payload_record_extraction_shapes():
    assert ScholixClient._records_from_payload([{"id": 1}]) == [{"id": 1}]
    assert ScholixClient._records_from_payload({"unknown": "shape"}) == []


@pytest.mark.asyncio
async def test_search_scholix_links_v2(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "currentPage": 0,
        "totalPages": 1,
        "totalLinks": 0,
        "result": [],
    }
    mock_api_client_fixture.request.return_value = mock_response

    response = await scholix_client.search_links_v2(
        page=0,
        page_size=100,
        filters=ScholixFilters(linkProvider="OpenCitations"),
    )

    assert response.total_links == 0
    mock_api_client_fixture.request.assert_called_once_with(
        method="GET",
        path="Links",
        params={"page": 0, "size": 99, "linkProvider": "OpenCitations"},
        base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v2"),
        data=None,
        json_data=None,
    )


@pytest.mark.asyncio
async def test_iterate_scholix_links_v2(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    link = create_mock_scholix_link_data("10.1234/source", "10.1234/target")
    responses = []
    for page in range(2):
        response = AsyncMock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {
            "currentPage": page,
            "totalPages": 2,
            "totalLinks": 2,
            "result": [link],
        }
        responses.append(response)
    mock_api_client_fixture.request = AsyncMock(side_effect=responses)

    results = [
        item
        async for item in scholix_client.iterate_links_v2(
            page_size=1, filters=ScholixFilters(sourcePid="10.1234/source")
        )
    ]

    assert len(results) == 2
    assert mock_api_client_fixture.request.call_count == 2


@pytest.mark.asyncio
async def test_iterate_scholix_links_v2_stops_on_empty_page(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "currentPage": 0,
        "totalPages": 1,
        "totalLinks": 0,
        "result": [],
    }
    mock_api_client_fixture.request.return_value = response

    results = [
        item
        async for item in scholix_client.iterate_links_v2(
            filters=ScholixFilters(sourcePid="10.1234/source")
        )
    ]

    assert results == []


@pytest.mark.asyncio
async def test_iterate_scholix_links_v2_stops_when_total_pages_is_zero(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    link = create_mock_scholix_link_data("10.1234/source", "10.1234/target")
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "currentPage": 0,
        "totalPages": 0,
        "totalLinks": 1,
        "result": [link],
    }
    mock_api_client_fixture.request.return_value = response

    results = [
        item
        async for item in scholix_client.iterate_links_v2(
            filters=ScholixFilters(sourcePid="10.1234/source")
        )
    ]

    assert len(results) == 1


@pytest.mark.asyncio
async def test_legacy_scholix_links_are_typed(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "links": [
            {
                "relationship": {
                    "name": "References",
                    "inverseRelationship": "IsReferencedBy",
                    "schema": "datacite",
                },
                "source": {
                    "identifier": [{"identifier": "10.1234/source", "schema": "doi"}],
                    "objectType": "publication",
                    "objectSubType": "Article",
                },
                "target": {
                    "identifier": [{"identifier": "10.1234/target", "schema": "doi"}],
                    "objectType": "dataset",
                    "objectSubType": "Dataset",
                },
            }
        ]
    }
    mock_api_client_fixture.request.return_value = mock_response

    links = await scholix_client.links_from_pid(
        "10.1234/source", pid_type="doi", page=2
    )

    assert links == [
        ScholixV1Link.model_validate(mock_response.json.return_value["links"][0])
    ]
    assert links[0].source.object_type == "publication"
    mock_api_client_fixture.request.assert_called_once_with(
        method="GET",
        path="linksFromPid",
        params={"pid": "10.1234/source", "pidType": "doi", "page": 2},
        base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v1"),
        data=None,
        json_data=None,
    )


@pytest.mark.asyncio
async def test_scholix_directory_and_kpi_endpoints(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    provider_response = AsyncMock(spec=httpx.Response)
    provider_response.status_code = 200
    provider_response.json.return_value = {"result": [{"name": "OpenCitations"}]}

    publisher_response = AsyncMock(spec=httpx.Response)
    publisher_response.status_code = 200
    publisher_response.json.return_value = {"result": [{"name": "Publisher"}]}

    datasource_response = AsyncMock(spec=httpx.Response)
    datasource_response.status_code = 200
    datasource_response.json.return_value = {"datasources": [{"name": "Data source"}]}

    kpi_response = AsyncMock(spec=httpx.Response)
    kpi_response.status_code = 200
    kpi_response.text = "# HELP scholix_links_total 1"

    mock_api_client_fixture.request = AsyncMock(
        side_effect=[
            provider_response,
            publisher_response,
            datasource_response,
            kpi_response,
        ]
    )

    assert await scholix_client.list_link_providers() == [{"name": "OpenCitations"}]
    assert await scholix_client.list_link_publishers(in_target=False) == [
        {"name": "Publisher"}
    ]
    assert await scholix_client.list_datasources() == [{"name": "Data source"}]
    assert await scholix_client.get_kpi() == "# HELP scholix_links_total 1"

    expected_bases = [
        OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v2"),
        OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v2"),
        OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v1"),
        OPENAIRE_SCHOLIX_API_BASE_URL.rsplit("/", 1)[0],
    ]
    assert [
        call.kwargs["base_url_override"]
        for call in mock_api_client_fixture.request.call_args_list
    ] == expected_bases


def test_scholix_custom_base_url_without_version(mock_api_client_fixture):
    client = ScholixClient(
        api_client=mock_api_client_fixture, scholix_base_url="https://example.test"
    )
    assert client._root_base_url() == "https://example.test"


@pytest.mark.asyncio
async def test_legacy_scholix_publisher_and_datasource_links(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    payload = {"links": []}
    publisher_response = AsyncMock(spec=httpx.Response)
    publisher_response.status_code = 200
    publisher_response.json.return_value = payload
    datasource_response = AsyncMock(spec=httpx.Response)
    datasource_response.status_code = 200
    datasource_response.json.return_value = payload
    mock_api_client_fixture.request = AsyncMock(
        side_effect=[publisher_response, datasource_response]
    )

    assert await scholix_client.links_from_publisher("Publisher", page=2) == []
    assert await scholix_client.links_from_datasource("Datasource", page=3) == []

    assert mock_api_client_fixture.request.call_args_list == [
        call(
            method="GET",
            path="linksFromPublisher",
            params={"publisher": "Publisher", "page": 2},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v1"),
            data=None,
            json_data=None,
        ),
        call(
            method="GET",
            path="linksFromDatasource",
            params={"datasource": "Datasource", "page": 3},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL.replace("/v3", "/v1"),
            data=None,
            json_data=None,
        ),
    ]


@pytest.mark.asyncio
async def test_iterate_scholix_links_api_error(
    scholix_client: ScholixClient, mock_api_client_fixture: AsyncMock
):
    """Test API error during Scholix link iteration."""
    target_pid_val = "10.error/target"
    page_size = 1

    link_data_page1 = create_mock_scholix_link_data("10.source/page1", target_pid_val)
    expected_link_model_page1 = ScholixRelationship.model_validate(link_data_page1)

    page1_response_dict = {
        "currentPage": 0,
        "totalPages": 2,
        "totalLinks": 2,
        "result": [link_data_page1],
    }
    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json.return_value = page1_response_dict

    error_response_mock = AsyncMock(spec=httpx.Response)
    error_response_mock.status_code = 500
    error_response_mock.request = httpx.Request("GET", f"/{SCHOLIX}")
    error_response_mock.json.return_value = {"error": "scholix server down"}

    mock_api_client_fixture.request.side_effect = [
        mock_http_response_page1,
        httpx.HTTPStatusError(
            message="Scholix Server Error '500'",
            request=error_response_mock.request,
            response=error_response_mock,
        ),
    ]

    iterated_links = []
    filters = ScholixFilters(targetPid=target_pid_val)
    with pytest.raises(BibliofabricError) as exc_info:
        async for link in scholix_client.iterate_links(
            filters=filters, page_size=page_size
        ):
            iterated_links.append(link)

    assert len(iterated_links) == 1
    assert iterated_links[0] == expected_link_model_page1
    assert f"Unexpected error searching {SCHOLIX}: Scholix Server Error '500'" in str(
        exc_info.value
    )

    expected_calls = [
        call(
            method="GET",
            path=SCHOLIX,
            params={"targetPid": target_pid_val, "size": page_size, "page": 0},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
            data=None,
            json_data=None,
        ),
        call(
            method="GET",
            path=SCHOLIX,
            params={"targetPid": target_pid_val, "size": page_size, "page": 1},
            base_url_override=OPENAIRE_SCHOLIX_API_BASE_URL,
            data=None,
            json_data=None,
        ),
    ]
    mock_api_client_fixture.request.assert_has_calls(expected_calls)
    assert mock_api_client_fixture.request.call_count == 2
