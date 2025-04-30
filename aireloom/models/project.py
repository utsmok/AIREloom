# https://graph.openaire.eu/docs/data-model/entities/project

from pydantic import BaseModel, Field

# Import base classes
from .base import ApiResponse, BaseEntity


class FundingStream(BaseModel):
    """Details about the funding stream for a project."""

    description: str | None = None
    id: str | None = None

    class Config:
        extra = "allow"


class Funding(BaseModel):
    """Details about the funding source and stream."""

    fundingStream: FundingStream | None = None
    jurisdiction: str | None = None
    name: str | None = None
    shortName: str | None = None

    class Config:
        extra = "allow"


class Grant(BaseModel):
    """Details about the grant amounts."""

    currency: str | None = None
    fundedAmount: float | None = None
    totalCost: float | None = None

    class Config:
        extra = "allow"


class H2020Programme(BaseModel):
    """Details about the H2020 programme, if applicable."""

    code: str | None = None
    description: str | None = None

    class Config:
        extra = "allow"


class Project(BaseEntity):
    """Model representing an OpenAIRE Project entity."""

    # id is inherited from BaseEntity
    code: str | None = None
    acronym: str | None = None
    title: str | None = None
    callIdentifier: str | None = None
    fundings: list[Funding] | None = Field(default_factory=list)
    granted: Grant | None = None
    h2020Programmes: list[H2020Programme] | None = Field(default_factory=list)
    keywords: str | None = None  # Consider list[str] if API returns multiple keywords
    openAccessMandateForDataset: bool | None = None
    openAccessMandateForPublications: bool | None = None
    startDate: str | None = None  # Consider converting to date/datetime
    endDate: str | None = None  # Consider converting to date/datetime
    subjects: list[str] | None = Field(default_factory=list)
    summary: str | None = None
    websiteUrl: str | None = None


# Define the specific response type for projects
ProjectResponse = ApiResponse[Project]
