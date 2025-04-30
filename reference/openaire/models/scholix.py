# https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema

from typing import Literal

from pydantic import BaseModel, Field

RelationshipName = Literal[
    "IsSupplementTo", "IsSupplementedBy", "References", "IsReferencedBy", "IsRelatedTo"
]
EntityType = Literal["publication", "dataset", "software", "other"]


class Identifier(BaseModel):
    ID: str | None = None
    IDScheme: str | None = None
    IDURL: str | None = None

    class Config:
        frozen = True


class LinkProvider(BaseModel):
    name: str | None = None
    identifier: list[Identifier] = Field(default_factory=list)

    class Config:
        frozen = True


class RelationshipType(BaseModel):
    Name: RelationshipName | None = None
    SubType: str | None = None
    SubTypeSchema: str | None = None

    class Config:
        frozen = True


class Creator(BaseModel):
    Name: str | None = None
    Identifier: "Identifier" | None = None

    class Config:
        frozen = True


class Publisher(BaseModel):
    name: str | None = None
    Identifier: list["Identifier"] = Field(default_factory=list)

    class Config:
        frozen = True


class Entity(BaseModel):
    Identifier: list["Identifier"] = Field(default_factory=list)
    Type: EntityType | None = None
    SubType: str | None = None
    Title: str | None = None
    Creator: list["Creator"] = Field(default_factory=list)
    PublicationDate: str | None = None
    Publisher: list["Publisher"] = Field(default_factory=list)

    class Config:
        frozen = True


class ScholixRelationship(BaseModel):
    LinkPublicationDate: str | None = None
    LinkProvider: list["LinkProvider"] = Field(default_factory=list)
    RelationshipType: "RelationshipType" | None = None
    LicenseURL: str | None = None
    Source: Entity | None = None
    Target: Entity | None = None

    class Config:
        frozen = True


# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None

    class Config:
        frozen = True


class Message(BaseModel):
    header: Header
    results: list[ScholixRelationship]

    class Config:
        frozen = True
