# tests/resources/test_persons_client.py
from unittest.mock import AsyncMock

import httpx
import pytest
from bibliofabric.exceptions import BibliofabricError
from pydantic import ValidationError

from aireloom.client import AireloomClient
from aireloom.constants import DEFAULT_PAGE_SIZE
from aireloom.endpoints import PERSONS, PersonsFilters
from aireloom.models import Header, Person
from aireloom.resources import PersonsClient
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
def persons_client(mock_api_client_fixture: AsyncMock) -> PersonsClient:
    """Fixture to create a PersonsClient with a mocked API client."""
    return PersonsClient(api_client=mock_api_client_fixture)


@pytest.mark.asyncio
async def test_get_person(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test getting a single person."""
    person_id = "person_test_id_123"
    expected_person_data_dict = {
        "id": person_id,
        "givenName": "Marie",
        "familyName": "Curie",
    }
    expected_person = Person.model_validate(expected_person_data_dict)

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    # Use search response format with results array
    mock_http_response.json.return_value = {
        "results": [expected_person_data_dict],
        "header": {"numFound": 1, "pageSize": 1},
    }
    mock_api_client_fixture.request.return_value = mock_http_response

    person = await persons_client.get(person_id)

    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        PERSONS,
        params={"id": person_id, "pageSize": 1},
        base_url_override=None,
    )
    assert person == expected_person


@pytest.mark.asyncio
async def test_get_person_not_found(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test getting a non-existent person."""
    person_id = "non_existent_person_id"

    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.request = httpx.Request("GET", f"/{PERSONS}/{person_id}")
    mock_response.json.return_value = {"error": "not found"}

    mock_api_client_fixture.request.side_effect = httpx.HTTPStatusError(
        message=f"Client error '404 Not Found' for url /{PERSONS}/{person_id}",
        request=mock_response.request,
        response=mock_response,
    )

    with pytest.raises(BibliofabricError) as exc_info:
        await persons_client.get(person_id)

    assert f"Unexpected error fetching entity {person_id}" in str(exc_info.value)
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        PERSONS,
        params={"id": person_id, "pageSize": 1},
        base_url_override=None,
    )


