# tests/resources/test_links.py
"""Tests for the Research Products links functionality.

Covers:
- LinksFilters validation (valid and invalid params)
- search_links method with mocked HTTP responses
- iterate_links pagination
- get_relations_info
- Relation/Node/RelType model validation
"""

from unittest.mock import AsyncMock

import httpx
import pytest
from pydantic import ValidationError

from aireloom.client import AireloomClient
from aireloom.constants import OPENAIRE_GRAPH_API_BASE_URL
from aireloom.endpoints import LinksFilters
from aireloom.models import (
    EntityRef,
    Identifier,
    LinksResponse,
    Node,
    Relation,
    RelType,
)
from aireloom.resources import ResearchProductsClient
from aireloom.unwrapper import OpenAireUnwrapper

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
            "page": 1,
            "pageSize": 10,
            "totalPages": 0,
        },
        "results": [],
    }
    mock_client.request.return_value = mock_http_response
    return mock_client


@pytest.fixture
def research_products_client(
    mock_api_client_fixture: AsyncMock,
) -> ResearchProductsClient:
    """Fixture to create a ResearchProductsClient with a mocked API client."""
    return ResearchProductsClient(api_client=mock_api_client_fixture)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_relation_dict(
    source_title: str = "Test Paper",
    source_type: str = "publication",
    source_doi: str = "10.1234/test",
    target_title: str = "Test Dataset",
    target_type: str = "dataset",
    target_doi: str = "10.5678/data",
    rel_name: str = "IsSupplementTo",
) -> dict:
    """Build a single relation dict matching the live API structure."""
    return {
        "source": {
            "title": source_title,
            "type": source_type,
            "instanceType": "Article",
            "publicationDate": "2024-01-01",
            "identifiers": [
                {
                    "id": source_doi,
                    "idScheme": "doi",
                    "idUrl": f"https://doi.org/{source_doi}",
                }
            ],
            "authors": [{"name": "Smith J", "identifiers": []}],
            "collectedFrom": [{"name": "Crossref", "identifiers": []}],
        },
        "target": {
            "title": target_title,
            "type": target_type,
            "identifiers": [
                {
                    "id": target_doi,
                    "idScheme": "doi",
                    "idUrl": f"https://doi.org/{target_doi}",
                }
            ],
        },
        "relType": {
            "name": rel_name,
            "typeSchema": "datacite",
        },
        "provenance": ["OpenAIRE"],
    }


def _mock_links_response(
    relations: list[dict] | None = None,
    num_found: int = 0,
    page: int = 1,
    page_size: int = 10,
    total_pages: int = 0,
    total_links: int = 0,
) -> dict:
    """Build a full links API response dict."""
    if relations is None:
        relations = []
    return {
        "header": {
            "numFound": num_found,
            "page": page,
            "pageSize": page_size,
            "totalPages": total_pages,
            "totalLinks": total_links,
        },
        "results": relations,
    }


# ===========================================================================
# 1. LinksFilters validation
# ===========================================================================


class TestLinksFilters:
    """Tests for the LinksFilters Pydantic model."""

    def test_valid_empty_filters(self):
        f = LinksFilters()
        assert f.sourcePid is None
        assert f.targetPid is None

    def test_valid_with_source_pid(self):
        f = LinksFilters(sourcePid="10.1234/test")
        assert f.sourcePid == "10.1234/test"

    def test_valid_with_all_fields(self):
        f = LinksFilters(
            sourcePid="10.1234/a",
            targetPid="10.5678/b",
            sourcePublisher="Crossref",
            targetPublisher="DataCite",
            sourceType="publication",
            targetType="dataset",
            relation="IsSupplementTo",
            fromDate="2020-01-01",
            toDate="2024-12-31",
        )
        assert f.sourcePid == "10.1234/a"
        assert f.toDate == "2024-12-31"

    def test_invalid_extra_field_forbidden(self):
        with pytest.raises(ValidationError) as exc_info:
            LinksFilters(unknownField="value")
        assert "Extra inputs are not permitted" in str(exc_info.value)

    def test_model_dump_excludes_none(self):
        f = LinksFilters(sourcePid="10.1234/test")
        dumped = f.model_dump(exclude_none=True)
        assert dumped == {"sourcePid": "10.1234/test"}

    def test_valid_with_date_fields(self):
        f = LinksFilters(fromDate="2024", toDate="2024-12-31")
        assert f.fromDate == "2024"
        assert f.toDate == "2024-12-31"


