# aireloom/models/data_source.py
"""Pydantic models for representing OpenAIRE Data Source entities and related structures.

This module defines the Pydantic model for an OpenAIRE Data Source,
including nested models for controlled vocabulary fields and type literals
for restricted string values based on the OpenAIRE data model documentation.
Reference: https://graph.openaire.eu/docs/data-model/entities/data-source
"""

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, computed_field

from .base import ApiResponse, BaseEntity, SafeCfHbKeyValue
from .research_product import Container
from .safe_types import SafeList, SafeStr

# Type literals for restricted values
AccessRightType = Literal["open", "restricted", "closed"]
DatabaseRestrictionType = Literal["feeRequired", "registration", "other"]


# Base classes for controlled fields
class CodeLabel(BaseModel):
    """A code/label pair used by ``eoscdatasourcetype`` and ``jurisdiction``."""

    code: SafeStr = ""
    label: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeCodeLabel = Annotated[
    CodeLabel, BeforeValidator(lambda v: CodeLabel() if v is None else v)
]


class ControlledField(BaseModel):
    """Represents a field with a controlled vocabulary, typically including a scheme and a value.

    This model is used for structured data elements where the value has a specific
    meaning defined by an associated scheme (e.g., a PID like DOI, or a subject
    classification from a specific thesaurus).

    Attributes:
        scheme: The scheme or system defining the context of the value (e.g., "doi", "orcid", "mesh").
        value: The actual value from the controlled vocabulary.
    """

    scheme: SafeStr = ""
    value: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeControlledField = Annotated[
    ControlledField, BeforeValidator(lambda v: ControlledField() if v is None else v)
]

SafeContainer = Annotated[
    Container, BeforeValidator(lambda v: Container() if v is None else v)
]


# Main DataSource model
class DataSource(BaseEntity):
    """Model representing an OpenAIRE Data Source entity.

    A data source in OpenAIRE can be a repository, journal, aggregator, etc.
    This model captures various metadata fields associated with a data source.

    Attributes:
        originalIds: List of original identifiers.
        pids: Persistent identifiers.
        type: Data source type as a scheme/value pair.
        openaireCompatibility: Human-readable OpenAIRE compatibility level.
        officialName: Official name of the data source.
        englishName: English name of the data source.
        websiteUrl: URL of the data source website.
        logoUrl: URL of the data source logo.
        dateOfValidation: Date of last validation.
        description: Description of the data source.
        subjects: Subject keywords.
        languages: Languages covered.
        contentTypes: Content types accepted.
        releaseStartDate: Start date of content coverage.
        releaseEndDate: End date of content coverage.
        accessRights: Access rights policy (V3: plain string, not restricted enum).
        uploadRights: Upload rights policy (V3: plain string, not restricted enum).
        databaseAccessRestriction: Database access restriction (V3: plain string, not restricted enum).
        dataUploadRestriction: Data upload restriction.
        versioning: Whether versioning is supported.
        citationGuidelineUrl: URL to citation guidelines.
        pidSystems: PID systems supported.
        certificates: Certificates held.
        policies: Policy URLs.
        missionStatementUrl: URL to mission statement.
        journal: Journal metadata (if applicable).
        collectedFrom: Data sources this record was collected from (V3).
        thematic: Whether this is a thematic data source (V3).
        eoscdatasourcetype: EOSC data source type as code/label (V3).
        links: Related records linked to this data source (V3; ``RelatedRecord`` objects).
        jurisdiction: Jurisdiction scope as code/label (V3).
        odlanguages: OpenDOAR languages (V3; lowercase response field name).
        openaireCompatibilityId: Machine-readable OpenAIRE compatibility ID (V3).
    """

    originalIds: SafeList[str] = Field(default_factory=list)
    pids: SafeList[ControlledField] = Field(default_factory=list)
    type: SafeControlledField = Field(default_factory=ControlledField)
    openaireCompatibility: str | None = None
    officialName: SafeStr = ""
    englishName: SafeStr = ""
    websiteUrl: str | None = None
    logoUrl: str | None = None
    dateOfValidation: str | None = None
    description: SafeStr = ""
    subjects: SafeList[str] = Field(default_factory=list)
    languages: SafeList[str] = Field(default_factory=list)
    contentTypes: SafeList[str] = Field(default_factory=list)
    releaseStartDate: str | None = None
    releaseEndDate: str | None = None
    accessRights: str | None = None
    uploadRights: str | None = None
    databaseAccessRestriction: str | None = None
    dataUploadRestriction: str | None = None
    versioning: bool | None = None
    citationGuidelineUrl: str | None = None
    pidSystems: str | None = None
    certificates: str | None = None
    policies: SafeList[str] = Field(default_factory=list)
    missionStatementUrl: str | None = None
    journal: SafeContainer = Field(default_factory=Container)
    # --- V3 fields (additive) ---
    collectedFrom: SafeList[SafeCfHbKeyValue] = Field(default_factory=list)
    thematic: bool | None = None
    eoscdatasourcetype: SafeCodeLabel = Field(default_factory=CodeLabel)
    jurisdiction: SafeCodeLabel = Field(default_factory=CodeLabel)
    odlanguages: SafeList[str] = Field(default_factory=list)
    openaireCompatibilityId: str | None = None
    # TODO(v3): type precisely once RelatedRecord shape is confirmed across entity types
    links: SafeList[dict] | None = None

    @computed_field
    @property
    def type_name(self) -> str | None:
        return self.type.value or None

    def __str__(self) -> str:
        name = self.officialName or self.englishName
        if name:
            return name
        return f"DataSource(id={self.id!r})"

    model_config = ConfigDict(extra="allow")


# Define the specific response type for data sources
DataSourceResponse = ApiResponse[DataSource]
"""Type alias for an API response containing a list of `DataSource` entities."""
