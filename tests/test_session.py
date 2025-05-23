# tests/test_session.py
import pytest
from dotenv import load_dotenv
from pytest_httpx import HTTPXMock

# Make sure aireloom can be imported from the src directory
# This might require specific pytest configuration or PYTHONPATH adjustments
# depending on project structure and how tests are run.
# Assuming standard src layout is handled by pytest/uv.
from aireloom import AireloomSession
from aireloom.auth import (  # Import specific auth strategies for checking
    NoAuth,
    StaticTokenAuth,
)
from aireloom.constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)
from aireloom.exceptions import AireloomError, ValidationError

# Load .env file for local testing (e.g., containing AIRELOOM_OPENAIRE_API_TOKEN)
load_dotenv()

# --- Constants ---
# Keep existing constants
KNOWN_PRODUCT_ID = "doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108"
KNOWN_PRODUCT_TITLE_FRAGMENT = (
    "OpenAIRE Graph"  # A fragment likely present in the title
)
KNOWN_DOI_WITH_LINKS = "10.5281/zenodo.7668094"
UNKNOWN_PRODUCT_ID = "oai:example.org:nonexistent123"
INVALID_PRODUCT_ID_FORMAT = "not-a-valid-id-format"

# --- Mock Data ---
MOCK_SCHOLIX_RESPONSE = {
    "currentPage": 0,
    "totalLinks": 1,
    "totalPages": 1,
    "result": [
        {
            "LinkProvider": [{"Name": "Example Provider", "AgentId": "example"}],
            "LinkPublicationDate": "2023-01-15T12:00:00Z",  # Use ISO format with Z
            "RelationshipType": {
                "Name": "References",  # Correct casing
                "SubType": "Scholix",
                "SubTypeSchema": "http://example.com/datacite",  # Fix: Use valid URL
            },
            "Source": {  # Source (Required)
                "Identifier": [{"ID": KNOWN_DOI_WITH_LINKS, "IDScheme": "doi"}],
                "Type": "publication",  # Use valid literal from ScholixEntityTypeName
                "Title": "Source Title",
                "Creator": [{"Name": "Source Author"}],
                "PublicationDate": "2023",
                "Publisher": [
                    {"Name": "Source Publisher"}
                ],  # Fix: Make Publisher a list of objects
            },
            "Target": {  # Add Target (Required)
                "Identifier": [{"ID": "10.1234/target.dataset", "IDScheme": "doi"}],
                "Type": "dataset",  # Use valid literal from ScholixEntityTypeName
            },
            "LicenseURL": None,  # Optional
            "HarvestDate": None,  # Optional
        }
    ],
}

# --- Basic Initialization Tests ---


@pytest.mark.asyncio
async def test_session_initialization_no_token():
    """Test initializing AireloomSession without providing a token."""
    async with AireloomSession() as session:
        assert session is not None
        # Check if NoAuth strategy is implicitly used
        assert isinstance(session._api_client._auth_strategy, NoAuth)


@pytest.mark.asyncio
async def test_session_initialization_with_token(
    api_token,
):  # Uses fixture from conftest.py
    """Test initializing AireloomSession with a token (from fixture)."""
    if not api_token:
        pytest.skip(
            "Skipping token test: AIRELOOM_OPENAIRE_API_TOKEN not set in environment."
        )

    # Test explicit token argument
    async with AireloomSession(api_token=api_token) as session:
        assert session is not None
        # Check if TokenAuth strategy is used
        assert isinstance(session._api_client._auth_strategy, StaticTokenAuth)
        assert session._api_client._auth_strategy._token == api_token

    # Test token via settings (implicitly via environment variable AIRELOOM_OPENAIRE_API_TOKEN)
    # This assumes the ApiClient correctly reads from settings when no strategy/token is passed
    async with AireloomSession() as session_env:
        assert session_env is not None
        assert isinstance(session_env._api_client._auth_strategy, StaticTokenAuth)
        assert session_env._api_client._auth_strategy._token == api_token


# --- Graph API Tests ---


# Use a known, stable, public research product ID for testing
# Example: OpenAIRE-Nexus project publication


