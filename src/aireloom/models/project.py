# aireloom/models/project.py
"""Pydantic models for representing OpenAIRE Project entities and related structures.

This module defines the Pydantic model for an OpenAIRE Project,
including nested models for funding details, grants, and H2020 programme information,
based on the OpenAIRE data model documentation.
Reference: https://graph.openaire.eu/docs/data-model/entities/project
"""

from typing import Annotated, Any

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)

from .base import ApiResponse, BaseEntity
from .safe_types import SafeList, SafeStr


class FundingStream(BaseModel):
    """Represents details about a specific funding stream for a project.

    Attributes:
        description: A description of the funding stream.
        id: The unique identifier of the funding stream.
    """

    description: SafeStr = ""
    id: str | None = None
    model_config = ConfigDict(extra="allow")


SafeFundingStream = Annotated[FundingStream, BeforeValidator(lambda v: FundingStream() if v is None else v)]


class Funding(BaseModel):
    """Represents funding information for a project, including the source and stream.

    Attributes:
        fundingStream: A `FundingStream` object detailing the specific stream.
        jurisdiction: The jurisdiction associated with the funding (e.g., country code).
        name: The name of the funding body or organization.
        shortName: An optional short name or acronym for the funding body.
    """

    fundingStream: SafeFundingStream = Field(default_factory=FundingStream)
    jurisdiction: str | None = None
    name: SafeStr = ""
    shortName: SafeStr = ""
    model_config = ConfigDict(extra="allow")


class Grant(BaseModel):
    """Represents details about the grant amounts associated with a project.

    Attributes:
        currency: The currency code for the amounts (e.g., "EUR", "USD").
        fundedAmount: The amount of funding awarded.
        totalCost: The total cost of the project.
    """

    currency: SafeStr = ""
    fundedAmount: float | None = None
    totalCost: float | None = None
    model_config = ConfigDict(extra="allow")


SafeGrant = Annotated[Grant, BeforeValidator(lambda v: Grant() if v is None else v)]


class H2020Programme(BaseModel):
    """Represents details about an H2020 programme related to a project.

    Attributes:
        code: The code of the H2020 programme.
        description: A description of the H2020 programme.
    """

    code: str | None = None
    description: SafeStr = ""
    model_config = ConfigDict(extra="allow")


class Project(BaseEntity):
    """Model representing an OpenAIRE Project entity.

    Captures comprehensive information about a research project, including its
    identifiers, title, funding, duration, and related metadata. Inherits the
    `id` field from `BaseEntity`.

    Attributes:
        code: The project code or grant number.
        acronym: The acronym of the project.
        title: The official title of the project.
        callIdentifier: Identifier for the funding call.
        fundings: A list of `Funding` objects detailing the project's funding sources.
        granted: A `Grant` object with information about the awarded grant amounts.
        h2020Programmes: A list of `H2020Programme` objects if the project is part of H2020.
        keywords: A list of keywords describing the project.
                  A validator attempts to parse comma or semicolon-separated strings.
        openAccessMandateForDataset: Boolean indicating if there's an open access
                                     mandate for datasets produced by the project.
        openAccessMandateForPublications: Boolean indicating if there's an open access
                                          mandate for publications from the project.
        startDate: The start date of the project (typically "YYYY-MM-DD" string).
        endDate: The end date of the project (typically "YYYY-MM-DD" string).
        subjects: A list of subject classifications for the project.
        summary: A summary or abstract of the project.
        websiteUrl: The URL of the project's official website.
    """

    # id is inherited from BaseEntity
    code: str | None = None
    acronym: SafeStr = ""
    title: SafeStr = ""
    callIdentifier: str | None = None
    fundings: SafeList[Funding] = Field(default_factory=list)
    granted: SafeGrant = Field(default_factory=Grant)
    h2020Programmes: SafeList[H2020Programme] = Field(default_factory=list)
    # Keywords might be a single string or a delimited string. Attempt parsing.
    keywords: SafeList[str] = Field(default_factory=list)
    openAccessMandateForDataset: bool | None = None
    openAccessMandateForPublications: bool | None = None
    # Dates are kept as string for safety due to potential missing parts or nulls.
    # Expected format is typically YYYY-MM-DD.
    startDate: str | None = None
    endDate: str | None = None
    subjects: SafeList[str] = Field(default_factory=list)
    summary: SafeStr = ""
    websiteUrl: str | None = None

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
        if self.startDate and len(self.startDate) >= 4:
            try:
                return int(self.startDate[:4])
            except ValueError:
                return None
        return None

    @computed_field
    @property
    def end_year(self) -> int | None:
        if self.endDate and len(self.endDate) >= 4:
            try:
                return int(self.endDate[:4])
            except ValueError:
                return None
        return None

    model_config = ConfigDict(extra="allow")

    @field_validator("keywords", mode="before")
    @classmethod
    def parse_keywords_string(cls, v: Any) -> list[str]:
        """Attempts to parse a keyword string into a list of strings.

        If the input `v` is a string, this validator tries to split it by common
        delimiters (comma, then semicolon). If splitting produces any parts,
        a list of stripped parts is returned. Otherwise an empty list is returned.
        If `v` is not a string (e.g., already a list or None), it's returned as is.

        Args:
            v: The value to parse, expected to be a string, list, or None.

        Returns:
            A list of strings. Returns [] if input was empty or unparseable.
        """
        if isinstance(v, str):
            # Prioritize comma, then semicolon
            delimiters = [",", ";"]
            for delimiter in delimiters:
                parts = [part.strip() for part in v.split(delimiter) if part.strip()]
                if parts:
                    return parts
            return []
        # If not a string (e.g., already a list or None), return as is
        return v


# Define the specific response type for projects
ProjectResponse = ApiResponse[Project]
"""Type alias for an API response containing a list of `Project` entities."""
