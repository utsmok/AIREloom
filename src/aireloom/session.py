"""Main user-facing session class for interacting with the OpenAIRE Graph API and Scholexplorer."""

from functools import partial

from bibliofabric.auth import AuthStrategy
from bibliofabric.log_config import configure_logging, logger

from . import queries
from .client import AireloomClient
from .config import ApiSettings, get_settings  # Added ApiSettings
from .constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)

_DELEGATED_CLIENTS = frozenset(
    {
        "research_products",
        "organizations",
        "projects",
        "persons",
        "data_sources",
        "scholix",
    }
)

configure_logging()

# RESOURCE_CLIENTS_MAP is no longer needed as AireloomClient manages its own instances.


class _QueryAccessor:
    """Binds an AireloomSession to convenience query functions."""

    def __init__(self, queries_module, session):
        self._module = queries_module
        self._session = session

    def __getattr__(self, name):
        attr = getattr(self._module, name)
        if callable(attr):
            return partial(attr, self._session)
        return attr


class AireloomSession:
    """High-level session manager for interacting with OpenAIRE APIs.

    This class acts as the primary entry point for users of the `aireloom` library.
    It provides convenient access to various OpenAIRE resource clients (e.g., for
    research products, projects) through an underlying `AireloomClient` instance.

    The session handles the lifecycle of the `AireloomClient`, including its
    creation with appropriate settings (like timeouts and authentication) and
    its proper closure when the session is no longer needed. It supports
    asynchronous context management (`async with`).

    Example:
    ```python
    async with AireloomSession(timeout=60) as session:
        product = await session.research_products.get("some_id")
        # ... further API calls
    ```

    Attributes:
        research_products (ResearchProductsClient): Client for research product APIs.
        organizations (OrganizationsClient): Client for organization APIs.
        projects (ProjectsClient): Client for project APIs.
        data_sources (DataSourcesClient): Client for data source APIs.
        scholix (ScholixClient): Client for Scholix (scholarly link) APIs.
        _api_client (AireloomClient): The underlying client instance.
    """

    def __init__(
        self,
        auth_strategy: AuthStrategy | None = None,
        timeout: int | None = None,
        api_base_url: str | None = None,
        scholix_base_url: str | None = None,
    ):
        """Initializes the Aireloom session and its underlying `AireloomClient`.

        The session allows for overriding certain configurations like request timeout
        and API base URLs. Authentication strategy can also be provided directly.
        If not provided, the `AireloomClient` will attempt to determine it based
        on its own settings (loaded from environment or .env files).

        Args:
            auth_strategy: An optional `AuthStrategy` instance to be used for
                all requests made through this session. If `None`, the
                `AireloomClient` will determine authentication based on its settings.
            timeout: An optional integer to override the default request timeout
                (in seconds) for all HTTP requests made during this session.
                If `None`, the timeout from global or client-specific settings is used.
            api_base_url: An optional string to override the default base URL for the
                OpenAIRE Graph API.
            scholix_base_url: An optional string to override the default base URL for
                the OpenAIRE Scholix API.
        """
        _api_base_url = api_base_url or OPENAIRE_GRAPH_API_BASE_URL
        _scholix_base_url = scholix_base_url or OPENAIRE_SCHOLIX_API_BASE_URL

        current_settings = get_settings()
        session_specific_settings: ApiSettings
        if timeout is not None:
            logger.debug(f"Overriding request timeout for this session to: {timeout}s")
            session_specific_settings = current_settings.model_copy(
                update={"request_timeout": timeout}
            )
        else:
            session_specific_settings = current_settings

        # Pass the original auth_strategy (which can be None) to the client.
        # The client will then decide its auth based on this and its settings.
        logger.debug(
            f"AireloomSession: Initializing AireloomClient with auth_strategy param: {type(auth_strategy)}"
        )
        self._api_client = AireloomClient(
            settings=session_specific_settings,
            auth_strategy=auth_strategy,  # Pass the original auth_strategy parameter
            base_url=_api_base_url,  # Pass Graph API base URL
            scholix_base_url=_scholix_base_url,  # Pass Scholix base URL
        )
        logger.debug(f"AireloomSession initialized for API: {_api_base_url}")
        logger.debug(f"Scholexplorer base URL configured for: {_scholix_base_url}")

    @property
    def queries(self):
        """Access convenience query functions.

        Returns a ``_QueryAccessor`` bound to this session so you can call any
        convenience function without passing the session explicitly::

            papers = await session.queries.publications_by_doi(
                "10.1234/..."
            )
        """
        return _QueryAccessor(queries, self)

    def __getattr__(self, name: str):
        if name in _DELEGATED_CLIENTS:
            return getattr(self._api_client, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __dir__(self):
        return list(super().__dir__()) + list(_DELEGATED_CLIENTS)

    async def close(self) -> None:
        """Closes the underlying HTTP client session."""
        await self._api_client.aclose()

    async def __aenter__(self) -> "AireloomSession":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
