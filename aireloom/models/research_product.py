# https://graph.openaire.eu/docs/data-model/entities/research-product

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

# Import base classes
from .base import ApiResponse, BaseEntity

"""
This module contains the Pydantic models for parsing & validation OpenAIRE API responses.
The models are designed to be used with the OpenAIRE Graph API and are structured to match
the expected JSON response format for Research Products.
"""

# Add type literals for restricted values
OpenAccessRouteType = Literal["gold", "green", "hybrid", "bronze"]
RefereedType = Literal["peerReviewed", "nonPeerReviewed", "UNKNOWN"]
ResearchProductType = Literal["publication", "dataset", "software", "other"]


# Sub-models for nested structures
class PidIdentifier(BaseModel):
    scheme: str | None = None
    value: str | None = None

    class Config:
        extra = "allow"


class PidProvenance(BaseModel):
    provenance: str | None = None
    trust: float | None = None

    class Config:
        extra = "allow"


class Pid(BaseModel):
    id: PidIdentifier | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("id"):
                data["id"] = PidIdentifier()
            if not data.get("provenance"):
                data["provenance"] = PidProvenance()
        return data

    class Config:
        extra = "allow"


class Author(BaseModel):
    fullName: str | None = None
    rank: int | None = None
    name: str | None = None
    surname: str | None = None
    pid: Pid | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("pid"):
            data["pid"] = Pid()
        return data

    class Config:
        extra = "allow"


class BestAccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    scheme: str | None = None

    class Config:
        extra = "allow"


class ResultCountry(BaseModel):
    code: str | None = None
    label: str | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("provenance"):
            data["provenance"] = PidProvenance()
        return data

    class Config:
        extra = "allow"


# Updated CitationImpact to match documentation
class CitationImpact(BaseModel):
    influence: float | None = None
    influenceClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    citationCount: int | None = None
    citationClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    popularity: float | None = None
    popularityClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    impulse: float | None = None
    impulseClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None

    class Config:
        extra = "allow"


class UsageCounts(BaseModel):
    downloads: str | None = None
    views: str | None = None

    @model_validator(mode="before")
    @classmethod
    def text_fix(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("downloads") or not isinstance(data["downloads"], str):
                data["downloads"] = "0"
            if not data.get("views") or not isinstance(data["views"], str):
                data["views"] = "0"
        return data

    class Config:
        extra = "allow"


class Indicator(BaseModel):
    citationImpact: CitationImpact | None = None
    usageCounts: UsageCounts | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("citationImpact"):
                data["citationImpact"] = CitationImpact()
            if not data.get("usageCounts"):
                data["usageCounts"] = UsageCounts()
        return data

    class Config:
        extra = "allow"


# Updated AccessRight model to include openAccessRoute
class AccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    openAccessRoute: OpenAccessRouteType | None = None
    scheme: str | None = None

    class Config:
        extra = "allow"


class ArticleProcessingCharge(BaseModel):
    amount: str | None = None
    currency: str | None = None

    class Config:
        extra = "allow"


class ResultPid(BaseModel):
    scheme: str | None = None
    value: str | None = None

    class Config:
        extra = "allow"


class License(BaseModel):
    code: str | None = None
    label: str | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("provenance"):
            data["provenance"] = PidProvenance()
        return data

    class Config:
        extra = "allow"


class Instance(BaseModel):
    accessRight: AccessRight | None = None
    alternateIdentifier: list[dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: ArticleProcessingCharge | None = None
    license: License | None = None
    pid: list[ResultPid] = Field(default_factory=list)
    publicationDate: str | None = None
    refereed: RefereedType | None = None
    type: str | None = None
    urls: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("accessRight"):
                data["accessRight"] = AccessRight()
            if not data.get("articleProcessingCharge"):
                data["articleProcessingCharge"] = ArticleProcessingCharge()
            if not data.get("license"):
                data["license"] = License()
            if not data.get("pid"):
                data["pid"] = [ResultPid()]

        return data

    class Config:
        extra = "allow"


class Language(BaseModel):
    code: str | None = None
    label: str | None = None

    class Config:
        extra = "allow"


class Subject(BaseModel):
    subject: dict[str, str] | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("subject"):
                data["subject"] = {}
            if not data.get("provenance"):
                data["provenance"] = PidProvenance()
        return data

    class Config:
        extra = "allow"


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

    class Config:
        extra = "allow"


# GeoLocation for Data
class GeoLocation(BaseModel):
    box: str | None = None
    place: str | None = None
    point: str | None = None

    class Config:
        extra = "allow"


# Update main ResearchProduct model
class ResearchProduct(BaseEntity):
    type: ResearchProductType | None = None
    originalId: list[str] = Field(default_factory=list)
    mainTitle: str | None = None
    subTitle: str | None = None
    author: list[Author] = Field(default_factory=list)
    bestAccessRight: BestAccessRight | None = None
    contributors: list[str] = Field(default_factory=list)
    country: list[ResultCountry] = Field(default_factory=list)
    coverages: list[str] = Field(default_factory=list)
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
    formats: list[str] = Field(default_factory=list)
    subjects: list[Subject] = Field(default_factory=list)
    isGreen: bool | None = None
    openAccessColor: str | None = None
    isInDiamondJournal: bool | None = None
    publiclyFunded: bool | None = None

    # for publications
    container: Container | None = None
    # for datasets
    size: str | None = None
    version: str | None = None
    geolocations: list[GeoLocation] = Field(default_factory=list)
    # for software
    documentationUrls: list[str] = Field(default_factory=list)
    codeRepositoryUrl: str | None = None
    programmingLanguage: str | None = None
    # for other research products
    contactPeople: list[str] = Field(default_factory=list)
    contactGroups: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if not isinstance(data, dict):
            return data

        # Handle optional object fields
        obj_fields = {
            "bestAccessRight": BestAccessRight,
            "indicators": Indicator,
            "language": Language,
            "container": Container,
        }

        data["publiclyFunded"] = bool(
            data.get("publicyFunded") == "True"
            or (
                isinstance(data.get("publiclyFunded"), bool)
                and data.get("publiclyFunded")
            )
        )

        for field, classtype in obj_fields.items():
            if data.get(field) is None:
                data[field] = classtype()

        obj_list_fields = {
            "bestAccessRight": BestAccessRight,
            "indicators": Indicator,
            "language": Language,
            "author": Author,
            "country": ResultCountry,
            "instance": Instance,
            "pid": ResultPid,
            "subjects": Subject,
            "geolocation": GeoLocation,
        }
        for field, classtype in obj_list_fields.items():
            if not data.get(field) or data.get(field) is None or data.get(field) == []:
                data[field] = [classtype()]
        return data

    class Config:
        extra = "allow"


# Define the specific response type for ResearchProduct results
ResearchProductResponse = ApiResponse[ResearchProduct]
