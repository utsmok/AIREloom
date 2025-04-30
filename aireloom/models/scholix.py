# https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema

from datetime import datetime
from typing import Annotated, Literal

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
    ID: str
    IDScheme: str
    IDURL: HttpUrl | None = None


class ScholixCreator(BaseModel):
    Name: str | None = None  # Sometimes just identifier is present
    Identifier: list[ScholixIdentifier] | None = None


class ScholixPublisher(BaseModel):
    Name: str
    Identifier: list[ScholixIdentifier] | None = None


class ScholixEntity(BaseModel):
    Identifier: list[ScholixIdentifier]
    Type: ScholixEntityTypeName
    SubType: str | None = None
    Title: str | None = None
    Creator: list[ScholixCreator] | None = None
    PublicationDate: str | None = None  # Keep as string for flexibility
    Publisher: list[ScholixPublisher] | None = None


class ScholixRelationshipType(BaseModel):
    Name: ScholixRelationshipNameValue
    SubType: str | None = None
    SubTypeSchema: HttpUrl | None = None


class ScholixLinkProvider(BaseModel):
    Name: str
    Identifier: list[ScholixIdentifier] | None = None


class ScholixRelationship(BaseModel):
    LinkProvider: list[ScholixLinkProvider] | None = None
    RelationshipType: ScholixRelationshipType
    Source: ScholixEntity
    Target: ScholixEntity
    LinkPublicationDate: datetime | None = Field(
        default=None, description="Date the link was published."
    )
    LicenseURL: HttpUrl | None = None
    # HarvestDate appears in examples but not the schema doc?
    HarvestDate: Annotated[str | None, Field(alias="HarvestDate")] = None


class ScholixResponse(BaseModel):
    """Response structure for the Scholexplorer Links endpoint."""

    currentPage: int = Field(..., description="The current page number (0-indexed).")
    totalLinks: int = Field(
        ..., description="Total number of links matching the query."
    )
    totalPages: int = Field(..., description="Total number of pages available.")
    result: list[ScholixRelationship] = Field(
        ..., description="List of Scholix relationship links."
    )
