# https://graph.openaire.eu/docs/data-model/entities/data-source
from typing import Literal

from pydantic import BaseModel, Field

from .research_product import Container

# Type literals for restricted values
AccessRightType = Literal["open", "restricted", "closed"]
DatabaseRestrictionType = Literal["feeRequired", "registration", "other"]


# Base classes for controlled fields
class ControlledField(BaseModel):
    scheme: str | None = None
    value: str | None = None
    model_config = dict(extra="allow")

# Main DataSource model
class DataSource(BaseModel):
    id: str | None = None
    originalIds: list[str] = Field(default_factory=list)
    pids: list[ControlledField] = Field(default_factory=list)
    type: ControlledField | None = None
    openaireCompatibility: str | None = None
    officialName: str | None = None
    englishName: str | None = None
    websiteUrl: str | None = None
    logoUrl: str | None = None
    dateOfValidation: str | None = None
    description: str | None = None
    subjects: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    contentTypes: list[str] = Field(default_factory=list)
    releaseStartDate: str | None = None
    releaseEndDate: str | None = None
    accessRights: AccessRightType | None = None
    uploadRights: AccessRightType | None = None
    databaseAccessRestriction: DatabaseRestrictionType | None = None
    dataUploadRestriction: str | None = None  # Can be space-separated combination
    versioning: bool | None = None
    citationGuidelineUrl: str | None = None
    pidSystems: str | None = None
    certificates: str | None = None
    policies: list[str] = Field(default_factory=list)
    journal: Container | None = None  # Reuse Container from research_product.py
    missionStatementUrl: str | None = None
    model_config = dict(extra="allow")

# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None
    model_config = dict(extra="allow")


class Message(BaseModel):
    header: Header
    results: list[DataSource]

    model_config = dict(extra="allow")
