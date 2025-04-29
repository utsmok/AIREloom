# https://graph.openaire.eu/docs/data-model/entities/project

from pydantic import BaseModel, Field

class FundingStream(BaseModel):
    description: str | None = None
    id: str | None = None

    class Config:
        frozen = True

class Funding(BaseModel):
    fundingStream: FundingStream | None = None
    jurisdiction: str | None = None
    name: str | None = None
    shortName: str | None = None

    class Config:
        frozen = True

class Grant(BaseModel):
    currency: str | None = None
    fundedAmount: float | None = None
    totalCost: float | None = None

    class Config:
        frozen = True

class H2020Programme(BaseModel):
    code: str | None = None
    description: str | None = None

    class Config:
        frozen = True

class Project(BaseModel):
    id: str | None = None
    code: str | None = None
    acronym: str | None = None
    title: str | None = None
    callIdentifier: str | None = None
    fundings: list[Funding] = Field(default_factory=list)
    granted: Grant | None = None
    h2020Programmes: list[H2020Programme] = Field(default_factory=list)
    keywords: str | None = None
    openAccessMandateForDataset: bool | None = None
    openAccessMandateForPublications: bool | None = None
    startDate: str | None = None
    endDate: str | None = None
    subjects: list[str] = Field(default_factory=list)
    summary: str | None = None
    websiteUrl: str | None = None

    class Config:
        frozen = True

# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None

    class Config:
        frozen = True

class Message(BaseModel):
    header: Header
    results: list[Project]

    class Config:
        frozen = True