"""Pydantic models for OpenAIRE API entities and responses."""

from .base import ApiResponse, BaseEntity, Header
from .data_source import ControlledField, DataSource, DataSourceResponse
from .organization import Country, Organization, OrganizationPid, OrganizationResponse
from .person import Person, PersonResponse
from .project import (
    Funding,
    FundingStream,
    Grant,
    H2020Programme,
    Project,
    ProjectResponse,
)
from .relation import (
    EntityRef,
    Identifier,
    LinksResponse,
    Node,
    Relation,
    RelType,
)
from .research_product import ResearchProduct, ResearchProductResponse
from .safe_types import SafeList, SafeStr
from .scholix import (
    ScholixCreator,
    ScholixEntity,
    ScholixIdentifier,
    ScholixLinkProvider,
    ScholixPublisher,
    ScholixRelationship,
    ScholixResponse,
)

__all__ = [
    "ApiResponse",
    "BaseEntity",
    "SafeList",
    "SafeStr",
    "ControlledField",
    "Country",
    "DataSource",
    "DataSourceResponse",
    "EntityRef",
    "Funding",
    "FundingStream",
    "Grant",
    "H2020Programme",
    "Header",
    "Identifier",
    "LinksResponse",
    "Node",
    "Organization",
    "OrganizationPid",
    "OrganizationResponse",
    "Person",
    "PersonResponse",
    "Project",
    "ProjectResponse",
    "Relation",
    "RelType",
    "ResearchProduct",
    "ResearchProductResponse",
    "ScholixCreator",
    "ScholixEntity",
    "ScholixIdentifier",
    "ScholixLinkProvider",
    "ScholixPublisher",
    "ScholixRelationship",
    "ScholixResponse",
]
