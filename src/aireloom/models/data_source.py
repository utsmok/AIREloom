# aireloom/models/data_source.py
"""Pydantic models for representing OpenAIRE Data Source entities.

Reference: https://graph.openaire.eu/docs/data-model/entities/data-source
"""

from bibliofabric import SafeList, SafeStr
from pydantic import Field, computed_field

from .base import ApiResponse, BaseEntity, CfHbKeyValue, CodeLabel, Pid, safe
from .research_product import Container, RelatedRecord


class DataSource(BaseEntity):
    """Model representing an OpenAIRE Data Source entity.

    A data source in OpenAIRE can be a repository, journal, aggregator, etc.
    Inherits the ``id`` field from ``BaseEntity``.
    """

    originalIds: SafeList[str] = Field(default_factory=list)
    pids: SafeList[Pid] = Field(default_factory=list)
    type: safe(Pid) = Field(default_factory=Pid)
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
    journal: safe(Container) = Field(default_factory=Container)
    # Harvesting endpoints (e.g. OAI-PMH base URL), added upstream in 1.5.0.
    endpoints: SafeList[str] = Field(default_factory=list)
    # V3 fields
    collectedFrom: SafeList[safe(CfHbKeyValue)] = Field(default_factory=list)
    thematic: bool | None = None
    eoscdatasourcetype: safe(CodeLabel) = Field(default_factory=CodeLabel)
    jurisdiction: safe(CodeLabel) = Field(default_factory=CodeLabel)
    odlanguages: SafeList[str] = Field(default_factory=list)
    openaireCompatibilityId: str | None = None
    links: SafeList[RelatedRecord] = Field(default_factory=list)

    @computed_field
    @property
    def type_name(self) -> str | None:
        return self.type.value or None

    def __str__(self) -> str:
        name = self.officialName or self.englishName
        if name:
            return name
        return f"DataSource(id={self.id!r})"


# Define the specific response type for data sources
DataSourceResponse = ApiResponse[DataSource]
"""Type alias for an API response containing a list of `DataSource` entities."""
