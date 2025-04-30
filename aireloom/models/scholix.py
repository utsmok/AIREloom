# https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema

from datetime import datetime
from typing import Annotated, Literal, Optional, List

from pydantic import BaseModel, Field, HttpUrl


# Type Aliases & Literals
ScholixEntityTypeName = Literal["publication", "dataset", "software", "other"]
ScholixRelationshipNameValue = Literal[
    "IsSupplementTo",
    "IsSupplementedBy",
    "References",
    "IsReferencedBy",
    "IsRelatedTo",
]


class ScholixIdentifier(BaseModel):
    # Renamed fields to snake_case, added aliases
    id_val: str = Field(alias='ID')
    id_scheme: str = Field(alias='IDScheme')
    id_url: Optional[HttpUrl] = Field(alias='IDURL', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixCreator(BaseModel):
    # Renamed fields to snake_case, added aliases
    name: Optional[str] = Field(alias='Name', default=None)
    identifier: Optional[List[ScholixIdentifier]] = Field(alias='Identifier', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixPublisher(BaseModel):
    # Renamed fields to snake_case, added aliases
    name: str = Field(alias='Name') # Required field
    identifier: Optional[List[ScholixIdentifier]] = Field(alias='Identifier', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixEntity(BaseModel):
    # Renamed fields to snake_case, added aliases
    identifier: List[ScholixIdentifier] = Field(alias='Identifier') # Required field
    type: ScholixEntityTypeName = Field(alias='Type') # Required field
    sub_type: Optional[str] = Field(alias='SubType', default=None)
    title: Optional[str] = Field(alias='Title', default=None)
    creator: Optional[List[ScholixCreator]] = Field(alias='Creator', default=None)
    publication_date: Optional[str] = Field(alias='PublicationDate', default=None)
    publisher: Optional[List[ScholixPublisher]] = Field(alias='Publisher', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixRelationshipType(BaseModel):
    # Renamed fields to snake_case, added aliases
    name: ScholixRelationshipNameValue = Field(alias='Name') # Required field
    sub_type: Optional[str] = Field(alias='SubType', default=None)
    sub_type_schema: Optional[HttpUrl] = Field(alias='SubTypeSchema', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixLinkProvider(BaseModel):
    # Renamed fields to snake_case, added aliases
    name: str = Field(alias='Name') # Required field
    identifier: Optional[List[ScholixIdentifier]] = Field(alias='Identifier', default=None)

    model_config = dict(populate_by_name=True, extra="allow") # Added missing config


class ScholixRelationship(BaseModel):
    # Renamed fields to snake_case, added aliases
    link_provider: Optional[List[ScholixLinkProvider]] = Field(alias='LinkProvider', default=None)
    relationship_type: ScholixRelationshipType = Field(alias='RelationshipType') # Required
    source: ScholixEntity = Field(alias='Source') # Required
    target: ScholixEntity = Field(alias='Target') # Required
    link_publication_date: Optional[datetime] = Field(
        alias='LinkPublicationDate', default=None, description="Date the link was published."
    )
    license_url: Optional[HttpUrl] = Field(alias='LicenseURL', default=None)
    # Use alias for HarvestDate, keep Optional[str]
    harvest_date: Optional[str] = Field(alias='HarvestDate', default=None)

    model_config = dict(populate_by_name=True, extra="allow")


class ScholixResponse(BaseModel):
    """Response structure for the Scholexplorer Links endpoint."""
    # Renamed fields to snake_case, added aliases, ensured required
    current_page: int = Field(alias='currentPage', description="The current page number (0-indexed).")
    total_links: int = Field(
        alias='totalLinks', description="Total number of links matching the query."
    )
    total_pages: int = Field(alias='totalPages', description="Total number of pages available.")
    result: List[ScholixRelationship] = Field(
        alias='result', description="List of Scholix relationship links."
    )

    model_config = dict(populate_by_name=True, extra="allow")
