# aireloom/models/project.py
"""Pydantic models for representing OpenAIRE Project entities and related structures.

This module defines the Pydantic model for an OpenAIRE Project,
including nested models for funding details, grants, and H2020 programme
information, based on the OpenAIRE data model documentation.
Reference: https://graph.openaire.eu/docs/data-model/entities/project
"""

from typing import Any

from bibliofabric import SafeList, SafeStr
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from .base import (
    ApiResponse,
    BaseEntity,
    CodeLabel,
    FundingHierarchy,
    RelatedRecordHeader,
    TypedPid,
    safe,
)


class FundingStream(BaseModel):
    """A funding stream: ``{"id", "description"}``."""

    description: SafeStr = ""
    id: str | None = None

    model_config = ConfigDict(extra="allow")


class Funding(BaseModel):
    """Flat funding entry in ``Project.fundings[]``."""

    fundingStream: safe(FundingStream) = Field(default_factory=FundingStream)
    jurisdiction: str | None = None
    name: SafeStr = ""
    shortName: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class Grant(BaseModel):
    """Grant amounts for a project (``Project.granted``)."""

    currency: SafeStr = ""
    fundedAmount: float | None = None
    totalCost: float | None = None

    model_config = ConfigDict(extra="allow")


class H2020Programme(BaseModel):
    """An H2020 programme related to a project."""

    code: str | None = None
    description: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class ProjectLink(BaseModel):
    """A related-entity link entry in ``Project.links`` (e.g. participant orgs)."""

    header: safe(RelatedRecordHeader) = Field(default_factory=RelatedRecordHeader)
    legalname: SafeStr = ""
    pid: SafeList[TypedPid] = Field(default_factory=list)
    country: safe(CodeLabel) = Field(default_factory=CodeLabel)

    model_config = ConfigDict(extra="allow")


class Project(BaseEntity):
    """Model representing an OpenAIRE Project entity.

    Captures identifiers, title, funding, duration, and related metadata.
    Inherits the ``id`` field from ``BaseEntity``.
    """

    code: str | None = None
    acronym: SafeStr = ""
    title: SafeStr = ""
    callIdentifier: str | None = None
    fundings: SafeList[Funding] = Field(default_factory=list)
    funding: safe(FundingHierarchy) = Field(default_factory=FundingHierarchy)
    granted: safe(Grant) = Field(default_factory=Grant)
    h2020Programmes: SafeList[H2020Programme] = Field(default_factory=list)
    keywords: SafeList[str] = Field(default_factory=list)
    openAccessMandateForDataset: bool | None = None
    openAccessMandateForPublications: bool | None = None
    # Dates are kept as strings: parts may be missing or null.
    startDate: str | None = None
    endDate: str | None = None
    subjects: SafeList[str] = Field(default_factory=list)
    summary: SafeStr = ""
    websiteUrl: str | None = None
    links: SafeList[ProjectLink] = Field(default_factory=list)

    @computed_field
    @property
    def funder_name(self) -> str | None:
        if self.fundings:
            f = self.fundings[0]
            return f.shortName or f.name or None
        return None

    @computed_field
    @property
    def funder_jurisdiction(self) -> str | None:
        if self.fundings:
            return self.fundings[0].jurisdiction
        return None

    @computed_field
    @property
    def start_year(self) -> int | None:
        if self.startDate:
            try:
                return int(self.startDate[:4])
            except ValueError:
                return None
        return None

    @computed_field
    @property
    def end_year(self) -> int | None:
        if self.endDate:
            try:
                return int(self.endDate[:4])
            except ValueError:
                return None
        return None

    def __str__(self) -> str:
        parts = []
        if self.title:
            parts.append(self.title[:80])
        if self.code:
            parts.append(f"[{self.code}]")
        if self.funder_name:
            parts.append(f"funded by {self.funder_name}")
        return " | ".join(parts) if parts else f"Project(id={self.id!r})"

    @field_validator("keywords", mode="before")
    @classmethod
    def parse_keywords_string(cls, v: Any) -> Any:
        """Split a delimited keyword string (comma, then semicolon) into a list."""
        if isinstance(v, str):
            for delimiter in (",", ";"):
                parts = [part.strip() for part in v.split(delimiter) if part.strip()]
                if parts:
                    return parts
            return []
        return v


# Define the specific response type for projects
ProjectResponse = ApiResponse[Project]
"""Type alias for an API response containing a list of `Project` entities."""
