# https://graph.openaire.eu/docs/data-model/relationships/relationship-object
# https://graph.openaire.eu/docs/data-model/relationships/relationship-types

from typing import Literal
from pydantic import BaseModel, Field

from .research_product import PidProvenance

# Type literals
EntityType = Literal["project", "organization", "researchproduct", "datasource", "community"]

class RelType(BaseModel):
    type: str | None = None
    name: str | None = None

    class Config:
        frozen = True

class Relationship(BaseModel):
    source: str | None = None
    sourceType: EntityType | None = None
    target: str | None = None
    targetType: EntityType | None = None
    relType: RelType | None = None
    provenance: PidProvenance | None = None  # Reuse PidProvenance as it matches Provenance structure
    validated: bool | None = None
    validationDate: str | None = None

    class Config:
        frozen = True

# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None

    class Config:
        frozen = True

class Message(BaseModel):
    header: Header
    results: list[Relationship]

    class Config:
        frozen = True