@pytest.mark.asyncio
async def test_search_persons_no_filters(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test searching persons with no filters."""
    expected_results_data = [
        {"id": "person1", "givenName": "Ada", "familyName": "Lovelace"}
    ]
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

    response = await persons_client.search(page=1, page_size=DEFAULT_PAGE_SIZE)

    expected_params = {"page": 1, "pageSize": DEFAULT_PAGE_SIZE}
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        PERSONS,
        params=expected_params,
        base_url_override=None,
    )
    assert response.results == [
        Person.model_validate(item) for item in expected_results_data
    ]
    assert response.header == Header.model_validate(expected_header_data)


@pytest.mark.asyncio
async def test_search_persons_with_filters_and_sort(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test searching persons with filters and sorting."""
    filters_model = PersonsFilters(givenName="Marie", lastName="Curie")
    sort_by = "relevance asc"
    page = 1
    page_size = 5

    expected_results_data = [
        {
            "id": "person_mc",
            "givenName": "Marie",
            "familyName": "Curie",
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

    response = await persons_client.search(
        filters=filters_model, sort_by=sort_by, page=page, page_size=page_size
    )

    expected_params = {
        "givenName": "Marie",
        "lastName": "Curie",
        "sortBy": sort_by,
        "page": page,
        "pageSize": page_size,
    }

    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        PERSONS,
        params=expected_params,
        base_url_override=None,
    )
    assert response.results == [
        Person.model_validate(item) for item in expected_results_data
    ]
    assert response.header == Header.model_validate(expected_header_data)


@pytest.mark.asyncio
async def test_search_sort_field_passed_through(
    persons_client: PersonsClient,
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
    await persons_client.search(sort_by="customField asc")
    call_args = mock_api_client_fixture.request.call_args
    assert call_args.kwargs.get("params", {}).get("sortBy") == "customField asc"


@pytest.mark.asyncio
async def test_iterate_persons(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating through persons using cursor pagination."""
    filters_model = PersonsFilters(lastName="Einstein")
    page_size = 1
    sort_by = "relevance asc"

    # Page 1
    page1_results_data = [
        {"id": "person_ae", "givenName": "Albert", "familyName": "Einstein"}
    ]
    page1_header_data = {
        "numFound": 2,
        "pageSize": page_size,
        "nextCursor": "cursor_person_page2",
    }
    mock_response_page1_json = {
        "results": page1_results_data,
        "header": page1_header_data,
    }

    # Page 2
    page2_results_data = [
        {"id": "person_ea2", "givenName": "Elsa", "familyName": "Einstein"}
    ]
    page2_header_data = {"numFound": 2, "pageSize": page_size, "nextCursor": None}
    mock_response_page2_json = {
        "results": page2_results_data,
        "header": page2_header_data,
    }

    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json = lambda: mock_response_page1_json

    mock_http_response_page2 = AsyncMock(spec=httpx.Response)
    mock_http_response_page2.status_code = 200
    mock_http_response_page2.json = lambda: mock_response_page2_json

    mock_api_client_fixture.request = AsyncMock(
        side_effect=[
            mock_http_response_page1,
            mock_http_response_page2,
        ]
    )

    iterated_persons = []
    async for person in persons_client.iterate(
        filters=filters_model, page_size=page_size, sort_by=sort_by
    ):
        iterated_persons.append(person)

    assert len(iterated_persons) == 2
    assert iterated_persons[0] == Person.model_validate(page1_results_data[0])
    assert iterated_persons[1] == Person.model_validate(page2_results_data[0])

    # Verify the mock was called the expected number of times
    assert mock_api_client_fixture.request.call_count == 2


@pytest.mark.asyncio
async def test_iterate_persons_no_results(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test iterating persons when the search yields no results."""
    filters_model = PersonsFilters(givenName="Nonexistent")
    page_size = 3

    expected_header_data = {"numFound": 0, "pageSize": page_size, "nextCursor": None}
    mock_response_json = {"results": [], "header": expected_header_data}

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = mock_response_json
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    count = 0
    async for _ in persons_client.iterate(
        filters=filters_model, page_size=page_size
    ):
        count += 1

    assert count == 0
    expected_params = {
        "givenName": "Nonexistent",
        "pageSize": page_size,
        "cursor": "*",
    }
    mock_api_client_fixture.request.assert_called_once_with(
        "GET",
        PERSONS,
        params=expected_params,
        base_url_override=None,
    )


@pytest.mark.asyncio
async def test_iterate_persons_api_error(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test API error during person iteration."""
    filters_model = PersonsFilters(lastName="Newton")
    page_size = 1

    # Page 1 - success
    page1_results_data = [
        {"id": "person_in", "givenName": "Isaac", "familyName": "Newton"}
    ]
    page1_header_data = {
        "numFound": 2,
        "pageSize": page_size,
        "nextCursor": "cursor_newton_page2",
    }
    mock_response_page1_json = {
        "results": page1_results_data,
        "header": page1_header_data,
    }

    mock_http_response_page1 = AsyncMock(spec=httpx.Response)
    mock_http_response_page1.status_code = 200
    mock_http_response_page1.json = lambda: mock_response_page1_json

    # Page 2 - error
    error_response_mock = AsyncMock(spec=httpx.Response)
    error_response_mock.status_code = 500
    error_response_mock.request = httpx.Request("GET", f"/{PERSONS}")
    error_response_mock.json.return_value = {"error": "server broke"}

    mock_api_client_fixture.request = AsyncMock(
        side_effect=[
            mock_http_response_page1,
            httpx.HTTPStatusError(
                message="Server error '500'",
                request=error_response_mock.request,
                response=error_response_mock,
            ),
        ]
    )

    iterated_persons = []
    with pytest.raises(BibliofabricError) as exc_info:
        async for person in persons_client.iterate(
            filters=filters_model, page_size=page_size
        ):
            iterated_persons.append(person)

    assert len(iterated_persons) == 1  # Only first page
    assert iterated_persons[0] == Person.model_validate(page1_results_data[0])
    assert "Unexpected error during iteration" in str(exc_info.value)

    # Verify the mock was called the expected number of times
    assert mock_api_client_fixture.request.call_count == 2


@pytest.mark.asyncio
async def test_persons_filters_conversion(
    persons_client: PersonsClient, mock_api_client_fixture: AsyncMock
):
    """Test that PersonsFilters fields are correctly converted to query params."""
    filters_model = PersonsFilters(
        search="quantum",
        id="person123",
        originalId="orcid:0000-0001-2345-6789",
        givenName="Richard",
        lastName="Feynman",
    )
    page_size = 10

    mock_http_response = AsyncMock(spec=httpx.Response)
    mock_http_response.status_code = 200
    mock_http_response.json.return_value = {
        "results": [],
        "header": {"numFound": 0, "pageSize": page_size},
    }
    mock_api_client_fixture.request = AsyncMock(return_value=mock_http_response)

    await persons_client.search(filters=filters_model, page_size=page_size)

    call_params = mock_api_client_fixture.request.call_args.kwargs.get("params", {})
    assert call_params.get("search") == "quantum"
    assert call_params.get("id") == "person123"
    assert call_params.get("originalId") == "orcid:0000-0001-2345-6789"
    assert call_params.get("givenName") == "Richard"
    assert call_params.get("lastName") == "Feynman"


def test_persons_filters_forbid_extra():
    """Test that PersonsFilters rejects unknown fields."""
    with pytest.raises(ValidationError):
        PersonsFilters(unknownField="value")



def test_persons_client_routes_to_v1(persons_client):
    """PersonsClient should NOT have a v2 base URL override — persons is v1-only."""
    assert persons_client._base_url_override is None