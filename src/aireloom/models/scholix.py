# aireloom/models/scholix.py
"""Pydantic models for representing Scholix (Scholarly Link Exchange) data.

This module defines Pydantic models for parsing and validating data from the
OpenAIRE Scholexplorer API, which follows the Scholix schema. It includes
models for entities, relationships, identifiers, and the overall response structure.
Reference: https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema
and DDI-CDI Codi Model: https://ddi-alliance.github.io/DDI-CDI/current/Model/
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .safe_types import SafeList, SafeStr

ScholixEntityTypeName = Literal["publication", "dataset", "software", "other"]
"""Defines the allowed types for a Scholix entity (e.g., publication, dataset)."""
ScholixRelationshipNameValue = Literal[
    "IsRelatedTo", "References", "IsReferencedBy",
    "IsSupplementTo", "IsSupplementedBy",
    "IsSourceOf", "IsDerivedFrom", "IsVersionOf",
    "HasVersion", "IsPartOf", "IsPreviousVersionOf",
    "IsNewVersionOf", "IsIdenticalTo", "IsContinuedBy",
    "Continues", "IsCompiledBy", "Compiles",
    "IsDescribedBy", "Describes", "HasAmongTopNSimilarDocuments",
    "IsAmongTopNSimilarDocuments", "Reviews", "IsReviewedBy",
    "Cites", "IsCitedBy", "IsOriginalFormOf",
    "IsVariantFormOf", "IsPublishedIn",
]
"""Known relationship type names in the Scholix schema."""

class ScholixIdentifier(BaseModel):
    """Represents a persistent identifier within the Scholix schema.

    Attributes:
        id_val: The value of the identifier (aliased from "ID").
        id_scheme: The scheme of the identifier (aliased from "IDScheme", e.g., "doi", "url").
        id_url: An optional URL or string for the identifier (aliased from "IDURL").
    """

    id_val: SafeStr = Field(alias="ID", default="")
    id_scheme: SafeStr = Field(alias="IDScheme", default="")
    id_url: str | None = Field(alias="IDURL", default=None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixCreator(BaseModel):
    """Represents a creator (e.g., author, contributor) in the Scholix schema.

    Attributes:
        name: The name of the creator (aliased from "Name").
        identifier: An optional list of `ScholixIdentifier` objects for the creator.
    """

    name: SafeStr = Field(alias="Name", default="")
    identifier: list[ScholixIdentifier] | None = Field(alias="Identifier", default=None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixPublisher(BaseModel):
    """Represents a publisher in the Scholix schema.

    Attributes:
        name: The name of the publisher (aliased from "Name").
        identifier: An optional list of `ScholixIdentifier` objects for the publisher.
    """

    name: SafeStr = Field(alias="Name", default="")
    identifier: list[ScholixIdentifier] | None = Field(alias="Identifier", default=None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixEntity(BaseModel):
    """Represents a scholarly entity (source or target) in a Scholix relationship.

    Attributes:
        identifier: A list of `ScholixIdentifier` objects for the entity.
        type: The `ScholixEntityTypeName` (e.g., "publication", "dataset").
        sub_type: An optional subtype providing more specific classification.
        title: The title of the scholarly entity.
        creator: A list of `ScholixCreator` objects.
        publication_date: The publication date of the entity (string format).
        publisher: A list of `ScholixPublisher` objects.
    """

    identifier: SafeList[ScholixIdentifier] = Field(alias="Identifier", default_factory=list)
    type: ScholixEntityTypeName = Field(alias="Type")
    sub_type: str | None = Field(alias="SubType", default=None)
    title: SafeStr = Field(alias="Title", default="")
    creator: SafeList[ScholixCreator] = Field(alias="Creator", default_factory=list)
    publication_date: str | None = Field(alias="PublicationDate", default=None)
    publisher: SafeList[ScholixPublisher] = Field(alias="Publisher", default_factory=list)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixRelationshipType(BaseModel):
    """Describes the type of relationship between two Scholix entities.

    Attributes:
        name: The primary name of the relationship type (e.g., "References", "IsSupplementTo").
        sub_type: An optional subtype for more specific relationship classification.
        sub_type_schema: An optional schema identifier (may be a URL or a short string like 'datacite').
    """

    name: ScholixRelationshipNameValue | str = Field(alias="Name", default="")
    sub_type: str | None = Field(alias="SubType", default=None)
    sub_type_schema: str | None = Field(alias="SubTypeSchema", default=None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixLinkProvider(BaseModel):
    """Represents the provider of the Scholix link.

    Attributes:
        name: The name of the link provider (aliased from "Name").
        identifier: An optional list of `ScholixIdentifier` objects for the provider.
    """

    name: SafeStr = Field(alias="Name", default="")
    identifier: SafeList[ScholixIdentifier] = Field(alias="Identifier", default_factory=list)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixRelationship(BaseModel):
    """Represents a single Scholix relationship link between two scholarly entities.

    This is a core model in the Scholix schema, detailing the link provider,
    the type of relationship, the source entity, and the target entity.

    Attributes:
        link_provider: A list of `ScholixLinkProvider` objects detailing who provided the link.
        relationship_type: A `ScholixRelationshipType` object describing the nature of the link.
        source: A `ScholixEntity` representing the source of the relationship.
        target: A `ScholixEntity` representing the target of the relationship.
        link_publication_date: The date when this link was published or made available.
        license_url: An optional URL pointing to the license governing the use of this link information.
        harvest_date: The date when this link information was last harvested or updated.
    """

    link_provider: list[ScholixLinkProvider] | None = Field(
        alias="LinkProvider", default=None
    )
    relationship_type: ScholixRelationshipType = Field(alias="RelationshipType")
    source: ScholixEntity = Field(alias="Source")
    target: ScholixEntity = Field(alias="Target")
    link_publication_date: datetime | None = Field(
        alias="LinkPublicationDate",
        default=None,
        description="Date the link was published.",
    )
    license_url: str | None = Field(alias="LicenseURL", default=None)
    harvest_date: str | None = Field(alias="HarvestDate", default=None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ScholixResponse(BaseModel):
    """Response structure for the Scholexplorer Links endpoint."""

    current_page: int = Field(
        default=0,
        alias="currentPage",
        description="The current page number (0-indexed).",
    )
    total_links: int = Field(
        default=0,
        alias="totalLinks",
        description="Total number of links matching the query.",
    )
    total_pages: int = Field(
        default=0,
        alias="totalPages",
        description="Total number of pages available.",
    )
    result: list[ScholixRelationship] = Field(
        default_factory=list,
        alias="result",
        description="List of Scholix relationship links.",
    )

    model_config = ConfigDict(populate_by_name=True, extra="allow")
