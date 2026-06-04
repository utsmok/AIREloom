# aireloom/resources/organizations_client.py
"""Client for interacting with the OpenAIRE Organizations API endpoint.

This module provides the `OrganizationsClient`, which facilitates access to
OpenAIRE's organization data. It leverages generic mixins from `bibliofabric.resources`
for common API operations like retrieving individual entities, searching, and
iterating through result sets.
"""

from typing import TYPE_CHECKING

from bibliofabric.log_config import logger
from bibliofabric.resources import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)

if TYPE_CHECKING:
    from ..client import AireloomClient
from ..endpoints import ORGANIZATIONS
from ..models import Organization, OrganizationResponse


class OrganizationsClient(
    GettableMixin, SearchableMixin, CursorIterableMixin, BaseResourceClient
):
    """Client for the OpenAIRE Organizations API endpoint.

    This client provides standardized methods (`get`, `search`, `iterate`) for
    accessing organization data, by inheriting from `bibliofabric` mixins.
    It is configured with the specific API path and Pydantic models relevant
    to OpenAIRE organizations.

    Attributes:
        _entity_path (str): The API path for organizations.
        _entity_model (type[Organization]): Pydantic model for a single organization.
        _search_response_model (type[OrganizationResponse]): Pydantic model for the
                                                              search response envelope.
    """

    _entity_path: str = ORGANIZATIONS
    _entity_model: type[Organization] = Organization
    _search_response_model: type[OrganizationResponse] = OrganizationResponse

    def __init__(self, api_client: "AireloomClient"):
        """Initializes the OrganizationsClient.

        Args:
            api_client: An instance of AireloomClient.
        """
        super().__init__(api_client)
        logger.debug(
            f"OrganizationsClient initialized for path: {self._entity_path}"
        )

    # All get, search, and iterate methods are now provided by the mixins
