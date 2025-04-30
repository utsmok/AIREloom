# https://graph.openaire.eu/docs/data-model/entities/research-product

import logging
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

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
    scheme: Optional[str] = None
    value: Optional[str] = None

    model_config = dict(extra="allow")


class PidProvenance(BaseModel):
    provenance: Optional[str] = None
    trust: Optional[float] = None

    model_config = dict(extra="allow")


class Pid(BaseModel):
    id: Optional[PidIdentifier] = None
    provenance: Optional[PidProvenance] = None

    model_config = dict(extra="allow")


class Author(BaseModel):
    fullName: Optional[str] = None
    rank: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    pid: Optional[Pid] = None

    model_config = dict(extra="allow")


class BestAccessRight(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    scheme: Optional[str] = None

    model_config = dict(extra="allow")


class ResultCountry(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    provenance: Optional[PidProvenance] = None

    model_config = dict(extra="allow")


class CitationImpact(BaseModel):
    influence: Optional[float] = None
    influenceClass: Optional[Literal["C1", "C2", "C3", "C4", "C5"]] = None
    citationCount: Optional[int] = None
    citationClass: Optional[Literal["C1", "C2", "C3", "C4", "C5"]] = None
    popularity: Optional[float] = None
    popularityClass: Optional[Literal["C1", "C2", "C3", "C4", "C5"]] = None
    impulse: Optional[float] = None
    impulseClass: Optional[Literal["C1", "C2", "C3", "C4", "C5"]] = None

    model_config = dict(extra="allow")


class UsageCounts(BaseModel):
    downloads: Optional[int] = None
    views: Optional[int] = None

    @field_validator('downloads', 'views', mode='before')
    @classmethod
    def coerce_str_to_int(cls, v: Any) -> Optional[int]:
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

    model_config = dict(extra="allow")


class Indicator(BaseModel):
    citationImpact: Optional[CitationImpact] = None
    usageCounts: Optional[UsageCounts] = None

    model_config = dict(extra="allow")


class AccessRight(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    openAccessRoute: Optional[OpenAccessRouteType] = None
    scheme: Optional[str] = None

    model_config = dict(extra="allow")


class ArticleProcessingCharge(BaseModel):
    amount: Optional[str] = None
    currency: Optional[str] = None

    model_config = dict(extra="allow")


class ResultPid(BaseModel):
    scheme: Optional[str] = None
    value: Optional[str] = None

    model_config = dict(extra="allow")


class License(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    provenance: Optional[PidProvenance] = None

    model_config = dict(extra="allow")


class Instance(BaseModel):
    accessRight: Optional[AccessRight] = None
    alternateIdentifier: list[dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: Optional[ArticleProcessingCharge] = None
    license: Optional[License] = None
    collectedFrom: Optional[dict[str, str]] = None
    hostedBy: Optional[dict[str, str]] = None
    distributionLocation: Optional[str] = None
    embargoEndDate: Optional[str] = None
    instanceId: Optional[str] = None
    publicationDate: Optional[str] = None
    refereed: Optional[RefereedType] = None
    type: Optional[str] = None
    urls: list[str] = Field(default_factory=list)

    model_config = dict(extra="allow")


class Language(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None

    model_config = dict(extra="allow")


class Subject(BaseModel):
    subject: Optional[dict[str, str]] = None
    provenance: Optional[PidProvenance] = None

    model_config = dict(extra="allow")


# Container for Publication
class Container(BaseModel):
    edition: Optional[str] = None
    iss: Optional[str] = None
    issnLinking: Optional[str] = None
    issnOnline: Optional[str] = None
    issnPrinted: Optional[str] = None
    name: Optional[str] = None
    sp: Optional[str] = None
    ep: Optional[str] = None
    vol: Optional[str] = None

    model_config = dict(extra="allow")


# GeoLocation for Data
class GeoLocation(BaseModel):
    box: Optional[str] = None
    place: Optional[str] = None
    point: Optional[str] = None

    model_config = dict(extra="allow")


# Update main ResearchProduct model
class ResearchProduct(BaseEntity):
    type: Optional[ResearchProductType] = None
    originalId: list[str] = Field(default_factory=list)
    mainTitle: Optional[str] = None
    subTitle: Optional[str] = None
    author: list[Author] = Field(default_factory=list)
    bestAccessRight: Optional[BestAccessRight] = None
    contributors: list[str] = Field(default_factory=list)
    country: list[ResultCountry] = Field(default_factory=list)
    coverages: list[str] = Field(default_factory=list)
    dateOfCollection: Optional[str] = None
    descriptions: list[str] = Field(default_factory=list)
    embargoEndDate: Optional[str] = None
    indicators: Optional[Indicator] = None
    instance: list[Instance] = Field(default_factory=list)
    language: Optional[Language] = None
    lastUpdateTimeStamp: Optional[int] = None
    pid: list[ResultPid] = Field(default_factory=list)
    publicationDate: Optional[str] = None
    publisher: Optional[str] = None
    source: list[str] = Field(default_factory=list)
    formats: list[str] = Field(default_factory=list)
    subjects: list[Subject] = Field(default_factory=list)
    isGreen: Optional[bool] = None
    openAccessColor: Optional[str] = None
    isInDiamondJournal: Optional[bool] = None
    publiclyFunded: Optional[bool] = None

    # Optional nested objects for specific types
    container: Optional[Container] = None
    # for datasets
    size: Optional[str] = None
    version: Optional[str] = None
    geolocations: list[GeoLocation] = Field(default_factory=list)
    # for software
    documentationUrls: list[str] = Field(default_factory=list)
    codeRepositoryUrl: Optional[str] = None
    programmingLanguage: Optional[str] = None
    # for other research products
    contactPeople: list[str] = Field(default_factory=list)
    contactGroups: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)

    model_config = dict(extra="allow")


# Define the specific response type for ResearchProduct results
ResearchProductResponse = ApiResponse[ResearchProduct]
