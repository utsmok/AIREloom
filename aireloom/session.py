"""Main user-facing session class for interacting with the OpenAIRE Graph API."""

import httpx
from typing import Optional, Dict, Any, Type, TypeVar, AsyncIterator, Mapping
from urllib.parse import urlencode

from .auth import Authenticator
from .client import ApiClient
from .constants import GRAPH_API_BASE_URL, DEFAULT_TIMEOUT, DEFAULT_PAGE_SIZE
from .endpoints import (
    RESEARCH_PRODUCTS,
    ORGANIZATIONS,
    DATA_SOURCES,
    PROJECTS,
    ENDPOINT_DEFINITIONS,
)
from .exceptions import ValidationError, AireloomError
from .models import (
    ResearchProduct,
    Organization,
    DataSource,
    Project,
    ApiResponse,
    ResearchProductResponse,
    OrganizationResponse,
    DataSourceResponse,
    ProjectResponse,
)
from .validators import default_validation # Add more specific validators later


# Type variable for entity models
EntityType = TypeVar("EntityType", ResearchProduct, Organization, DataSource, Project)
# Type variable for response models
ResponseType = TypeVar("ResponseType", bound=ApiResponse)


class AireloomSession:
    """Provides methods to interact with the OpenAIRE Graph API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 1,
        client: Optional[httpx.AsyncClient] = None, # Allow passing external client
    ):
        """Initializes the Aireloom session.

        Args:
            client_id: Client ID for Client Credentials authentication.
            client_secret: Client Secret for Client Credentials authentication.
            refresh_token: Refresh Token for Refresh Token authentication.
            timeout: Default request timeout.
            max_retries: Max retries on rate limit errors.
            client: Optional external httpx.AsyncClient.
        """
        # Initialize Authenticator first
        try:
            self._authenticator = Authenticator(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
                timeout=timeout,
            )
        except ValueError as e:
            # Provide a more user-friendly error if no auth details provided
            raise AireloomError(
                "Authentication required: Please provide either client_id/client_secret or a refresh_token."
            ) from e

        # Initialize API Client
        self._api_client = ApiClient(
            authenticator=self._authenticator,
            base_url=GRAPH_API_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            client=client,
        )

        # Mapping from entity path to Pydantic models
        self._model_map: Dict[str, Dict[str, Type]] = {
            RESEARCH_PRODUCTS: {"entity": ResearchProduct, "response": ResearchProductResponse},
            ORGANIZATIONS: {"entity": Organization, "response": OrganizationResponse},
            DATA_SOURCES: {"entity": DataSource, "response": DataSourceResponse},
            PROJECTS: {"entity": Project, "response": ProjectResponse},
        }

    def _validate_filters(self, entity_path: str, filters: Dict[str, Any]) -> None:
        """Validates filter keys and potentially values against endpoint definitions."""
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path: {entity_path}")

        valid_filters = ENDPOINT_DEFINITIONS[entity_path]["filters"]
        for key, value in filters.items():
            if key not in valid_filters:
                raise ValidationError(f"Invalid filter key for {entity_path}: '{key}'")
            # TODO: Add value validation using specific functions from validators.py
            # try:
            #     validator = getattr(validators, f"validate_{key}", default_validation)
            #     validator(value)
            # except (ValueError, TypeError) as e:
            #     raise ValidationError(f"Invalid value for filter '{key}': {e}") from e

    def _validate_sort(self, entity_path: str, sort_by: Optional[str]) -> None:
        """Validates the sort field."""
        if not sort_by:
            return
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path: {entity_path}")

        valid_sort_fields = ENDPOINT_DEFINITIONS[entity_path]["sort_fields"]
        # Sort format can be "field", "field asc", "field desc"
        sort_field = sort_by.split()[0]
        if sort_field not in valid_sort_fields:
             raise ValidationError(f"Invalid sort field for {entity_path}: '{sort_field}'")

    def _build_params(self, page: int, page_size: int, sort_by: Optional[str], filters: Dict[str, Any]) -> Dict[str, Any]:
        """Builds the query parameter dictionary."""
        params = {"page": page, "size": page_size}
        if sort_by:
            params["sortBy"] = sort_by
        params.update(filters)
        # Remove None values, encode others safely
        return {k: v for k, v in params.items() if v is not None}

    async def _get_single_entity(
        self, entity_path: str, entity_id: str, entity_model: Type[EntityType]
    ) -> EntityType:
        """Generic method to fetch a single entity by ID."""
        endpoint = f"{entity_path}/{entity_id}"
        try:
            response = await self._api_client.get(endpoint)
            # Parse directly into the entity model
            return entity_model.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise AireloomError(f"{entity_model.__name__} with ID '{entity_id}' not found.") from e
            raise # Re-raise other ApiErrors
        except Exception as e:
            if isinstance(e, AireloomError):
                 raise e
            raise AireloomError(f"Failed to fetch {entity_model.__name__} {entity_id}: {e}") from e

    async def _search_entities(
        self, entity_path: str, response_model: Type[ResponseType], params: Dict[str, Any]
    ) -> ResponseType:
        """Generic method to search for entities."""
        try:
            response = await self._api_client.get(entity_path, params=params)
            return response_model.model_validate(response.json())
        except Exception as e:
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(f"Failed to search {entity_path}: {e}") from e

    async def _iterate_entities(
        self, entity_path: str, entity_model: Type[EntityType], params: Dict[str, Any]
    ) -> AsyncIterator[EntityType]:
        """Generic method to iterate through all results using cursor pagination."""
        # Use cursor pagination: start with '*', remove page/size if present
        current_params = params.copy()
        current_params.pop("page", None)
        current_params["cursor"] = "*"
        if "size" not in current_params:
             current_params["size"] = DEFAULT_PAGE_SIZE # Ensure size is set

        while True:
            try:
                response = await self._api_client.get(entity_path, params=current_params)
                data = response.json()
                api_response = ApiResponse[entity_model].model_validate(data) # Use generic directly for parsing

                if not api_response.results:
                    break

                for result in api_response.results:
                    yield result

                next_cursor = api_response.header.next_cursor
                if not next_cursor:
                    break # No more pages

                current_params["cursor"] = next_cursor

            except Exception as e:
                if isinstance(e, AireloomError):
                    raise e
                raise AireloomError(f"Failed during iteration of {entity_path}: {e}") from e

    # --- Public Methods --- #

    async def get_research_product(self, product_id: str) -> ResearchProduct:
        """Retrieves a single Research Product by its ID."""
        return await self._get_single_entity(
            RESEARCH_PRODUCTS, product_id, ResearchProduct
        )

    async def search_research_products(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: Optional[str] = None,
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
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(
            RESEARCH_PRODUCTS, ResearchProductResponse, params
        )

    async def iterate_research_products(
        self,
        page_size: int = 100, # Larger default for iteration
        sort_by: Optional[str] = None,
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
        params = self._build_params(page=1, page_size=page_size, sort_by=sort_by, filters=filters)
        params.pop("page", None)

        async for item in self._iterate_entities(RESEARCH_PRODUCTS, ResearchProduct, params):
            yield item

    # --- Add similar get/search/iterate methods for Organization, DataSource, Project --- #

    async def get_organization(self, org_id: str) -> Organization:
        """Retrieves a single Organization by its ID."""
        return await self._get_single_entity(ORGANIZATIONS, org_id, Organization)

    async def search_organizations(
        self, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE, sort_by: Optional[str] = None, **filters: Any
    ) -> OrganizationResponse:
        """Searches for Organizations."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(ORGANIZATIONS, OrganizationResponse, params)

    async def iterate_organizations(
        self, page_size: int = 100, sort_by: Optional[str] = None, **filters: Any
    ) -> AsyncIterator[Organization]:
        """Iterates through all Organization results."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(page=1, page_size=page_size, sort_by=sort_by, filters=filters)
        params.pop("page", None)
        async for item in self._iterate_entities(ORGANIZATIONS, Organization, params):
            yield item

    async def get_data_source(self, ds_id: str) -> DataSource:
        """Retrieves a single Data Source by its ID."""
        return await self._get_single_entity(DATA_SOURCES, ds_id, DataSource)

    async def search_data_sources(
        self, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE, sort_by: Optional[str] = None, **filters: Any
    ) -> DataSourceResponse:
        """Searches for Data Sources."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(DATA_SOURCES, DataSourceResponse, params)

    async def iterate_data_sources(
        self, page_size: int = 100, sort_by: Optional[str] = None, **filters: Any
    ) -> AsyncIterator[DataSource]:
        """Iterates through all Data Source results."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(page=1, page_size=page_size, sort_by=sort_by, filters=filters)
        params.pop("page", None)
        async for item in self._iterate_entities(DATA_SOURCES, DataSource, params):
            yield item

    async def get_project(self, project_id: str) -> Project:
        """Retrieves a single Project by its ID."""
        return await self._get_single_entity(PROJECTS, project_id, Project)

    async def search_projects(
        self, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE, sort_by: Optional[str] = None, **filters: Any
    ) -> ProjectResponse:
        """Searches for Projects."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(PROJECTS, ProjectResponse, params)

    async def iterate_projects(
        self, page_size: int = 100, sort_by: Optional[str] = None, **filters: Any
    ) -> AsyncIterator[Project]:
        """Iterates through all Project results."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(page=1, page_size=page_size, sort_by=sort_by, filters=filters)
        params.pop("page", None)
        async for item in self._iterate_entities(PROJECTS, Project, params):
            yield item

    # --- Context Management --- #

    async def close(self) -> None:
        """Closes the underlying HTTP client."""
        await self._api_client.close()

    async def __aenter__(self) -> "AireloomSession":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()