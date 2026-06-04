"""Models for Graph API /researchProducts/links responses."""

import logging

from pydantic import BaseModel, ConfigDict

from .base import Header

logger = logging.getLogger(__name__)


class Identifier(BaseModel):
    """An identifier with id, scheme, and url."""

    id: str | None = None
    idScheme: str | None = None
    idUrl: str | None = None
    model_config = ConfigDict(extra="allow")


class EntityRef(BaseModel):
    """Named entity with identifiers (authors, collectedFrom)."""

    name: str | None = None
    identifiers: list[Identifier] | None = None
    model_config = ConfigDict(extra="allow")


class Node(BaseModel):
    """A node (source or target) in a relation link."""

    title: str | None = None
    type: str | None = None
    instanceType: str | None = None
    publicationDate: str | None = None
    identifiers: list[Identifier] | None = None
    authors: list[EntityRef] | None = None
    collectedFrom: list[EntityRef] | None = None
    model_config = ConfigDict(extra="allow")


class RelType(BaseModel):
    """Relation type information."""

    name: str | None = None
    type: str | None = None
    typeSchema: str | None = None
    model_config = ConfigDict(extra="allow")


class Relation(BaseModel):
    """A single relation link between two scholarly entities."""

    source: Node | None = None
    target: Node | None = None
    relType: RelType | None = None
    model_config = ConfigDict(extra="allow")


class LinksResponse(BaseModel):
    """Response envelope for /researchProducts/links endpoint.

    Unlike standard ApiResponse, this is a standalone model because Relation
    entities don't carry an id field required by BaseEntity.
    """

    header: Header | None = None
    results: list[Relation] | None = None
    model_config = ConfigDict(extra="allow")
