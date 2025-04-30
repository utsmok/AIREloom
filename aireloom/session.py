"""Main user-facing session class for interacting with the OpenAIRE Graph API and Scholexplorer."""

import http
from collections.abc import AsyncIterator
from typing import Any, TypeVar

import httpx
from loguru import logger

from .auth import AuthStrategy, NoAuth
from .client import AireloomClient
from .constants import (
    DEFAULT_PAGE_SIZE,
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)
from .endpoints import (
    DATA_SOURCES,
    ENDPOINT_DEFINITIONS,
    ORGANIZATIONS,
    PROJECTS,
    RESEARCH_PRODUCTS,
    SCHOLIX,
)
from .exceptions import AireloomError, ValidationError
from .log_config import configure_logging
from .models import (
    ApiResponse,
    BaseEntity,
    DataSource,
    DataSourceResponse,
    Organization,
    OrganizationResponse,
    Project,
    ProjectResponse,
    ResearchProduct,
    ResearchProductResponse,
    ScholixRelationship,
    ScholixResponse,
)

configure_logging()

GraphApiEntityType = TypeVar(
    "GraphApiEntityType", ResearchProduct, Organization, DataSource, Project
)
GraphApiResponseType = TypeVar("GraphApiResponseType", bound=ApiResponse)


class AireloomSession:
    """Provides methods to interact with the OpenAIRE Graph API and Scholexplorer API."""

    def __init__(
        self,
        auth_strategy: AuthStrategy | None = None,
        timeout: int | None = None,
        api_base_url: str | None = None,
        scholix_base_url: str | None = None,
    ):
        """Initializes the Aireloom session.

        Args:
            auth_strategy:  Authentication strategy (e.g., NoAuth(), TokenAuth(...)).
                            Defaults to NoAuth.
            timeout: Default request timeout in seconds.
            api_base_url: Base URL for the OpenAIRE Graph API.
            scholix_base_url: Base URL for the Scholexplorer API.
        """
        self._auth_strategy = auth_strategy or NoAuth()
        self._api_base_url = api_base_url or OPENAIRE_GRAPH_API_BASE_URL
        self._scholix_base_url = scholix_base_url or OPENAIRE_SCHOLIX_API_BASE_URL

        self._api_client = AireloomClient(
            auth_strategy=self._auth_strategy,
            base_url=self._api_base_url,
        )
        logger.info(f"AireloomSession initialized for API: {self._api_base_url}")
        logger.info(f"Scholexplorer configured for: {self._scholix_base_url}")

        self._model_map: dict[
            str, dict[str, type[BaseEntity | ApiResponse | ScholixResponse]]
        ] = {
            RESEARCH_PRODUCTS: {
                "entity": ResearchProduct,
                "response": ResearchProductResponse,
            },
            ORGANIZATIONS: {"entity": Organization, "response": OrganizationResponse},
            DATA_SOURCES: {"entity": DataSource, "response": DataSourceResponse},
            PROJECTS: {"entity": Project, "response": ProjectResponse},
            # Scholix has a different structure, handled separately but mapped for validation
            SCHOLIX: {"entity": ScholixRelationship, "response": ScholixResponse},
        }

    # --- Helper Methods --- #

    def _validate_filters(self, entity_path: str, filters: dict[str, Any]) -> None:
        """Validates filter keys and attempts type conversion based on endpoint definitions."""
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path definition: {entity_path}")

        valid_filters = ENDPOINT_DEFINITIONS[entity_path].get("filters", {})
        if not valid_filters and filters:
            logger.warning(
                f"Filters provided for {entity_path}, but none are defined. Ignoring filters: {filters}"
            )
            return
        if not valid_filters:
            return

        for key, value in filters.items():
            if key not in valid_filters:
                raise ValidationError(
                    f"Invalid filter key for {entity_path}: '{key}'. Valid keys: {list(valid_filters)}"
                )

            try:
                filters[key] = self._validate_and_convert_filter_value(
                    key, value, valid_filters[key].get("type", "any")
                )
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Invalid type/value for filter '{key}'. Expected {valid_filters[key].get('type', 'any')}, got {type(value).__name__}. {e}"
                ) from e

    def _validate_and_convert_filter_value(
        self, key: str, value: Any, expected_type_str: str
    ) -> Any:
        """Validates and converts a single filter value based on the expected type string."""
        current_type = type(value)

        type_map = {
            "string": str,
            "integer": int,
            "boolean": bool,
            # Add other types here if needed (e.g., "list": list)
        }

        if expected_type_str == "any" or expected_type_str not in type_map:
            return value

        target_type = type_map[expected_type_str]

        if isinstance(value, target_type):
            return value

        logger.warning(
            f"Filter '{key}' expects {expected_type_str}, got {current_type.__name__}. Attempting conversion."
        )

        # Handle boolean string conversion explicitly
        if target_type is bool and isinstance(value, str):
            lower_val = value.lower()
            if lower_val in ["true", "1", "yes"]:
                return True
            if lower_val in ["false", "0", "no"]:
                return False
            raise ValueError("String cannot be reliably converted to boolean")

        # General conversion attempt
        try:
            return target_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Conversion to {expected_type_str} failed") from e

    def _validate_sort(self, entity_path: str, sort_by: str | None) -> None:
        """Validates the sort field against endpoint definitions."""
        if not sort_by:
            return
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path: {entity_path}")

        valid_sort_fields = ENDPOINT_DEFINITIONS[entity_path]["sort_fields"]
        # Sort format can be "field", "field asc", "field desc"
        sort_field = sort_by.split()[0]
        if sort_field not in valid_sort_fields:
            raise ValidationError(
                f"Invalid sort field for {entity_path}: '{sort_field}'"
            )

    def _build_params(
        self, page: int, page_size: int, sort_by: str | None, filters: dict[str, Any]
    ) -> dict[str, Any]:
        """Builds the query parameter dictionary."""
        params = {"page": page, "pageSize": page_size}
        if sort_by:
            params["sortBy"] = sort_by
        params.update(filters)
        # Remove None values, encode others safely
        return {k: v for k, v in params.items() if v is not None}

    async def _get_single_entity(
        self, entity_path: str, entity_id: str, entity_model: type[GraphApiEntityType]
    ) -> GraphApiEntityType:
        """Generic method to fetch a single entity by ID."""
        endpoint = f"{entity_path}/{entity_id}"
        try:
            response = await self._api_client.request("GET", endpoint)
            # Parse directly into the entity model
            return entity_model.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            # Use http.HTTPStatus constant
            if e.response.status_code == http.HTTPStatus.NOT_FOUND:
                raise AireloomError(
                    f"{entity_model.__name__} with ID '{entity_id}' not found."
                ) from e
            raise
        except Exception as e:
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(
                f"Failed to fetch {entity_model.__name__} {entity_id}: {e}"
            ) from e

    async def _search_entities(
        self,
        entity_path: str,
        response_model: type[GraphApiResponseType],
        params: dict[str, Any],
    ) -> GraphApiResponseType:
        """Generic method to search for entities."""
        try:
            response = await self._api_client.request("GET", entity_path, params=params)
            return response_model.model_validate(response.json())
        except Exception as e:
            if isinstance(e, AireloomError | ValidationError):
                raise e
            raise AireloomError(f"Failed to search {entity_path}: {e}") from e

    async def _iterate_entities(
        self,
        entity_path: str,
        entity_model: type[GraphApiEntityType],
        params: dict[str, Any],
    ) -> AsyncIterator[GraphApiEntityType]:
        """Generic method to iterate through all results using cursor pagination."""
        # Use cursor pagination: start with '*', remove page/size if present
        current_params = params.copy()
        current_params.pop("page", None)
        current_params["cursor"] = "*"
        if "size" not in current_params:
            current_params["size"] = DEFAULT_PAGE_SIZE

        while True:
            try:
                response = await self._api_client.request(
                    "GET", entity_path, params=current_params
                )
                data = response.json()
                api_response = ApiResponse[entity_model].model_validate(data)

                if not api_response.results:
                    break

                for result in api_response.results:
                    yield result

                next_cursor = api_response.header.nextCursor
                if not next_cursor:
                    break

                current_params["cursor"] = next_cursor

            except Exception as e:
                if isinstance(e, AireloomError | ValidationError):
                    raise e
                logger.exception(
                    f"Failed during iteration of {entity_path}"
                )
                raise AireloomError(
                    f"Failed during iteration of {entity_path}: {e}"
                ) from e

    # --- Public Methods for Graph API --- #

    async def get_research_product(self, product_id: str) -> ResearchProduct:
        """Retrieves a single Research Product by its ID."""
        return await self._get_single_entity(
            RESEARCH_PRODUCTS, product_id, ResearchProduct
        )

    async def search_research_products(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> ResearchProductResponse:
        """Searches for Research Products.

        Args:
            page: Page number (1-indexed).
            page_size: Number of results per page.
            sort_by: Field to sort by (e.g., 'title asc', 'publicationdate desc').
            **filters: Keyword arguments for filtering (e.g., country='US', openAccess=True).

        Returns:
            A ResearchProductResponse object containing results and header info.
        """
        self._validate_filters(RESEARCH_PRODUCTS, filters)
        self._validate_sort(RESEARCH_PRODUCTS, sort_by)
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            **filters,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_entities(
            RESEARCH_PRODUCTS, ResearchProductResponse, params
        )

    async def iterate_research_products(
        self,
        page_size: int = 100,
        sort_by: str | None = None,
        **filters: Any,
    ) -> AsyncIterator[ResearchProduct]:
        """Iterates through all Research Product results matching the criteria.

        Uses cursor-based pagination for efficiency.

        Args:
            page_size: Number of results to fetch per API call during iteration.
            sort_by: Field to sort by.
            **filters: Keyword arguments for filtering.

        Yields:
            ResearchProduct objects.
        """
        self._validate_filters(RESEARCH_PRODUCTS, filters)
        self._validate_sort(RESEARCH_PRODUCTS, sort_by)
        # Build params *without* page, ensure size is present
        params = {
            "page": 1,
            "pageSize": page_size,
            "sortBy": sort_by,
            **filters,
        }
        params.pop("page", None)

        async for item in self._iterate_entities(
            RESEARCH_PRODUCTS, ResearchProduct, params
        ):
            yield item

    async def get_organization(self, org_id: str) -> Organization:
        """Retrieves a single Organization by its ID."""
        return await self._get_single_entity(ORGANIZATIONS, org_id, Organization)

    async def search_organizations(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> OrganizationResponse:
        """Searches for Organizations."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(ORGANIZATIONS, OrganizationResponse, params)

    async def iterate_organizations(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[Organization]:
        """Iterates through all Organization results."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(ORGANIZATIONS, Organization, params):
            yield item

    async def get_data_source(self, source_id: str) -> DataSource:
        """Retrieves a single Data Source by its ID."""
        return await self._get_single_entity(DATA_SOURCES, source_id, DataSource)

    async def search_data_sources(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> DataSourceResponse:
        """Searches for Data Sources."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(DATA_SOURCES, DataSourceResponse, params)

    async def iterate_data_sources(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[DataSource]:
        """Iterates through all Data Source results."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(DATA_SOURCES, DataSource, params):
            yield item

    async def get_project(self, project_id: str) -> Project:
        """Retrieves a single Project by its ID."""
        return await self._get_single_entity(PROJECTS, project_id, Project)

    async def search_projects(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> ProjectResponse:
        """Searches for Projects."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(PROJECTS, ProjectResponse, params)

    async def iterate_projects(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[Project]:
        """Iterates through all Project results."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(PROJECTS, Project, params):
            yield item

    # --- Scholexplorer Methods --- #

    async def search_scholix_links(
        self,
        page: int = 0,
        page_size: int = DEFAULT_PAGE_SIZE,
        **filters: Any,
    ) -> ScholixResponse:
        """Searches for Scholexplorer relationship links.

        Args:
            page: The page number to retrieve (0-indexed).
            page_size: The number of results per page.
            **filters: Keyword arguments corresponding to valid Scholexplorer filters
                       (e.g., sourcePid, targetPid, relationshipType, linkProviderName).

        Returns:
            A ScholixResponse object containing the results for the requested page.

        Raises:
            ValidationError: If invalid filter keys are provided.
            AireloomError: For API communication errors or unexpected issues.
        """
        # Use a mutable copy for validation side-effects
        mutable_filters = filters.copy()
        self._validate_filters(SCHOLIX, mutable_filters)

        # Scholexplorer uses 0-based page, size is 'rows'
        params = {
            "page": page,
            "rows": page_size,
            **mutable_filters,
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await self._api_client.request(
                method="GET",
                path=SCHOLIX,
                params=params,
                base_url_override=self._scholix_base_url,
            )
            return ScholixResponse.model_validate(response.json())
        except Exception as e:
            # Use | for isinstance check
            if isinstance(e, AireloomError | ValidationError):
                raise e
            logger.exception(f"Failed to search {SCHOLIX}")  # Log exception details
            raise AireloomError(f"Failed to search {SCHOLIX}: {e}") from e

    async def iterate_scholix_links(
        self,
        page_size: int = DEFAULT_PAGE_SIZE,
        **filters: Any,
    ) -> AsyncIterator[ScholixRelationship]:
        """Iterates through all Scholexplorer relationship links matching the filters.

        Handles pagination automatically based on 'totalPages'.

        Args:
            page_size: The number of results per page during iteration.
            **filters: Keyword arguments corresponding to valid Scholexplorer filters.

        Yields:
            ScholixRelationship objects matching the query.

        Raises:
            ValidationError: If invalid filter keys are provided.
            AireloomError: For API communication errors or unexpected issues.
        """
        # Validate filters first (validation modifies the dict if types need conversion)
        mutable_filters = filters.copy()
        self._validate_filters(SCHOLIX, mutable_filters)

        current_page = 0
        total_pages = 1 # Assume at least one page initially

        while current_page < total_pages:
            logger.debug(
                f"Iterating Scholix page {current_page + 1}/{total_pages if total_pages > 1 else '?'}"
            )
            try:
                # Call search_scholix_links, passing page_size explicitly,
                # and validated filters via **mutable_filters.
                response_data = await self.search_scholix_links(
                    page=current_page,
                    page_size=page_size, # Pass page_size directly
                    **mutable_filters, # Pass validated filters
                )

                if not response_data.result:
                    logger.debug("No results found on this page, stopping iteration.")
                    break

                for link in response_data.result:
                    yield link

                # Update total_pages from the first response, then check if done
                if current_page == 0:
                    total_pages = response_data.totalPages
                    logger.debug(f"Total pages reported by Scholix: {total_pages}")

                # Check if we've processed the last page
                if current_page >= total_pages - 1:
                    logger.debug("Last page processed, stopping iteration.")
                    break

                current_page += 1

            except Exception as e:
                # Use | for isinstance check
                if isinstance(e, AireloomError | ValidationError):
                    raise e
                logger.exception(
                    f"Failed during iteration of {SCHOLIX} on page {current_page}"
                )  # Log exception
                raise AireloomError(
                    f"Failed during iteration of {SCHOLIX} on page {current_page}: {e}"
                ) from e
        logger.debug("Scholix iteration finished.")

    async def close(self) -> None:
        """Closes the underlying HTTP client session."""
        await self._api_client.aclose()

    async def __aenter__(self) -> "AireloomSession":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
