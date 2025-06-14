# aireloom/resources/research_products_client.py
"""Client for interacting with OpenAIRE Research Products."""

import http
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

import httpx
from loguru import logger

if TYPE_CHECKING:
    from ..client import AireloomClient
from ..constants import DEFAULT_PAGE_SIZE  # RESEARCH_PRODUCTS is now in endpoints
from ..endpoints import (  # Import model
    ENDPOINT_DEFINITIONS,
    RESEARCH_PRODUCTS,
    ResearchProductsFilters,
)
from ..exceptions import AireloomError, ValidationError
from ..models import (
    ApiResponse,
    ResearchProduct,
    ResearchProductResponse,
)
from .base_client import BaseResourceClient


class ResearchProductsClient(BaseResourceClient):
    """Provides methods to interact with OpenAIRE Research Products."""

    _entity_path: str = RESEARCH_PRODUCTS
    _entity_model: type[ResearchProduct] = ResearchProduct
    _response_model: type[ResearchProductResponse] = ResearchProductResponse

    def __init__(self, api_client: "AireloomClient"):
        """Initializes the ResearchProductsClient.

        Args:
            api_client: An instance of AireloomClient.
        """
        super().__init__(api_client)
        if self._entity_path not in ENDPOINT_DEFINITIONS:
            # This should ideally not happen if constants are aligned with definitions
            raise ValueError(
                f"Missing endpoint definition for entity path: {self._entity_path}"
            )
        self._endpoint_def = ENDPOINT_DEFINITIONS[self._entity_path]
        self._valid_sort_fields = self._endpoint_def.get(
            "sort", {}
        ).keys()  # Get sort fields
        logger.debug(
            f"ResearchProductsClient initialized for path: {self._entity_path}"
        )

    # _validate_filters and _validate_and_convert_filter_value are removed as Pydantic handles this.

    def _validate_sort(self, sort_by: str | None) -> None:
        """Validates the sort field against endpoint definitions."""
        if not sort_by:
            return

        # valid_sort_fields is now an instance variable _valid_sort_fields
        if not self._valid_sort_fields:  # Check if any sort fields are defined
            logger.warning(
                f"Sort field '{sort_by}' provided for {self._entity_path}, "
                "but no sort fields are defined. Ignoring sort."
            )
            return

        sort_field_name = sort_by.split()[0]
        if sort_field_name not in self._valid_sort_fields:
            raise ValidationError(
                f"Invalid sort field for {self._entity_path}: '{sort_field_name}'. "
                f"Valid fields: {list(self._valid_sort_fields)}"
            )

    def _build_params(
        self,
        page: int | None,  # Allow None for iteration
        page_size: int,
        sort_by: str | None,
        filters: dict[str, Any] | None,
        *,
        is_iteration: bool = False,
    ) -> dict[str, Any]:
        """Builds the query parameter dictionary."""
        params: dict[str, Any] = {"pageSize": page_size}
        if is_iteration:
            params["cursor"] = "*"  # Iteration uses cursor
        elif page is not None:
            params["page"] = page

        if sort_by:
            params["sortBy"] = sort_by
        if filters:
            params.update(filters)
        return {k: v for k, v in params.items() if v is not None}

    async def _fetch_single_entity_impl(self, entity_id: str) -> ResearchProduct:
        """Generic method to fetch a single entity by ID."""
        endpoint = f"{self._entity_path}/{entity_id}"
        try:
            response = await self._api_client.request(
                "GET", endpoint, params=None, data=None, json_data=None
            )
            return self._entity_model.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == http.HTTPStatus.NOT_FOUND:
                raise AireloomError(
                    f"{self._entity_model.__name__} with ID '{entity_id}' not found "
                    f"at {self._entity_path}."
                ) from e
            logger.error(
                f"HTTPStatusError for {self._entity_model.__name__} ID '{entity_id}': {e.response.status_code}"
            )
            raise AireloomError(
                f"API error fetching {self._entity_model.__name__} {entity_id}: "
                f"Status {e.response.status_code}"
            ) from e
        except Exception as e:
            if isinstance(e, AireloomError):
                raise
            logger.exception(
                f"Failed to fetch {self._entity_model.__name__} {entity_id} from {self._entity_path}"
            )
            raise AireloomError(
                f"Unexpected error fetching {self._entity_model.__name__} {entity_id}: {e}"
            ) from e

    async def _search_entities_impl(
        self, params: dict[str, Any]
    ) -> ResearchProductResponse:
        """Generic method to search for entities."""
        try:
            response = await self._api_client.request(
                "GET", self._entity_path, params=params, data=None, json_data=None
            )
            return self._response_model.model_validate(response.json())
        except Exception as e:
            if isinstance(e, AireloomError | ValidationError):
                raise
            logger.exception(
                f"Failed to search {self._entity_path} with params {params}"
            )
            raise AireloomError(
                f"Unexpected error searching {self._entity_path}: {e}"
            ) from e

    async def _iterate_entities_impl(
        self, params: dict[str, Any]
    ) -> AsyncIterator[ResearchProduct]:
        """Generic method to iterate through all results using cursor pagination."""
        current_params = (
            params.copy()
        )  # Ensure pageSize is in params from _build_params

        while True:
            try:
                logger.debug(
                    f"Iterating {self._entity_path} with params: {current_params}"
                )
                response = await self._api_client.request(
                    "GET",
                    self._entity_path,
                    params=current_params,
                    data=None,
                    json_data=None,
                )
                data = response.json()
                # Use the generic ApiResponse for parsing iteration results
                api_response = ApiResponse[self._entity_model].model_validate(data)

                if not api_response.results:
                    logger.debug(
                        f"No more results for {self._entity_path}, stopping iteration."
                    )
                    break

                for result in api_response.results:
                    yield result

                next_cursor = api_response.header.nextCursor
                if not next_cursor:
                    logger.debug(
                        f"No nextCursor for {self._entity_path}, stopping iteration."
                    )
                    break

                current_params["cursor"] = next_cursor
                # Remove page if it accidentally got in, cursor handles pagination
                current_params.pop("page", None)

            except Exception as e:
                if isinstance(e, AireloomError | ValidationError):
                    raise
                logger.exception(
                    f"Failed during iteration of {self._entity_path} with params {current_params}"
                )
                raise AireloomError(
                    f"Unexpected error during iteration of {self._entity_path}: {e}"
                ) from e

    async def get(self, product_id: str) -> ResearchProduct:
        """Retrieves a single Research Product by its ID.

        Args:
            product_id: The ID of the research product.

        Returns:
            A ResearchProduct object.

        Raises:
            AireloomError: If the API request fails or the product is not found.
        """
        logger.info(f"Fetching research product with ID: {product_id}")
        return await self._fetch_single_entity_impl(product_id)

    async def search(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        filters: ResearchProductsFilters | None = None,  # Changed to Pydantic model
    ) -> ResearchProductResponse:
        """Searches for Research Products.

        Args:
            page: Page number (1-indexed).
            page_size: Number of results per page.
            sort_by: Field to sort by (e.g., 'title asc', 'publicationdate desc').
            filters: An instance of ResearchProductsFilters with filter criteria.

        Returns:
            A ResearchProductResponse object containing results and header info.

        Raises:
            ValidationError: If sort fields are invalid (filter validation by Pydantic).
            AireloomError: If the API request fails.
        """
        filter_dict = (
            filters.model_dump(exclude_none=True, by_alias=True) if filters else {}
        )
        logger.info(
            f"Searching research products: page={page}, size={page_size}, sort='{sort_by}', "
            f"filters={filter_dict}"
        )
        # self._validate_filters(mutable_filters) # Removed, Pydantic handles this
        self._validate_sort(sort_by)
        params = self._build_params(
            page=page, page_size=page_size, sort_by=sort_by, filters=filter_dict
        )
        return await self._search_entities_impl(params)

    async def iterate(
        self,
        page_size: int = 100,  # Default from original AireloomSession
        sort_by: str | None = None,
        filters: ResearchProductsFilters | None = None,  # Changed to Pydantic model
    ) -> AsyncIterator[ResearchProduct]:
        """Iterates through all Research Product results matching the criteria.

        Uses cursor-based pagination for efficiency.

        Args:
            page_size: Number of results to fetch per API call during iteration.
            sort_by: Field to sort by.
            filters: An instance of ResearchProductsFilters with filter criteria.

        Yields:
            ResearchProduct objects.

        Raises:
            ValidationError: If sort fields are invalid (filter validation by Pydantic).
            AireloomError: If the API request fails during iteration.
        """
        filter_dict = (
            filters.model_dump(exclude_none=True, by_alias=True) if filters else {}
        )
        logger.info(
            f"Iterating research products: pageSize={page_size}, sort='{sort_by}', "
            f"filters={filter_dict}"
        )
        # self._validate_filters(mutable_filters) # Removed, Pydantic handles this
        self._validate_sort(sort_by)
        # For iteration, page is not used directly; cursor is primary.
        # _build_params handles 'cursor': '*' when is_iteration=True
        params = self._build_params(
            page=None,  # Page is not used for cursor iteration start
            page_size=page_size,
            sort_by=sort_by,
            filters=filter_dict,
            is_iteration=True,
        )

        async for item in self._iterate_entities_impl(params):
            yield item
