# aireloom/resources/research_products_client.py
"""Client for interacting with the OpenAIRE Research Products API endpoint.

This module provides the `ResearchProductsClient`, which facilitates access to
OpenAIRE's research product data (e.g., publications, datasets, software).
It leverages generic mixins from `bibliofabric.resources` for common API
operations like retrieving individual entities, searching, and iterating
through result sets.
"""

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from bibliofabric.log_config import logger
from bibliofabric.resources import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)

from ._batch import BatchMixin
from ._standard import GraphV3FilterSerializationMixin

if TYPE_CHECKING:
    from ..client import AireloomClient
from ..constants import MAX_LINK_PAGE_SIZE
from ..endpoints import LINKS, RESEARCH_PRODUCTS, LinksFilters
from ..models import LinksResponse, Relation, ResearchProduct, ResearchProductResponse


class ResearchProductsClient(
    GraphV3FilterSerializationMixin,
    BatchMixin,
    GettableMixin,
    SearchableMixin,
    CursorIterableMixin,
    BaseResourceClient,
):
    """Client for the OpenAIRE Research Products API endpoint.

    This client provides standardized methods (`get`, `search`, `iterate`) for
    accessing research product data, by inheriting from `bibliofabric` mixins.
    It also provides `search_links`, `iterate_links`, and `get_relations_info`
    for the V3 ``/research-products/links`` sub-endpoint.

    Attributes:
        _entity_path (str): The API path for research products.
        _entity_model (type[ResearchProduct]): Pydantic model for a single research product.
        _search_response_model (type[ResearchProductResponse]): Pydantic model for the
                                                                search response envelope.
    """

    _entity_path: str = RESEARCH_PRODUCTS
    _entity_model: type[ResearchProduct] = ResearchProduct
    _search_response_model: type[ResearchProductResponse] = ResearchProductResponse
    _batch_fields: dict[str, str] = {
        "doi": "pid",
        "openaire_id": "id",
        "original_id": "originalId",
    }

    def __init__(self, api_client: "AireloomClient"):
        """Initializes the ResearchProductsClient.

        Args:
            api_client: An instance of AireloomClient.
        """
        super().__init__(api_client)
        logger.debug(
            f"ResearchProductsClient initialized for path: {self._entity_path}"
        )

    # Mixin-provided methods: get, search, iterate

    # ------------------------------------------------------------------
    # Links sub-endpoint (V3, 0-indexed page-based pagination)
    # ------------------------------------------------------------------

    async def search_links(
        self,
        *,
        filters: LinksFilters | None = None,
        page: int = 0,
        page_size: int = 20,
    ) -> LinksResponse:
        """Search for relation links between research products.

        Uses the V3 ``/research-products/links`` endpoint (NOT the Scholix API).

        Args:
            filters: Optional :class:`LinksFilters` with filter criteria.
            page: 0-indexed page number.
            page_size: Number of results per page (max 99; values >=100 are silently
                truncated to 10 by V3).

        Returns:
            A :class:`LinksResponse` containing the matching relations.
        """
        if page_size > MAX_LINK_PAGE_SIZE:
            logger.warning(
                "page_size=%d exceeds the V3 links maximum of %d "
                "(values >=100 are silently truncated to 10); clamping.",
                page_size,
                MAX_LINK_PAGE_SIZE,
            )
            page_size = MAX_LINK_PAGE_SIZE
        params: dict[str, Any] = {"page": page, "pageSize": page_size}
        if filters is not None:
            params.update(self._serialize_filters(filters))

        response = await self._api_client.request(
            method="GET",
            path=LINKS,
            params=params,
        )
        return LinksResponse.model_validate(response.json())

    async def iterate_links(
        self,
        *,
        filters: LinksFilters | None = None,
        page_size: int = MAX_LINK_PAGE_SIZE,
    ) -> AsyncIterator[Relation]:
        """Iterate through all relation links matching *filters*.

        Automatically handles page-based pagination using ``totalPages``
        from the response header.

        Args:
            filters: Optional :class:`LinksFilters` with filter criteria.
            page_size: Number of results per page (max 99; see :meth:`search_links`).

        Yields:
            :class:`Relation` objects.
        """
        current_page = 0
        total_pages = 1

        while current_page < total_pages:
            response = await self.search_links(
                filters=filters, page=current_page, page_size=page_size
            )

            if not response.results:
                break

            for rel in response.results:
                yield rel

            if current_page == 0 and response.header is not None:
                total_pages = response.header.totalPages or 1
                if total_pages == 0:
                    break

            if current_page >= total_pages:
                break

            current_page += 1

    async def get_relations_info(self) -> list[dict[str, Any]]:
        """Retrieve available relation types from the links endpoint.

        Uses the V3 ``/research-products/links/relations-info`` endpoint.

        Returns:
            A list of dicts describing relation types (name, inverse, description).
        """
        response = await self._api_client.request(
            method="GET",
            path=f"{LINKS}/relations-info",
            params={},
        )
        data = response.json()
        if isinstance(data, list):
            return data
        return [data]
