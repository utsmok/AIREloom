# https://graph.openaire.eu/docs/data-model/entities/research-product

import logging
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,  # model_validator was in the original thought process but not used here. Keeping for consistency if other models use it.
)

from .base import ApiResponse, BaseEntity

"""
This module contains the Pydantic models for parsing & validation OpenAIRE API responses.
The models are designed to be used with the OpenAIRE Graph API and are structured to match
the expected JSON response format for Research Products.
"""

OpenAccessRouteType = Literal["gold", "green", "hybrid", "bronze"]
RefereedType = Literal["peerReviewed", "nonPeerReviewed", "UNKNOWN"]
ResearchProductType = Literal["publication", "dataset", "software", "other"]

logger = logging.getLogger(__name__)


# Sub-models for nested structures
class PidIdentifier(BaseModel):
    scheme: str | None = None
    value: str | None = None

    model_config = ConfigDict(extra="allow")


class PidProvenance(BaseModel):
    provenance: str | None = None
    trust: float | None = None

    model_config = ConfigDict(extra="allow")


class Pid(BaseModel):
    id: PidIdentifier | None = None
    provenance: PidProvenance | None = None

    model_config = ConfigDict(extra="allow")


class Author(BaseModel):
    fullName: str | None = None
    rank: int | None = None
    name: str | None = None
    surname: str | None = None
    pid: Pid | None = None

    model_config = ConfigDict(extra="allow")


class BestAccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    scheme: str | None = None

    model_config = ConfigDict(extra="allow")


class ResultCountry(BaseModel):
    code: str | None = None
    label: str | None = None
    provenance: PidProvenance | None = None

    model_config = ConfigDict(extra="allow")


class CitationImpact(BaseModel):
    influence: float | None = None
    influenceClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    citationCount: int | None = None
    citationClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    popularity: float | None = None
    popularityClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    impulse: float | None = None
    impulseClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None

    model_config = ConfigDict(extra="allow")


class UsageCounts(BaseModel):
    downloads: int | None = None
    views: int | None = None

    @field_validator("downloads", "views", mode="before")
    @classmethod
    def coerce_str_to_int(cls, v: Any) -> int | None:
        """Coerce string count values to integers, handling None and errors."""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except (ValueError, TypeError):
                logger.warning(f"Could not coerce UsageCounts value '{v}' to int.")
                return None
        if isinstance(v, int):
            return v
        logger.warning(f"Unexpected type {type(v)} for UsageCounts value '{v}'.")
        return None

    model_config = ConfigDict(extra="allow")


class Indicator(BaseModel):
    citationImpact: CitationImpact | None = None
    usageCounts: UsageCounts | None = None

    model_config = ConfigDict(extra="allow")


class AccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    openAccessRoute: OpenAccessRouteType | None = None
    scheme: str | None = None

    model_config = ConfigDict(extra="allow")


class ArticleProcessingCharge(BaseModel):
    amount: str | None = None
    currency: str | None = None

    model_config = ConfigDict(extra="allow")


class ResultPid(BaseModel):
    scheme: str | None = None
    value: str | None = None

    model_config = ConfigDict(extra="allow")


class License(BaseModel):
    code: str | None = None
    label: str | None = None
    provenance: PidProvenance | None = None

    model_config = ConfigDict(extra="allow")


class Instance(BaseModel):
    accessRight: AccessRight | None = None
    alternateIdentifier: list[dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: ArticleProcessingCharge | None = None
    license: License | None = None
    collectedFrom: dict[str, str] | None = None
    hostedBy: dict[str, str] | None = None
    distributionLocation: str | None = None
    embargoEndDate: str | None = None
    instanceId: str | None = None
    publicationDate: str | None = None
    refereed: RefereedType | None = None
    type: str | None = None
    urls: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")


class Language(BaseModel):
    code: str | None = None
    label: str | None = None

    model_config = ConfigDict(extra="allow")


class Subject(BaseModel):
    subject: dict[str, str] | None = None
    provenance: PidProvenance | None = None

    model_config = ConfigDict(extra="allow")


# Container for Publication
class Container(BaseModel):
    edition: str | None = None
    iss: str | None = None
    issnLinking: str | None = None
    issnOnline: str | None = None
    issnPrinted: str | None = None
    name: str | None = None
    sp: str | None = None
    ep: str | None = None
    vol: str | None = None

    model_config = ConfigDict(extra="allow")


# GeoLocation for Data
class GeoLocation(BaseModel):
    box: str | None = None
    place: str | None = None
    point: str | None = None

    model_config = ConfigDict(extra="allow")


# Update main ResearchProduct model
class ResearchProduct(BaseEntity):
    type: ResearchProductType | None = None
    originalId: list[str] = Field(default_factory=list)
    mainTitle: str | None = None
    subTitle: str | None = None
    author: list[Author] = Field(default_factory=list)
    bestAccessRight: BestAccessRight | None = None
    contributors: list[str] | None = None
    country: list[ResultCountry] = Field(default_factory=list)
    coverages: list[str] | None = None
    dateOfCollection: str | None = None
    descriptions: list[str] = Field(default_factory=list)
    embargoEndDate: str | None = None
    indicators: Indicator | None = None
    instance: list[Instance] = Field(default_factory=list)
    language: Language | None = None
    lastUpdateTimeStamp: int | None = None
    pid: list[ResultPid] = Field(default_factory=list)
    publicationDate: str | None = None
    publisher: str | None = None
    source: list[str] = Field(default_factory=list)
    formats: list[str] | None = None
    subjects: list[Subject] | None = None
    isGreen: bool | None = None
    openAccessColor: str | None = None
    isInDiamondJournal: bool | None = None
    publiclyFunded: bool | None = None

    # Optional nested objects for specific types
    container: Container | None = None
    # for datasets
    size: str | None = None
    version: str | None = None
    geolocations: list[GeoLocation] = Field(default_factory=list)
    # for software
    documentationUrls: list[str] | None = None
    codeRepositoryUrl: str | None = None
    programmingLanguage: str | None = None
    # for other research products
    contactPeople: list[str] | None = None
    contactGroups: list[str] | None = None
    tools: list[str] | None = None

    @field_validator("type", mode="before")
    @classmethod
    def flatten_type_field(cls, v: Any) -> str | None:
        if isinstance(v, dict):
            return v.get("name")
        if isinstance(v, str) or v is None:
            return v
        logger.warning(
            f"Unexpected value for ResearchProduct.type: {v}. Expected dict, str, or None."
        )
        return None  # Or raise ValueError if strictness is preferred

    model_config = ConfigDict(extra="allow")


# Define the specific response type for ResearchProduct results
ResearchProductResponse = ApiResponse[ResearchProduct]