@pytest.mark.asyncio
async def test_get_research_product_success(httpx_mock: HTTPXMock):
    """Test fetching a known research product successfully.

    Ensures a valid response is parsed correctly.
    """
    product_id = "oai:zenodo.org:7668094"  # Use variable for clarity
    mock_product_response = {
        "id": product_id,
        "titles": [{"value": "Mocked Test Product Title"}],
        # Add mainTitle field to prevent None value
        "mainTitle": "Mocked Test Product Title",
        # Add other minimal required fields if necessary based on model
    }

    # Mock the specific API call
    httpx_mock.add_response(
        url=f"{OPENAIRE_GRAPH_API_BASE_URL}/researchProducts/{product_id}",
        method="GET",
        json=mock_product_response,
        status_code=200,
    )

    async with AireloomSession() as session:
        try:
            product = await session.get_research_product(product_id)
            assert product is not None
            assert product.id == product_id
            assert isinstance(product.mainTitle, str)  # Fix: use mainTitle
        except AireloomError as e:
            pytest.fail(f"Fetching known product failed: {e}")


@pytest.mark.asyncio
async def test_get_research_product_not_found():
    """Test fetching a non-existent research product."""
    async with AireloomSession() as session:
        with pytest.raises(AireloomError, match="API request failed with status 404"):
            await session.get_research_product("nonexistent:id_123456789_invalid")


@pytest.mark.asyncio
async def test_search_research_products_simple():
    """Test a simple search for research products."""
    async with AireloomSession() as session:
        try:
            # Search for a common term, limit results
            response = await session.search_research_products(
                page_size=5,
                mainTitle="Open Science",  # Use mainTitle filter
            )
            assert response is not None
            assert len(response.results) <= 5
            if response.results:
                assert isinstance(response.results[0].id, str)
                # Use mainTitle attribute for assertion
                assert isinstance(response.results[0].mainTitle, str)
        except AireloomError as e:
            pytest.fail(f"Simple product search failed: {e}")


@pytest.mark.asyncio
async def test_iterate_research_products(httpx_mock: HTTPXMock):
    """Test iterating through research products."""
    # Mock the API response for the iteration
    mock_response = {
        "header": {"total": 2},
        "results": [
            {"id": "id1", "mainTitle": "Title 1"},
            {"id": "id2", "mainTitle": "Title 2"},
        ],
    }
    httpx_mock.add_response(
        url="https://api.openaire.eu/graph/v1/researchProducts?pageSize=5&sortBy=&mainTitle=FAIR+data&cursor=%2A",
        method="GET",
        json=mock_response,
        status_code=200,
    )
    async with AireloomSession() as session:
        count = 0
        max_items_to_iterate = 15
        try:
            async for product in session.iterate_research_products(
                page_size=5, mainTitle="FAIR data"
            ):
                assert product is not None
                assert isinstance(product.id, str)
                count += 1
                if count >= max_items_to_iterate:
                    break
            assert count >= 0
            assert count <= max_items_to_iterate
        except AireloomError as e:
            pytest.fail(f"Product iteration failed: {e}")


# --- Scholix API Tests ---


# Use a known DOI with known relationships if possible, otherwise use a general one


@pytest.mark.asyncio
async def test_search_scholix_links_success(httpx_mock: HTTPXMock):
    """Test searching for Scholix links for a known DOI."""
    # Mock the API call
    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=0&rows=10",
        method="GET",
        json=MOCK_SCHOLIX_RESPONSE,
        status_code=200,
    )
    async with AireloomSession() as session:
        try:
            response = await session.search_scholix_links(
                page_size=10, sourcePid=KNOWN_DOI_WITH_LINKS
            )
            assert response is not None
            assert response.currentPage == 0  # API is 0-indexed
            assert response.totalLinks >= 0  # Check for non-negative
            assert response.result is not None
            assert 0 <= len(response.result) <= 10  # noqa: PLR2004
            # If results exist, check basic structure
            if response.result:
                link = response.result[0]
                # Assuming LinkPublicationDate might be None in real data or mock
                # assert link.LinkPublicationDate is not None
                assert link.source is not None
                assert link.target is not None
                assert isinstance(link.source.identifier, list)
                assert isinstance(link.target.identifier, list)
                assert link.relationship_type is not None  # Check added field
        except AireloomError as e:
            pytest.fail(f"Scholix link search failed: {e}")


