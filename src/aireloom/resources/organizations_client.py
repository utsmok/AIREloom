# aireloom/resources/organizations_client.py
"""Client for interacting with the OpenAIRE Organizations API endpoint."""

from ..endpoints import ORGANIZATIONS
from ..models import Organization, OrganizationResponse
from ._standard import StandardResourceClient


class OrganizationsClient(StandardResourceClient):
    """Client for the OpenAIRE Organizations API endpoint.

    Attributes:
        _entity_path (str): The API path for organizations.
        _entity_model (type[Organization]): Pydantic model for a single organization.
        _search_response_model (type[OrganizationResponse]): Pydantic model for the
                                                              search response envelope.
    """

    _entity_path: str = ORGANIZATIONS
    _entity_model: type[Organization] = Organization
    _search_response_model: type[OrganizationResponse] = OrganizationResponse
    _batch_fields: dict[str, str] = {
        "pid": "pid",
        "openaire_id": "id",
    }
