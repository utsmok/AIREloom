# https://graph.openaire.eu/docs/data-model/entities/organization

from pydantic import BaseModel, Field

from .research_product import ResultPid

class Country(BaseModel):
    code: str | None = None
    label: str | None = None

    class Config:
        frozen = True

class OrganizationPid(BaseModel):
    scheme: str | None = None
    value: str | None = None

    class Config:
        frozen = True

class Organization(BaseModel):
    id: str | None = None
    legalShortName: str | None = None
    legalName: str | None = None
    alternativeNames: list[str] = Field(default_factory=list)
    websiteUrl: str | None = None
    country: Country | None = None
    pids: list[OrganizationPid] = Field(default_factory=list)

    class Config:
        frozen = True

# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None

    class Config:
        frozen = True

class Message(BaseModel):
    header: Header
    results: list[Organization]

    class Config:
        frozen = True