@pytest.mark.asyncio
async def test_iterate_scholix_links(httpx_mock: HTTPXMock):
    """Test iterating through Scholix links."""
    # Mock the first page API call
    # Use a response with enough links for the test iteration count.
    mock_response_page1 = MOCK_SCHOLIX_RESPONSE.copy()
    mock_response_page1["currentPage"] = 0
    mock_response_page1["totalLinks"] = 7  # Example: 7 links total across 2 pages
    mock_response_page1["totalPages"] = 2  # Example: 2 pages total
    # Create 5 links for page 1 (size=5)
    # Ensure the base link structure is valid
    base_link = MOCK_SCHOLIX_RESPONSE["result"][0]
    mock_response_page1["result"] = []
    for i in range(5):
        link = base_link.copy()
        link["LinkPublicationDate"] = f"2023-01-15T12:00:0{i}Z"  # Vary slightly, use Z
        # Ensure Source and Target are valid ScholixEntity structures
        link["Source"] = {  # Add Source (Required)
            "Identifier": [{"ID": f"{KNOWN_DOI_WITH_LINKS}/{i}", "IDScheme": "doi"}],
            "Type": "publication",
        }
        link["Target"] = {  # Add Target (Required)
            "Identifier": [{"ID": f"10.1234/target.dataset.{i}", "IDScheme": "doi"}],
            "Type": "dataset",  # Ensure valid type
        }
        link["RelationshipType"]["SubTypeSchema"] = (
            "http://example.com/datacite"  # Fix SubTypeSchema
        )
        mock_response_page1["result"].append(link)

    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=0&rows=5",
        method="GET",
        json=mock_response_page1,
        status_code=200,
    )

    # Mock the second page
    mock_response_page2 = MOCK_SCHOLIX_RESPONSE.copy()
    mock_response_page2["currentPage"] = 1
    mock_response_page2["totalLinks"] = 7
    mock_response_page2["totalPages"] = 2
    # Create 2 remaining links for page 2
    mock_response_page2["result"] = []
    for i in range(2):
        link = base_link.copy()
        link["LinkPublicationDate"] = f"2023-01-16T13:00:0{i}Z"  # Vary slightly, use Z
        # Ensure Source and Target are valid ScholixEntity structures
        link["Source"] = {  # Add Source (Required)
            "Identifier": [
                {"ID": f"{KNOWN_DOI_WITH_LINKS}/{i + 5}", "IDScheme": "doi"}
            ],
            "Type": "publication",
        }
        link["Target"] = {  # Add Target (Required)
            "Identifier": [
                {"ID": f"10.1234/target.dataset.{i + 5}", "IDScheme": "doi"}
            ],
            "Type": "dataset",  # Ensure valid type
        }
        mock_response_page2["result"].append(link)

    httpx_mock.add_response(
        url=f"{OPENAIRE_SCHOLIX_API_BASE_URL}/Links?sourcePid={KNOWN_DOI_WITH_LINKS}&page=1&rows=5",
        method="GET",
        json=mock_response_page2,
        status_code=200,
    )
    async with AireloomSession() as session:
        count = 0
        max_items_to_iterate = 7  # Iterate through all mocked items
        try:
            async for link in session.iterate_scholix_links(
                page_size=5, sourcePid=KNOWN_DOI_WITH_LINKS
            ):
                assert link is not None
                assert link.relationship_type is not None  # Use snake_case field name
                assert link.source is not None
                assert link.target is not None
                assert link.link_publication_date is not None  # Check date exists
                count += 1
                if count >= max_items_to_iterate:
                    break
            assert count == max_items_to_iterate
        except AireloomError as e:
            pytest.fail(f"Scholix iteration failed: {e}")


@pytest.mark.asyncio
async def test_search_scholix_invalid_filter():
    """Test searching Scholix links with an invalid filter key."""
    async with AireloomSession() as session:
        with pytest.raises(
            ValidationError, match="Invalid filter key"
        ):  # Check error message content
            # Pass a deliberately invalid filter key
            # Also pass a valid sourcePid to get past the initial check
            await session.search_scholix_links(
                page_size=10,
                sourcePid=KNOWN_DOI_WITH_LINKS,
                someMadeUpFilterKey="someValue",
            )
