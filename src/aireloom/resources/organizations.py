"""Resource client for OpenAIRE organizations (V4)."""

from ..filters import OrganizationsFilters
from ..models import Organization
from .base import GraphResource


class OrganizationsResource(GraphResource[Organization]):
    """V4 organizations endpoint: search, iterate, count, facets, group_by.

    ``get(id)`` reads the V3 by-id route because V4 has no by-id endpoints.
    """

    path = "v4/organizations"
    model = Organization
    filters_model = OrganizationsFilters
