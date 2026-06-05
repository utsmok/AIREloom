from typing import Self

from bibliofabric.auth import (
    AuthStrategy,
    ClientCredentialsAuth,
    NoAuth,
    StaticTokenAuth,
)
from bibliofabric.client import BaseApiClient
from bibliofabric.log_config import logger

from .config import ApiSettings, get_settings
from .constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)
from .resources import (
    DataSourcesClient,
    OrganizationsClient,
    PersonsClient,
    ProjectsClient,
    ResearchProductsClient,
    ScholixClient,
)
from .unwrapper import OpenAireUnwrapper


class AireloomClient(BaseApiClient):
    """Asynchronous client for interacting with the OpenAIRE Graph and Scholix APIs.

    This client provides a high-level interface to various OpenAIRE API endpoints,
    handling authentication, request retries, caching, and rate limiting.
    It builds upon the generic `bibliofabric.client.BaseApiClient` and is configured
    specifically for OpenAIRE services.

    Resource clients for different OpenAIRE entities (e.g., research products,
    projects, organizations) are available as properties of this client.

    Authentication is handled automatically based on provided settings or can be
    customized by passing an `auth_strategy`. If no credentials or strategy are
    provided, requests will be made without authentication.

    Typical usage:
    ```python
    async with AireloomClient() as client:
        product = await client.research_products.get(
            "some_product_id"
        )
        async for project in client.projects.iterate(
            filters=ProjectFilters(...)
        ):
            print(project.title)
    ```

    Attributes:
        research_products (ResearchProductsClient): Client for research product endpoints.
        organizations (OrganizationsClient): Client for organization endpoints.
        projects (ProjectsClient): Client for project endpoints.
        data_sources (DataSourcesClient): Client for data source endpoints.
        scholix (ScholixClient): Client for Scholix (scholarly link exchange) endpoints.
        _settings (ApiSettings): The resolved API settings for this client instance.
        _scholix_base_url (str): The base URL for the Scholix API.
    """

    def __init__(
        self,
        settings: ApiSettings | None = None,
        auth_strategy: AuthStrategy | None = None,
        *,
        api_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = OPENAIRE_GRAPH_API_BASE_URL,
        scholix_base_url: str = OPENAIRE_SCHOLIX_API_BASE_URL,
    ):
        """Initializes the AireloomClient.

        This constructor sets up the client with necessary configurations,
        determines the authentication strategy, and initializes resource-specific
        sub-clients.

        Authentication Strategy Resolution:
        - If `auth_strategy` is explicitly provided, it is used.
        - Otherwise, credentials (api_token, client_id, client_secret) passed
          directly to this constructor take precedence over those in `settings`.
        - If credentials are not passed directly, they are sourced from `settings`
          (which are loaded from environment variables or .env files).
        - The order of preference for automatic strategy selection is:
            1. Client Credentials (if client_id & client_secret are available)
            2. Static Token (if api_token is available)
            3. No Authentication (if no credentials are found)

        Args:
            settings: An optional `ApiSettings` instance. If `None`, global settings
                are loaded via `aireloom.config.get_settings()`. These settings
                can be a source for authentication credentials and other client behaviors.
            auth_strategy: An optional explicit `AuthStrategy` instance. If provided,
                it overrides automatic authentication resolution.
            api_token: An optional static API token. If provided, it takes precedence
                over `settings.openaire_api_token` for StaticTokenAuth.
            client_id: An optional client ID for ClientCredentialsAuth. Takes
                precedence over `settings.openaire_client_id`.
            client_secret: An optional client secret for ClientCredentialsAuth. Takes
                precedence over `settings.openaire_client_secret`.
            base_url: The base URL for the OpenAIRE Graph API. Defaults to the
                production OpenAIRE Graph API URL.
            scholix_base_url: The base URL for the OpenAIRE Scholix API. Defaults
                to the production OpenAIRE Scholix API URL.
        """
        self._settings: ApiSettings = settings or get_settings()
        self._scholix_base_url: str = scholix_base_url.rstrip("/")

        _cid = self._settings.openaire_client_id
        _cid_display = (
            f"***{_cid[-4:]}" if _cid and len(_cid) > 4 else ("***" if _cid else "None")  # noqa: PLR2004
        )
        logger.debug(
            f"AireloomClient.__init__ settings: id={id(self._settings)}, "
            f"client_id={_cid_display}, "
            f"token={'***' if self._settings.openaire_api_token else 'None'}, "
            f"timeout={self._settings.request_timeout}"
        )

        self._auth_strategy = self._resolve_auth_strategy(
            auth_strategy, api_token, client_id, client_secret, _cid_display
        )

        # Create the OpenAIRE response unwrapper
        unwrapper = OpenAireUnwrapper()

        # Initialize the base client with all the generic functionality
        super().__init__(
            base_url=base_url,
            settings=self._settings,
            auth_strategy=self._auth_strategy,
            response_unwrapper=unwrapper,
        )

        # Initialize OpenAIRE-specific resource clients
        self._research_products = ResearchProductsClient(api_client=self)
        self._organizations = OrganizationsClient(api_client=self)
        self._projects = ProjectsClient(api_client=self)
        self._persons = PersonsClient(api_client=self)
        self._data_sources = DataSourcesClient(api_client=self)
        self._scholix = ScholixClient(
            api_client=self, scholix_base_url=self._scholix_base_url
        )

        logger.debug("AireloomClient initialized successfully.")

    def _resolve_auth_strategy(
        self,
        auth_strategy: AuthStrategy | None,
        api_token: str | None,
        client_id: str | None,
        client_secret: str | None,
        _cid_display: str,
    ) -> AuthStrategy:
        """Resolve the authentication strategy from explicit strategy or credentials.

        Args:
            auth_strategy: An explicit AuthStrategy, if provided.
            api_token: Optional static API token override.
            client_id: Optional client ID override.
            client_secret: Optional client secret override.
            _cid_display: Masked display string for logging.

        Returns:
            The resolved AuthStrategy instance.
        """
        if auth_strategy:
            logger.debug(
                f"Using explicitly provided authentication strategy: {type(auth_strategy).__name__}"
            )
            return auth_strategy

        logger.debug("Determining auth type based on provided parameters or settings.")
        _client_id = client_id or self._settings.openaire_client_id
        _client_secret = client_secret or self._settings.openaire_client_secret
        _api_token = api_token or self._settings.openaire_api_token
        _token_url = self._settings.openaire_token_url

        logger.debug(
            f"Auth decision: client_id_param={'***' if client_id else None}, "
            f"settings_client_id={_cid_display}, "
            f"api_token_param={'***' if api_token else None}, "
            f"settings_api_token={'***' if self._settings.openaire_api_token else None}"
        )

        if _client_id and _client_secret:
            logger.debug("Using Client Credentials authentication.")
            if client_id and client_secret:
                logger.debug("Client ID and secret were directly passed as parameters.")
            else:
                logger.debug(
                    "Client ID and secret were loaded from settings or environment variables."
                )
            return ClientCredentialsAuth(
                client_id=_client_id,
                client_secret=_client_secret,
                token_url=_token_url,
            )

        if _api_token:
            logger.debug("Using Static Token authentication.")
            return StaticTokenAuth(token=_api_token)

        logger.debug("No authentication credentials found, using NoAuth.")
        return NoAuth()

    @property
    def research_products(self) -> ResearchProductsClient:
        """Provides access to the ResearchProductsClient for OpenAIRE research product APIs."""
        return self._research_products

    @property
    def organizations(self) -> OrganizationsClient:
        """Provides access to the OrganizationsClient for OpenAIRE organization APIs."""
        return self._organizations

    @property
    def projects(self) -> ProjectsClient:
        """Provides access to the ProjectsClient for OpenAIRE project APIs."""
        return self._projects

    @property
    def persons(self) -> PersonsClient:
        """Provides access to the PersonsClient for OpenAIRE person APIs."""
        return self._persons

    @property
    def data_sources(self) -> DataSourcesClient:
        """Provides access to the DataSourcesClient for OpenAIRE data source APIs."""
        return self._data_sources

    @property
    def scholix(self) -> ScholixClient:
        """Provides access to the ScholixClient for OpenAIRE Scholix (scholarly link) APIs."""
        return self._scholix

    async def __aenter__(self) -> Self:
        """Async context manager entry."""
        logger.debug(
            f"AireloomClient.__aenter__() called. Client ID: {id(self)}. "
            f"HTTP client closed: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        logger.debug(
            f"AireloomClient.__aexit__() called. Client ID: {id(self)}. "
            f"HTTP client closed before aclose: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
        await self.aclose()
        logger.debug(
            f"AireloomClient.__aexit__() finished. Client ID: {id(self)}. "
            f"HTTP client closed after aclose: {self._http_client.is_closed if self._http_client else 'N/A'}"
        )
