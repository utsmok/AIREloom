"""Resource client for OpenAIRE research products (V4) plus the links route."""

import logging
from collections.abc import AsyncIterator, Callable
from typing import Any

from bibliofabric.client import BaseApiClient
from bibliofabric.ids import normalize_doi
from bibliofabric.paging import Page
from bibliofabric.resources import OnError

from ..filters import LinksFilters, ResearchProductsFilters
from ..models import Relation, RelationInfo, ResearchProduct
from .base import GraphResource
from .links import LinksResource

logger = logging.getLogger(__name__)


class ResearchProductsResource(GraphResource[ResearchProduct]):
    """V4 research products endpoint: search, iterate, count, facets, group_by.

    ``get(id)`` reads the V3 by-id route because V4 has no by-id endpoints.
    Batch lookups use OR expressions over ``id`` and ``ids.doi``.
    """

    path = "v4/research-products"
    model = ResearchProduct
    filters_model = ResearchProductsFilters
    sort_fields = frozenset(
        {
            "relevance",
            "publication_date",
            "date_of_collection",
            "citation_count",
            "influence",
            "popularity",
            "impulse",
        }
    )
    batch_size = 50

    def __init__(self, client: BaseApiClient, links: LinksResource) -> None:
        super().__init__(client)
        self._links = links

    def _record_key(self, entity: ResearchProduct, field: str) -> str | None:
        if field == "ids.doi":
            return normalize_doi(entity.doi) if entity.doi else None
        return super()._record_key(entity, field)

    async def batch_get_by_doi(
        self,
        dois: list[str] | tuple[str, ...],
        *,
        batch_size: int | None = None,
        concurrency: int = 4,
    ) -> dict[str, ResearchProduct]:
        """Fetch research products for many DOIs in bounded, concurrent chunks.

        Keys are bare, lowercased DOIs; missing DOIs are absent from the
        result. The request goes out as ``filter=ids.doi:a|b|c``.
        """
        normalized = list(dict.fromkeys(normalize_doi(doi) for doi in dois))
        return await self.batch_get(
            normalized, field="ids.doi", batch_size=batch_size, concurrency=concurrency
        )

    async def search_links(
        self,
        filters: LinksFilters | None = None,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Page[Relation]:
        """Fetch one page of relations from the Graph links route."""
        return await self._links.search(filters, page=page, page_size=page_size)

    def iterate_links(
        self,
        filters: LinksFilters | None = None,
        *,
        page_size: int | None = None,
        limit: int | None = None,
        on_error: OnError = "raise",
        failures: list[tuple[dict[str, Any], Exception]] | None = None,
        on_page: Callable[[int, str | None], Any] | None = None,
    ) -> AsyncIterator[Relation]:
        """Iterate over all relations matching ``filters``, 99 per page.

        See :class:`LinksResource` for the missing-sort hazard of this
        page-based route.
        """
        return self._links.iterate(
            filters,
            page_size=page_size,
            limit=limit,
            on_error=on_error,
            failures=failures,
            on_page=on_page,
        )

    async def get_relations_info(self) -> list[RelationInfo]:
        """Return the relation types the links endpoint can produce."""
        return await self._links.get_relations_info()