# ===========================================================================
# 2. search_links
# ===========================================================================


class TestSearchLinks:
    """Tests for ResearchProductsClient.search_links."""

    @pytest.mark.asyncio
    async def test_search_links_basic(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        relation = _mock_relation_dict()
        response_data = _mock_links_response(
            relations=[relation],
            num_found=1,
            page=1,
            page_size=10,
            total_pages=1,
            total_links=1,
        )

        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = response_data
        mock_api_client_fixture.request.return_value = mock_http

        filters = LinksFilters(sourcePid="10.1234/test")
        result = await research_products_client.search_links(filters=filters)

        assert result.header.page == 1
        assert result.header.totalPages == 1
        assert result.header.totalLinks == 1
        assert len(result.results) == 1

        rel = result.results[0]
        assert isinstance(rel, Relation)
        assert rel.source.title == "Test Paper"
        assert rel.target.title == "Test Dataset"
        assert rel.relType.name == "IsSupplementTo"

    @pytest.mark.asyncio
    async def test_search_links_passes_filters_as_params(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = _mock_links_response()
        mock_api_client_fixture.request.return_value = mock_http

        filters = LinksFilters(sourcePid="10.1234/test", targetType="dataset")
        await research_products_client.search_links(
            filters=filters, page=2, page_size=5
        )

        call_args = mock_api_client_fixture.request.call_args
        params = call_args.kwargs.get("params", {})
        assert params.get("sourcePid") == "10.1234/test"
        assert params.get("targetType") == "dataset"
        assert params.get("page") == 2
        assert params.get("pageSize") == 5

    @pytest.mark.asyncio
    async def test_search_links_no_filters(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = _mock_links_response()
        mock_api_client_fixture.request.return_value = mock_http

        result = await research_products_client.search_links()
        assert result.header.totalPages == 0
        assert result.results == []

    @pytest.mark.asyncio
    async def test_search_links_uses_v1_base_url(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = _mock_links_response()
        mock_api_client_fixture.request.return_value = mock_http

        await research_products_client.search_links()

        call_args = mock_api_client_fixture.request.call_args
        assert call_args.kwargs.get("base_url_override") == OPENAIRE_GRAPH_API_BASE_URL

    @pytest.mark.asyncio
    async def test_search_links_response_model_validation(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        relation = _mock_relation_dict()
        response_data = _mock_links_response(
            relations=[relation], num_found=1, total_pages=1
        )

        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = response_data
        mock_api_client_fixture.request.return_value = mock_http

        result = await research_products_client.search_links()
        assert isinstance(result, LinksResponse)
        assert isinstance(result.results[0], Relation)


# ===========================================================================
# 3. iterate_links pagination
# ===========================================================================


class TestIterateLinks:
    """Tests for ResearchProductsClient.iterate_links."""

    @pytest.mark.asyncio
    async def test_iterate_links_single_page(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        relation = _mock_relation_dict()
        response_data = _mock_links_response(
            relations=[relation], num_found=1, page=1, total_pages=1
        )

        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = response_data
        mock_api_client_fixture.request.return_value = mock_http

        results = [
            rel async for rel in research_products_client.iterate_links()
        ]
        assert len(results) == 1
        assert isinstance(results[0], Relation)
        assert results[0].source.title == "Test Paper"

    @pytest.mark.asyncio
    async def test_iterate_links_multi_page(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        rel1 = _mock_relation_dict(source_doi="10.111/a", target_doi="10.222/b")
        rel2 = _mock_relation_dict(
            source_doi="10.333/c", target_doi="10.444/d", rel_name="References"
        )

        page1_data = _mock_links_response(
            relations=[rel1], num_found=2, page=1, total_pages=2
        )
        page2_data = _mock_links_response(
            relations=[rel2], num_found=2, page=2, total_pages=2
        )

        mock_http_p1 = AsyncMock(spec=httpx.Response)
        mock_http_p1.status_code = 200
        mock_http_p1.json.return_value = page1_data

        mock_http_p2 = AsyncMock(spec=httpx.Response)
        mock_http_p2.status_code = 200
        mock_http_p2.json.return_value = page2_data

        mock_api_client_fixture.request.side_effect = [mock_http_p1, mock_http_p2]

        results = [
            rel
            async for rel in research_products_client.iterate_links(
                filters=LinksFilters(sourcePid="10.1234/test")
            )
        ]

        assert len(results) == 2
        assert results[0].source.identifiers[0].id == "10.111/a"
        assert results[1].relType.name == "References"
        assert mock_api_client_fixture.request.call_count == 2

    @pytest.mark.asyncio
    async def test_iterate_links_no_results(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        response_data = _mock_links_response(total_pages=0)

        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = response_data
        mock_api_client_fixture.request.return_value = mock_http

        results = [
            rel
            async for rel in research_products_client.iterate_links(
                filters=LinksFilters(sourcePid="10.0000/none")
            )
        ]
        assert len(results) == 0


# ===========================================================================
# 4. get_relations_info
# ===========================================================================


class TestGetRelationsInfo:
    """Tests for ResearchProductsClient.get_relations_info."""

    @pytest.mark.asyncio
    async def test_get_relations_info(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        expected_info = [
            {
                "relation": "Cites",
                "inverse": "IsCitedBy",
                "description": "This resource cites another resource.",
            },
            {
                "relation": "References",
                "inverse": "IsReferencedBy",
                "description": "This resource references another resource.",
            },
        ]
        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = expected_info
        mock_api_client_fixture.request.return_value = mock_http

        result = await research_products_client.get_relations_info()

        assert result == expected_info
        call_args = mock_api_client_fixture.request.call_args
        assert "relations-info" in call_args.kwargs.get("path", "")

    @pytest.mark.asyncio
    async def test_get_relations_info_empty(
        self,
        research_products_client: ResearchProductsClient,
        mock_api_client_fixture: AsyncMock,
    ):
        mock_http = AsyncMock(spec=httpx.Response)
        mock_http.status_code = 200
        mock_http.json.return_value = []
        mock_api_client_fixture.request.return_value = mock_http

        result = await research_products_client.get_relations_info()
        assert result == []


# ===========================================================================
# 5. Relation/Node/RelType model validation
# ===========================================================================


class TestRelationModels:
    """Tests for the Relation, Node, RelType, and related Pydantic models."""

    def test_relation_full_validation(self):
        data = _mock_relation_dict()
        rel = Relation.model_validate(data)

        assert rel.source.title == "Test Paper"
        assert rel.source.type == "publication"
        assert rel.source.instanceType == "Article"
        assert rel.source.publicationDate == "2024-01-01"
        assert len(rel.source.identifiers) == 1
        assert rel.source.identifiers[0].id == "10.1234/test"
        assert rel.source.identifiers[0].idScheme == "doi"

        assert rel.target.title == "Test Dataset"
        assert rel.target.type == "dataset"

        assert rel.relType.name == "IsSupplementTo"
        assert rel.relType.typeSchema == "datacite"

    def test_node_minimal(self):
        node = Node(title="Minimal", type="publication")
        assert node.title == "Minimal"
        assert node.type == "publication"
        assert node.identifiers is None

    def test_rel_type_validation(self):
        rt = RelType(name="References", typeSchema="datacite")
        assert rt.name == "References"
        assert rt.type is None
        assert rt.typeSchema == "datacite"

    def test_identifier_model(self):
        ident = Identifier(id="10.1234/test", idScheme="doi")
        assert ident.id == "10.1234/test"
        assert ident.idScheme == "doi"
        assert ident.idUrl is None

        ident_full = Identifier(
            id="10.1234/test",
            idScheme="doi",
            idUrl="https://doi.org/10.1234/test",
        )
        assert ident_full.idUrl == "https://doi.org/10.1234/test"

    def test_entity_ref_model(self):
        ref = EntityRef(name="Smith J", identifiers=[])
        assert ref.name == "Smith J"

    def test_relation_with_provenance(self):
        """Relation allows extra fields like provenance from the live API."""
        data = _mock_relation_dict()
        data["provenance"] = ["Crossref", "OpenAIRE"]
        rel = Relation.model_validate(data)
        assert rel.source.title == "Test Paper"

    def test_relation_missing_optional_fields(self):
        data = {
            "source": {"title": "Source", "type": "publication"},
            "target": {"title": "Target", "type": "dataset"},
            "relType": {"name": "References", "typeSchema": "datacite"},
        }
        rel = Relation.model_validate(data)
        assert rel.source.title == "Source"
        assert rel.source.identifiers is None
        assert rel.relType.name == "References"

    def test_links_response_validation(self):
        data = _mock_links_response(
            relations=[_mock_relation_dict()],
            total_links=5,
            total_pages=3,
        )
        resp = LinksResponse.model_validate(data)
        assert resp.header.totalLinks == 5
        assert resp.header.totalPages == 3
        assert len(resp.results) == 1
