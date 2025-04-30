# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\__init__.py
#
# ------------------------------------------------------

"""Pydantic models for OpenAIRE API entities and responses."""

# Combined & Sorted Imports
from .base import ApiResponse, BaseEntity, Header
from .data_source import ControlledField, DataSource, DataSourceResponse
from .organization import Country, Organization, OrganizationPid, OrganizationResponse
from .project import (
    Funding,
    FundingStream,
    Grant,
    H2020Programme,
    Project,
    ProjectResponse,
)
from .research_product import ResearchProduct, ResearchProductResponse
from .scholix import (
    ScholixCreator,
    ScholixEntity,
    ScholixIdentifier,
    ScholixLinkProvider,
    ScholixPublisher,
    ScholixRelationship,
    ScholixResponse,
)

__all__ = [
    "ApiResponse",
    "BaseEntity",
    "ControlledField",
    "Country",
    "DataSource",
    "DataSourceResponse",
    "Funding",
    "FundingStream",
    "Grant",
    "H2020Programme",
    "Header",
    "Organization",
    "OrganizationPid",
    "OrganizationResponse",
    "Project",
    "ProjectResponse",
    "ResearchProduct",
    "ResearchProductResponse",
    "ScholixCreator",
    "ScholixEntity",
    "ScholixEntityType",
    "ScholixIdentifier",
    "ScholixLinkProvider",
    "ScholixPublisher",
    "ScholixRelationship",
    "ScholixResponse",
]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\base.py
#
# ------------------------------------------------------

"""Base Pydantic models for API entities and responses."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel,  HttpUrl, field_validator

# Generic type for the entity contained within the response results
EntityType = TypeVar("EntityType", bound="BaseEntity")


class Header(BaseModel):
    """Model for the standard API response header."""

    status: str | None = None
    code: str | None = None
    message: str | None = None
    # total and count are often strings in the API response, needs validation/coercion
    queryTime: int | None = None
    numFound: int | None = None
    # next/prev can be full URLs or just the cursor string
    nextCursor: str | HttpUrl | None = None
    pageSize: int | None = None

    @field_validator("queryTime", "numFound", "pageSize", mode="before")
    @classmethod
    def coerce_str_to_int(cls, v: Any) -> int | None:
        """Coerce string representations of numbers to integers."""
        if isinstance(v, str):
            try:
                return int(v)
            except (ValueError, TypeError):
                return None  # Or raise a validation error if preferred
        return v

    model_config = dict(extra="allow")


class BaseEntity(BaseModel):
    """Base model for all OpenAIRE entities (like publication, project, etc.)."""

    # Common identifier across most entities
    id: str

    model_config = dict(extra="allow")


class ApiResponse(BaseModel, Generic[EntityType]):
    """Generic base model for standard API list responses."""

    header: Header
    # Results can sometimes be null/absent, sometimes an empty list
    results: list[EntityType] | None = None

    @field_validator("results", mode="before")
    @classmethod
    def handle_null_results(cls, v: Any) -> list[EntityType] | None:
        """Ensure 'results' is a list or None, handling potential null values from API."""
        if v is None:
            return None  # Explicitly return None if API sends null
        if isinstance(v, dict) and "result" in v:
            # API often wraps single result in {"result": {...}} or {"result": [{...}]}
            single_result = v["result"]
            if isinstance(single_result, list):
                return single_result
            if isinstance(single_result, dict):
                return [single_result]  # Wrap single dict in a list
        if isinstance(v, list):
            return v  # Already a list
        # If it's neither None, nor the expected dict wrapper, nor a list, handle appropriately
        # Option: Return empty list, None, or raise ValueError depending on strictness desired
        return []  # Default to empty list for unexpected formats

    model_config = dict(extra="allow")


# Example of a specific response type (for illustration)
# class ResearchProductResponse(ApiResponse[ResearchProduct]):
#     pass



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\data_source.py
#
# ------------------------------------------------------

# https://graph.openaire.eu/docs/data-model/entities/data-source
from typing import Literal

from pydantic import BaseModel, Field

from .base import ApiResponse, BaseEntity

# Type literals for restricted values
AccessRightType = Literal["open", "restricted", "closed"]
DatabaseRestrictionType = Literal["feeRequired", "registration", "other"]


# Base classes for controlled fields
class ControlledField(BaseModel):
    """Represents a controlled vocabulary field with scheme and value."""
    scheme: str | None = None
    value: str | None = None

    model_config = dict(extra="allow")


# Main DataSource model
class DataSource(BaseEntity):
    """Model representing an OpenAIRE Data Source entity."""

    originalIds: list[str] | None = Field(default_factory=list)
    pids: list[ControlledField] | None = Field(default_factory=list)
    type: ControlledField | None = None
    openaireCompatibility: str | None = None
    officialName: str | None = None
    englishName: str | None = None
    websiteUrl: str | None = None
    logoUrl: str | None = None
    dateOfValidation: str | None = None
    description: str | None = None
    subjects: list[str] | None = Field(default_factory=list)
    languages: list[str] | None = Field(default_factory=list)
    contentTypes: list[str] | None = Field(default_factory=list)
    releaseStartDate: str | None = None
    releaseEndDate: str | None = None
    accessRights: AccessRightType | None = None
    uploadRights: AccessRightType | None = None
    databaseAccessRestriction: DatabaseRestrictionType | None = None
    dataUploadRestriction: str | None = None
    versioning: bool | None = None
    citationGuidelineUrl: str | None = None
    pidSystems: str | None = None
    certificates: str | None = None
    policies: list[str] | None = Field(default_factory=list)
    missionStatementUrl: str | None = None


# Define the specific response type for data sources
DataSourceResponse = ApiResponse[DataSource]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\organization.py
#
# ------------------------------------------------------

# https://graph.openaire.eu/docs/data-model/entities/organization

from pydantic import BaseModel, Field

# Import base classes
from .base import ApiResponse, BaseEntity


class Country(BaseModel):
    """Represents the country associated with an organization."""

    code: str | None = None
    label: str | None = None

    model_config = dict(extra="allow")


class OrganizationPid(BaseModel):
    """Represents a persistent identifier for an organization."""

    scheme: str | None = None
    value: str | None = None

    model_config = dict(extra="allow")


class Organization(BaseEntity):
    """Model representing an OpenAIRE Organization entity."""

    # id is inherited from BaseEntity
    legalShortName: str | None = None
    legalName: str | None = None
    alternativeNames: list[str] | None = Field(default_factory=list)
    websiteUrl: str | None = None
    country: Country | None = None
    pids: list[OrganizationPid] | None = Field(default_factory=list)

    model_config = dict(extra="allow")


# Define the specific response type for organizations
OrganizationResponse = ApiResponse[Organization]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\project.py
#
# ------------------------------------------------------

# https://graph.openaire.eu/docs/data-model/entities/project

from pydantic import BaseModel, Field

# Import base classes
from .base import ApiResponse, BaseEntity


class FundingStream(BaseModel):
    """Details about the funding stream for a project."""

    description: str | None = None
    id: str | None = None
    model_config = dict(extra="allow")


class Funding(BaseModel):
    """Details about the funding source and stream."""

    fundingStream: FundingStream | None = None
    jurisdiction: str | None = None
    name: str | None = None
    shortName: str | None = None
    model_config = dict(extra="allow")



class Grant(BaseModel):
    """Details about the grant amounts."""

    currency: str | None = None
    fundedAmount: float | None = None
    totalCost: float | None = None
    model_config = dict(extra="allow")


class H2020Programme(BaseModel):
    """Details about the H2020 programme, if applicable."""

    code: str | None = None
    description: str | None = None
    model_config = dict(extra="allow")

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

    model_config = dict(extra="allow")


# Define the specific response type for projects
ProjectResponse = ApiResponse[Project]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\research_product.py
#
# ------------------------------------------------------

# https://graph.openaire.eu/docs/data-model/entities/research-product

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from .base import ApiResponse, BaseEntity

"""
This module contains the Pydantic models for parsing & validation OpenAIRE API responses.
The models are designed to be used with the OpenAIRE Graph API and are structured to match
the expected JSON response format for Research Products.
"""

OpenAccessRouteType = Literal["gold", "green", "hybrid", "bronze"]
RefereedType = Literal["peerReviewed", "nonPeerReviewed", "UNKNOWN"]
ResearchProductType = Literal["publication", "dataset", "software", "other"]


# Sub-models for nested structures
class PidIdentifier(BaseModel):
    scheme: str | None = None
    value: str | None = None

    model_config = dict(extra="allow")


class PidProvenance(BaseModel):
    provenance: str | None = None
    trust: float | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


class BestAccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    scheme: str | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


class CitationImpact(BaseModel):
    influence: float | None = None
    influenceClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    citationCount: int | None = None
    citationClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    popularity: float | None = None
    popularityClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    impulse: float | None = None
    impulseClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


class AccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    openAccessRoute: OpenAccessRouteType | None = None
    scheme: str | None = None

    model_config = dict(extra="allow")


class ArticleProcessingCharge(BaseModel):
    amount: str | None = None
    currency: str | None = None

    model_config = dict(extra="allow")


class ResultPid(BaseModel):
    scheme: str | None = None
    value: str | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


class Language(BaseModel):
    code: str | None = None
    label: str | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


# GeoLocation for Data
class GeoLocation(BaseModel):
    box: str | None = None
    place: str | None = None
    point: str | None = None

    model_config = dict(extra="allow")


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

    model_config = dict(extra="allow")


# Define the specific response type for ResearchProduct results
ResearchProductResponse = ApiResponse[ResearchProduct]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\models\scholix.py
#
# ------------------------------------------------------

# https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, HttpUrl

# Type Aliases & Literals
ScholixEntityTypeName = Literal["publication", "dataset", "software", "other"]
ScholixRelationshipNameValue = Literal[
    "IsSupplementTo",
    "IsSupplementedBy",
    "References",
    "IsReferencedBy",
    "IsRelatedTo",
]


class ScholixIdentifier(BaseModel):
    ID: str
    IDScheme: str
    IDURL: HttpUrl | None = None

    model_config = dict(extra="allow")


class ScholixCreator(BaseModel):
    Name: str | None = None  # Sometimes just identifier is present
    Identifier: list[ScholixIdentifier] | None = None

    model_config = dict(extra="allow")


class ScholixPublisher(BaseModel):
    Name: str
    Identifier: list[ScholixIdentifier] | None = None

    model_config = dict(extra="allow")


class ScholixEntity(BaseModel):
    Identifier: list[ScholixIdentifier]
    Type: ScholixEntityTypeName
    SubType: str | None = None
    Title: str | None = None
    Creator: list[ScholixCreator] | None = None
    PublicationDate: str | None = None  # Keep as string for flexibility
    Publisher: list[ScholixPublisher] | None = None

    model_config = dict(extra="allow")


class ScholixRelationshipType(BaseModel):
    Name: ScholixRelationshipNameValue
    SubType: str | None = None
    SubTypeSchema: HttpUrl | None = None

    model_config = dict(extra="allow")


class ScholixLinkProvider(BaseModel):
    Name: str
    Identifier: list[ScholixIdentifier] | None = None


class ScholixRelationship(BaseModel):
    LinkProvider: list[ScholixLinkProvider] | None = None
    RelationshipType: ScholixRelationshipType
    Source: ScholixEntity
    Target: ScholixEntity
    LinkPublicationDate: datetime | None = Field(
        default=None, description="Date the link was published."
    )
    LicenseURL: HttpUrl | None = None
    # HarvestDate appears in examples but not the schema doc?
    HarvestDate: Annotated[str | None, Field(alias="HarvestDate")] = None

    model_config = dict(extra="allow")


class ScholixResponse(BaseModel):
    """Response structure for the Scholexplorer Links endpoint."""

    currentPage: int = Field(..., description="The current page number (0-indexed).")
    totalLinks: int = Field(
        ..., description="Total number of links matching the query."
    )
    totalPages: int = Field(..., description="Total number of pages available.")
    result: list[ScholixRelationship] = Field(
        ..., description="List of Scholix relationship links."
    )

    model_config = dict(extra="allow")



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\__init__.py
#
# ------------------------------------------------------

"""AIREloom: A Python client for the OpenAIRE Graph API."""

__version__ = "0.1.0"  # Placeholder

# Import Exceptions
from .exceptions import (
    AireloomError,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

# Re-export key models from the models subpackage
from .models import (
    ApiResponse,
    BaseEntity,
    DataSource,
    Header,
    Organization,
    Project,
    ResearchProduct,
    ScholixRelationship,
)

# Import main session class
from .session import AireloomSession

__all__ = [
    "AireloomSession",
    "AireloomError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ApiResponse",
    "BaseEntity",
    "Community",
    "DataSource",
    "Header",
    "Organization",
    "Project",
    "Relationship",
    "ResearchProduct",
    "ScholixRelationship",
]



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\auth.py
#
# ------------------------------------------------------

import asyncio
from typing import Protocol

import httpx

from .exceptions import AuthError, ConfigurationError
from .log_config import logger


class AuthStrategy(Protocol):
    """Protocol defining the interface for authentication strategies."""

    async def async_authenticate(self, request: httpx.Request) -> None:
        """
        Asynchronously modifies the request to add authentication information.

        Args:
            request: The httpx.Request object to modify.

        Raises:
            AuthError: If authentication fails (e.g., token fetching).
            ConfigurationError: If required configuration for the strategy is missing.
        """
        ...


class NoAuth:
    """Implements the AuthStrategy protocol for requests requiring no authentication."""

    async def async_authenticate(self, request: httpx.Request) -> None:
        """Does nothing as no authentication is needed."""
        logger.trace("Using NoAuth strategy.")


class StaticTokenAuth:
    """
    Implements AuthStrategy using a static Bearer token (e.g., personal API token).
    """

    def __init__(self, token: str | None):
        if not token:
            # If token is expected but not provided, raise config error
            raise ConfigurationError("StaticTokenAuth requires a non-empty 'token'.")
        self._token = token
        logger.debug("StaticTokenAuth initialized.")

    async def async_authenticate(self, request: httpx.Request) -> None:
        """Adds the static Authorization: Bearer token header."""
        logger.trace("Authenticating request using StaticTokenAuth.")
        request.headers["Authorization"] = f"Bearer {self._token}"


class ClientCredentialsAuth:
    """
    Implements AuthStrategy using OAuth2 Client Credentials Grant Flow.

    Fetches a Bearer token using client_id and client_secret via Basic Auth.
    """

    def __init__(
        self, client_id: str | None, client_secret: str | None, token_url: str | None
    ):
        if not all([client_id, client_secret, token_url]):
            raise ConfigurationError(
                "ClientCredentialsAuth requires 'client_id', 'client_secret', and 'token_url'."
            )
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = token_url
        self._access_token: str | None = None
        self._token_client: httpx.AsyncClient | None = None
        self._fetch_lock = asyncio.Lock()  # Prevent concurrent token fetches
        logger.debug("ClientCredentialsAuth initialized.")

    async def _get_token_client(self) -> httpx.AsyncClient:
        """Initializes and returns the internal httpx client for token fetching."""
        if self._token_client is None:
            # Create a simple client for token fetching, no complex retries needed here usually
            self._token_client = httpx.AsyncClient(
                timeout=15.0
            )  # Shorter timeout for token request
        return self._token_client

    async def _fetch_access_token(self) -> str:
        """Fetches a new access token using client credentials."""
        async with self._fetch_lock:
            # Double-check if token was fetched while waiting for the lock
            if self._access_token:
                return self._access_token

            logger.info(f"Fetching new access token from {self._token_url}")
            client = await self._get_token_client()
            try:
                response = await client.post(
                    url=self._token_url,
                    auth=httpx.BasicAuth(
                        username=self._client_id, password=self._client_secret
                    ),
                    data={"grant_type": "client_credentials"},
                )
                response.raise_for_status()  # Raise HTTPStatusError for bad responses (4xx or 5xx)
                token_data = response.json()
                access_token = token_data.get("access_token")
                if not access_token:
                    raise AuthError("Access token not found in token response.")
                # TODO: Handle token expiry ('expires_in') for future automatic refresh
                # expires_in = token_data.get("expires_in")
                logger.info("Successfully fetched new access token.")
                self._access_token = access_token
                return self._access_token
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error fetching token: {e.response.status_code} - {e.response.text}"
                )
                raise AuthError(
                    f"Failed to fetch access token: {e.response.status_code} - {e.response.text}"
                ) from e
            except (httpx.RequestError, Exception) as e:
                logger.error(f"Error fetching token: {e}")
                raise AuthError(f"Failed to fetch access token: {e}") from e

    async def async_authenticate(self, request: httpx.Request) -> None:
        """Ensures a valid token is fetched and adds the Authorization header."""
        logger.trace("Authenticating request using ClientCredentialsAuth.")
        if not self._access_token:
            # Fetch token if not already available (first time or after expiry if implemented)
            await self._fetch_access_token()

        if not self._access_token:
            # Should not happen if fetch was successful, but check anyway
            raise AuthError("Authentication failed: Could not obtain access token.")

        request.headers["Authorization"] = f"Bearer {self._access_token}"

    async def close(self) -> None:
        """Closes the internal HTTP client used for token fetching."""
        if self._token_client:
            await self._token_client.aclose()
            self._token_client = None
            logger.debug("ClientCredentialsAuth internal client closed.")



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\client.py
#
# ------------------------------------------------------

import ssl
from collections.abc import Mapping
from typing import Any, Self

import certifi
import httpx
import tenacity
from tenacity import (
    AsyncRetrying,
    RetryError,
    stop_after_attempt,
    wait_exponential,
)

from .auth import (
    AuthStrategy,
    ClientCredentialsAuth,
    NoAuth,
    StaticTokenAuth,
)
from .config import ApiSettings, get_settings
from .constants import (
    OPENAIRE_GRAPH_API_BASE_URL,
)
from .exceptions import (
    AireloomError,
    APIError,
    AuthError,
    NetworkError,
    RateLimitError,
    TimeoutError,
    # Add ConfigurationError if needed, though not directly used here
)
from .log_config import logger
from .types import RequestData


class AireloomClient:
    """Asynchronous HTTP client for interacting with OpenAIRE APIs."""

    DEFAULT_RETRYABLE_STATUS_CODES = frozenset([429, 500, 502, 503, 504])

    def __init__(
        self,
        settings: ApiSettings | None = None,
        auth_strategy: AuthStrategy | None = None,
        *,
        # Allow direct override for testing/specific cases, but prefer settings
        api_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = OPENAIRE_GRAPH_API_BASE_URL,  # Default to Graph API
        http_client: httpx.AsyncClient | None = None,
        retryable_status_codes: frozenset[int] = DEFAULT_RETRYABLE_STATUS_CODES,
    ):
        """
        Initializes the AireloomClient.

        Authentication is determined automatically based on settings unless an
        explicit `auth_strategy` is provided.

        Order of precedence for automatic auth determination:
        1. Client Credentials (if client_id & client_secret are configured)
        2. Static Token (if api_token is configured)
        3. No Authentication

        Args:
            settings: Optional ApiSettings instance. If None, loads global settings.
            auth_strategy: Optional explicit authentication strategy instance.
            api_token: Optional static API token (overrides settings if provided).
            client_id: Optional client ID (overrides settings if provided).
            client_secret: Optional client secret (overrides settings if provided).
            base_url: The base URL for the API (defaults to Graph API).
            http_client: Optional pre-configured httpx.AsyncClient instance.
            retryable_status_codes: Set of HTTP status codes to retry on.
        """
        self._settings = settings or get_settings()
        self._base_url = base_url.rstrip("/")
        self._retryable_status_codes = retryable_status_codes

        self._auth_strategy: AuthStrategy
        if auth_strategy:
            logger.info("Using explicitly provided authentication strategy.")
            self._auth_strategy = auth_strategy
        else:
            # Use overrides if provided, otherwise use settings
            _client_id = client_id or self._settings.openaire_client_id
            _client_secret = client_secret or self._settings.openaire_client_secret
            _api_token = api_token or self._settings.openaire_api_token
            _token_url = self._settings.openaire_token_url

            if _client_id and _client_secret:
                logger.info("Using Client Credentials authentication.")
                self._auth_strategy = ClientCredentialsAuth(
                    client_id=_client_id,
                    client_secret=_client_secret,
                    token_url=_token_url,
                )
            elif _api_token:
                logger.info("Using Static Token authentication.")
                self._auth_strategy = StaticTokenAuth(token=_api_token)
            else:
                logger.info("No authentication credentials found, using NoAuth.")
                self._auth_strategy = NoAuth()

        self._should_close_client = http_client is None  # Close only if we created it
        self._http_client = http_client or self._create_default_http_client()

        logger.debug("AireloomClient initialized.")

    def _create_default_http_client(self) -> httpx.AsyncClient:
        """Creates a default httpx.AsyncClient with configured settings."""
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            verify_ssl = ssl_context
            logger.debug("Using certifi SSL context.")
        except Exception:
            verify_ssl = True
            logger.warning(
                "certifi not found or failed to load. Using default SSL verification."
            )

        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._settings.request_timeout,
            verify=verify_ssl,
            headers={"User-Agent": self._settings.user_agent},
            # Add transport/proxy settings from config if needed later
        )

    async def _execute_single_request(
        self, request_data: RequestData
    ) -> httpx.Response:
        """Executes a single HTTP request attempt."""
        request = request_data.build_request()
        try:
            # Apply authentication just before sending
            await self._auth_strategy.async_authenticate(request)

            logger.debug(f"Sending request: {request.method} {request.url}")
            logger.trace(f"Request Headers: {request.headers}")
            if request.content:
                # Avoid logging potentially large/sensitive bodies unless debugging heavily
                logger.trace(f"Request Body: {request.content.decode()}")

            response = await self._http_client.send(request)

            logger.debug(f"Received response: {response.status_code} for {request.url}")
            logger.trace(f"Response Headers: {response.headers}")
            # Optionally log response body excerpts for debugging
            # logger.trace(f"Response Body Excerpt: {response.text[:200]}")

            # Raise APIError for non-success status codes *after* logging
            if response.status_code >= 400:
                if response.status_code == 429:
                    raise RateLimitError("API rate limit exceeded.", response=response)
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    response=response,
                )
            return response

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Request failed with status {e.response.status_code}: {e.request.url}"
            )
            if e.response.status_code == 429:
                raise RateLimitError("API rate limit exceeded.", response=e.response, request=e.request) from e
            raise APIError(
                f"API request failed with status {e.response.status_code}",
                response=e.response,
                request=e.request,
            ) from e
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {request.url}")
            raise TimeoutError("Request timed out", request=request) from e
        except httpx.NetworkError as e:
            logger.error(f"Network error occurred: {request.url}")
            raise NetworkError("Network error occurred", request=request) from e
        except Exception as e:
            logger.exception(f"Unexpected error during single request execution to {request.url}: {e}")
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(f"An unexpected error occurred during request execution: {e}", request=request) from e

    def _should_retry_request(self, retry_state: tenacity.RetryCallState) -> bool:
        """Predicate for tenacity: should we retry this request?"""
        outcome = retry_state.outcome
        if not outcome: # Should not happen with reraise=True, but defensive check
            return False

        if outcome.failed:
            exc = outcome.exception()
            url = "N/A"
            request = getattr(exc, 'request', None)
            if request:
                url = getattr(request, 'url', 'N/A')

            if isinstance(exc, (TimeoutError, NetworkError, RateLimitError)):
                logger.warning(f"Retrying due to {type(exc).__name__} for {url}")
                return True
            if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
                logger.warning(f"Retrying due to {type(exc).__name__} (httpx) for {url}")
                return True

            status_code: int | None = None
            if isinstance(exc, APIError):
                if exc.response is not None:
                    status_code = exc.response.status_code
            elif isinstance(exc, httpx.HTTPStatusError):
                status_code = exc.response.status_code

            if status_code is not None and status_code in self._retryable_status_codes:
                logger.warning(
                    f"Retrying due to status code {status_code} for {url}"
                )
                return True

        return False

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        data: Mapping[str, Any] | None = None,
        base_url_override: str | None = None,
    ) -> httpx.Response:
        """Makes an HTTP request with configured retries for transient errors."""
        base_url = (base_url_override or self._base_url).rstrip("/")
        full_url = f"{base_url}/{path.lstrip('/')}"

        request_data = RequestData(
            method=method,
            url=full_url,
            params=params,
            json_data=json_data,
            data=data,
        )

        # Apply authentication *before* retry loop setup, fail fast on auth issues
        try:
            # Build a temporary request just for authentication purposes
            temp_request = request_data.build_request()
            await self._auth_strategy.async_authenticate(temp_request)
            # Update request_data headers if auth added/modified them
            request_data.headers = temp_request.headers
        except AuthError as e:
            logger.error(f"Authentication failed before request: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during pre-request authentication: {e}")
            raise AireloomError(f"Unexpected authentication error: {e}") from e

        # Prepare retry strategy
        retry_strategy = AsyncRetrying(
            stop=stop_after_attempt(self._settings.max_retries + 1),
            wait=wait_exponential(
                multiplier=self._settings.backoff_factor, min=0.1, max=10
            ),
            retry=self._should_retry_request,
            reraise=True, # Reraise the last exception if all retries fail
        )

        try:
            response = await retry_strategy(self._execute_single_request, request_data)
            return response

        except AuthError as e:
            logger.error(f"Authentication error during request execution: {e}")
            raise e
        except TimeoutError as e:
            logger.warning(f"Request timed out after retries: {e.request.url if e.request else 'N/A'}")
            raise e
        except NetworkError as e:
            logger.warning(f"Network error after retries: {e.request.url if e.request else 'N/A'}")
            raise e

        except RateLimitError as e:
            logger.warning(f"Rate limit error after retries: {e.request.url if e.request else 'N/A'}")
            raise e

        except APIError as e:
            logger.warning(
                f"API error {e.response.status_code if e.response else 'N/A'} after retries: {e.request.url if e.request else 'N/A'}"
            )
            raise e

        except httpx.TimeoutException as e:
            logger.warning(f"Request timed out after retries (httpx): {getattr(e.request, 'url', 'N/A')}")
            raise TimeoutError("Request timed out", request=e.request) from e

        except httpx.NetworkError as e:
            logger.warning(f"Network error after retries (httpx): {getattr(e.request, 'url', 'N/A')}")
            raise NetworkError("Connection failed", request=e.request) from e

        except httpx.HTTPStatusError as e:
            logger.warning(
                f"HTTP error after retries (httpx): Status {e.response.status_code}, URL: {e.request.url}"
            )
            #
            if e.response.status_code == 429:
                raise RateLimitError("API rate limit exceeded.", response=e.response, request=e.request) from e
            else:
                raise APIError(f"API request failed with status {e.response.status_code}", response=e.response, request=e.request) from e

        except RetryError as e:
            logger.error(f"Request failed after multiple retries: {e}")
            raise AireloomError("Request failed after multiple retries") from e

        except Exception as e:
            logger.exception(f"Unexpected error during request processing: {e}")
            request_info = getattr(e, "request", None)
            if not isinstance(request_info, (httpx.Request, type(None))):
                request_info = None
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(f"An unexpected error occurred: {e}", request=request_info) from e

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        data: Mapping[str, Any] | None = None,
        expected_model: type[Any] | None = None,  # For potential future validation
        base_url_override: str | None = None,
    ) -> httpx.Response | Any:
        """
        Performs an asynchronous HTTP request to the specified API path with retries.

        Args:
            method: HTTP method (e.g., "GET", "POST").
            path: API endpoint path (relative to base_url).
            params: URL query parameters.
            json_data: Data to send as JSON in the request body.
            data: Data to send form-encoded in the request body.
            expected_model: Pydantic model to validate the response against (optional).
            base_url_override: Use a different base URL for this specific request.

        Returns:
            The httpx.Response object, or a parsed Pydantic model if expected_model is provided.

        Raises:
            APIError: If the API returns an error status code (4xx, 5xx) after retries.
            RateLimitError: If the API returns a 429 status code after retries.
            TimeoutError: If the request times out after retries.
            NetworkError: If a network-level error occurs.
            AuthError: If authentication fails.
            AireloomError: For other unexpected client-side errors.
            ValidationError: If response parsing/validation fails (when using expected_model).
        """
        response = await self._request_with_retry(
            method=method,
            path=path,
            params=params,
            json_data=json_data,
            data=data,
            base_url_override=base_url_override,
        )

        if expected_model:
            # Placeholder for future response validation using the model
            # try:
            #     return expected_model.model_validate(response.json())
            # except Exception as e:
            #     raise ValidationError(f"Failed to parse/validate response: {e}", response=response) from e
            logger.warning("Response model validation not yet implemented.")
            return response  # Return raw response for now
        return response

    async def aclose(self) -> None:
        """Closes the underlying HTTP client and any auth-specific clients."""
        if self._should_close_client and self._http_client:
            await self._http_client.aclose()
            logger.info("AireloomClient internal HTTP client closed.")
        # Close auth strategy client if it has a close method
        if hasattr(self._auth_strategy, "close") and callable(
            self._auth_strategy.close
        ):
            await self._auth_strategy.close()  # type: ignore

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\config.py
#
# ------------------------------------------------------

# aireloom/config.py
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Assuming constants.py defines OPENAIRE_TOKEN_URL
from .constants import DEFAULT_USER_AGENT, REGISTERED_SERVICE_API_TOKEN_URL


class ApiSettings(BaseSettings):
    """
    Manages user-configurable settings for the AIREloom client,
    primarily loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "secrets.env"),  # Look in both .env and secrets.env
        env_file_encoding="utf-8",
        # Environment variables should be prefixed, e.g., AIRELOOM_OPENAIRE_API_TOKEN
        env_prefix="AIRELOOM_",
        extra="ignore",  # Ignore extra fields found in environment
        case_sensitive=False,  # Allow AIRELOOM_openaire_api_token etc.
    )

    # --- Client Behavior Settings ---
    request_timeout: float = Field(
        default=30.0, description="Default request timeout in seconds"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for failed requests"
    )
    backoff_factor: float = Field(
        default=0.5, description="Backoff factor for retries (seconds)"
    )
    user_agent: str = Field(
        default=DEFAULT_USER_AGENT,  # Get default from constants
        description="User-Agent header for requests",
    )

    # --- Authentication Settings ---
    # Option 1: Static API Token
    openaire_api_token: str | None = Field(
        default=None, description="Static OpenAIRE API Token (optional)"
    )

    # Option 2: Client Credentials for OAuth2 Token Fetching
    openaire_client_id: str | None = Field(
        default=None,
        description="OpenAIRE Client ID for OAuth2 (required for client_credentials)",
    )
    openaire_client_secret: str | None = Field(
        default=None,
        description="OpenAIRE Client Secret for OAuth2 (required for client_credentials)",
    )
    # Token URL is fetched from constants, but could be overridden via env if needed
    openaire_token_url: str = Field(
        default=REGISTERED_SERVICE_API_TOKEN_URL,
        description="OAuth2 Token Endpoint URL",
    )


# Create a single, cached instance of settings
@lru_cache
def get_settings() -> ApiSettings:
    """
    Provides access to the application settings.

    Settings are loaded from environment variables (prefixed with 'AIRELOOM_')
    or .env/secrets.env files. The instance is cached for performance.

    Returns:
        ApiSettings: The application settings instance.
    """
    # Check if running in a test environment and potentially load test-specific env
    # For now, relies on standard .env/.secrets.env loading
    return ApiSettings()



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\constants.py
#
# ------------------------------------------------------

"""Constants used throughout the Aireloom library."""

from enum import Enum
from typing import Literal

# Base URLs
OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v1"
OPENAIRE_SCHOLIX_API_BASE_URL = "https://api.scholexplorer.openaire.eu/v3"
REGISTERED_SERVICE_API_TOKEN_URL = "https://aai.openaire.eu/oidc/token"
PERSONAL_API_TOKEN_URL: str = (
    "https://services.openaire.eu/uoa-user-management/api/users/getAccessToken"
)

# Default settings
DEFAULT_TIMEOUT: int = 30  # Default request timeout in seconds
DEFAULT_RETRIES: int = 2  # Default number of retries on transient errors
DEFAULT_PAGE_SIZE: int = 20  # Default number of results per page for standard search
ITERATE_PAGE_SIZE: int = (
    100  # Default number of results per page for iteration (using cursor)
)

# --- API Parameter Enums/Literals --- #


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


EntityType = Literal[
    "publication",
    "dataset", # Added dataset based on typical OpenAIRE entities
    "software", # Added software
    "project",
    "organization",
    "datasource",
    "other",     # For 'other research products'
]


# TODO: Define Enums or Literals based on API docs for:
# - Sortable Fields (per entity) - Likely needs specific definitions per entity type
# - Filter Keys (per entity)
# - Open Access Routes ("gold", "green", etc.)
# - Funder Identifiers (e.g. "ec")
# - Country Codes (ISO 3166-1 alpha-2)
# - etc.

AIRELOOM_VERSION: str = "0.1.0"
DEFAULT_USER_AGENT: str = f"aireloom/{AIRELOOM_VERSION}"
CLIENT_HEADERS: dict[str, str] = {
    "accept": "application/json",
    "User-Agent": DEFAULT_USER_AGENT,
}



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\endpoints.py
#
# ------------------------------------------------------

"""Defines API endpoint paths and validation details."""

# Base URLs
GRAPH_API_BASE_URL = "https://api.graph.openaire.eu/v1/"
SCHOLIX_API_BASE_URL = (
    "https://api-beta.scholexplorer.openaire.eu/v3/"  # Scholexplorer v3 (beta)
)

# --- Graph API Endpoint Paths ---
RESEARCH_PRODUCTS = "researchProducts"
ORGANIZATIONS = "organizations"
DATA_SOURCES = "dataSources" # Corrected casing
PROJECTS = "projects"
SCHOLIX = "Links"  # Renamed for Scholexplorer

# Basic definition structure: {path: {'filters': dict(), 'sort': dict()}}
ENDPOINT_DEFINITIONS = {
    RESEARCH_PRODUCTS: {
        "filters": { # Map filter name to its definition (type, etc.)
            "search": {"type": "str"},
            "mainTitle": {"type": "str"},
            "description": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "originalId": {"type": "str"},
            "type": {"type": "str"}, # Could be Literal/Enum later
            "fromPublicationDate": {"type": "date"},
            "toPublicationDate": {"type": "date"},
            "subjects": {"type": "str"}, # Potentially list?
            "countryCode": {"type": "str"},
            "authorFullName": {"type": "str"},
            "authorOrcid": {"type": "str"},
            "publisher": {"type": "str"},
            "bestOpenAccessRightLabel": {"type": "str"},
            "influenceClass": {"type": "str"},
            "impulseClass": {"type": "str"},
            "popularityClass": {"type": "str"},
            "citationCountClass": {"type": "str"},
            "instanceType": {"type": "str"},
            "sdg": {"type": "str"}, # Potentially list?
            "fos": {"type": "str"}, # Potentially list?
            "isPeerReviewed": {"type": "bool"},
            "isInDiamondJournal": {"type": "bool"},
            "isPubliclyFunded": {"type": "bool"},
            "isGreen": {"type": "bool"},
            "openAccessColor": {"type": "str"},
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relProjectId": {"type": "str"},
            "relProjectCode": {"type": "str"},
            "hasProjectRel": {"type": "bool"},
            "relProjectFundingShortName": {"type": "str"},
            "relProjectFundingStreamId": {"type": "str"},
            "relHostingDataSourceId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": { # Map sort field to its definition (currently empty)
            "relevance": {},
            "publicationDate": {},
            "dateOfCollection": {},
            "influence": {},
            "popularity": {},
            "citationCount": {},
            "impulse": {},
        },
    },
    ORGANIZATIONS: {
        "filters": {
            "search": {"type": "str"},
            "legalName": {"type": "str"},
            "legalShortName": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "countryCode": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}},
    },
    DATA_SOURCES: {
        "filters": {
            "search": {"type": "str"},
            "officialName": {"type": "str"},
            "englishName": {"type": "str"},
            "legalShortName": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "subjects": {"type": "str"}, # Potentially list?
            "dataSourceTypeName": {"type": "str"},
            "contentTypes": {"type": "str"}, # Potentially list?
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}},
    },
    PROJECTS: {
        "filters": {
            "search": {"type": "str"},
            "title": {"type": "str"},
            "keywords": {"type": "str"}, # Potentially list?
            "id": {"type": "str"},
            "code": {"type": "str"},
            "acronym": {"type": "str"},
            "callIdentifier": {"type": "str"},
            "fundingShortName": {"type": "str"},
            "fundingStreamId": {"type": "str"},
            "fromStartDate": {"type": "date"},
            "toStartDate": {"type": "date"},
            "fromEndDate": {"type": "date"},
            "toEndDate": {"type": "date"},
            "relOrganizationName": {"type": "str"},
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relOrganizationCountryCode": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}, "startDate": {}, "endDate": {}},
    },
    SCHOLIX: {  # Updated for Scholexplorer v3 /Links endpoint
        "filters": { # Types based on Scholix v3 documentation
            "sourcePid": {"type": "str"}, # Required (one of source/target Pid/Publisher/Type)
            "targetPid": {"type": "str"},
            "sourcePublisher": {"type": "str"},
            "targetPublisher": {"type": "str"},
            "sourceType": {"type": "str"}, # Enum: Publication, Dataset, Software, Other
            "targetType": {"type": "str"}, # Enum: Publication, Dataset, Software, Other
            "relation": {"type": "str"},
            "from": {"type": "date"},
            "to": {"type": "date"},
        },
        "sort": {},  # Sorting not specified for /Links endpoint
    },
}


def get_valid_filters(endpoint_path: str) -> set[str]:
    """Returns the set of valid filter keys for a given endpoint path."""
    definitions = ENDPOINT_DEFINITIONS.get(endpoint_path, {})
    filter_definitions = definitions.get("filters", {})
    return set(filter_definitions.keys())


def get_valid_sort_fields(endpoint_path: str) -> set[str]:
    """Returns the set of valid sort fields for a given endpoint path."""
    definitions = ENDPOINT_DEFINITIONS.get(endpoint_path, {})
    sort_definitions = definitions.get("sort", {})
    return set(sort_definitions.keys())



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\exceptions.py
#
# ------------------------------------------------------

"""Custom exception classes for the Aireloom library."""

import httpx


class AireloomError(Exception):
    """Base exception class for all Aireloom errors."""

    def __init__(self, 
                 message: str, 
                 *, 
                 response: httpx.Response | None = None,
                 request: httpx.Request | None = None
                 ):
        """Initializes the base exception.

        Args:
            message: The error message.
            response: Optional httpx.Response object associated with the error.
            request: Optional httpx.Request object associated with the error.
        """
        super().__init__(message)
        self.message = message
        self.response = response
        self.request = request

    def __str__(self) -> str:
        if self.response:
            # Prefer response info if available
            url_info = getattr(getattr(self.response, 'request', None), 'url', 'N/A')
            return f"{self.message} (Status: {self.response.status_code}, URL: {url_info})"
        # Check type before accessing attribute
        if isinstance(self.request, httpx.Request):
            # Fallback to request info if response is missing and request is valid
            return f"{self.message} (URL: {self.request.url})"
        # Default message if neither response nor valid request is available
        return self.message


class APIError(AireloomError):
    """Represents a generic error returned by the OpenAIRE API (non-specific 4xx/5xx)."""

    # No additional methods needed currently


class AuthenticationError(APIError):
    """Represents an authentication error (401 Unauthorized or 403 Forbidden)."""

    # No additional methods needed currently


class NotFoundError(APIError):
    """Represents a resource not found error (404 Not Found)."""

    # No additional methods needed currently


class ValidationError(AireloomError):
    """Represents a request validation error (e.g., invalid parameters, 400 Bad Request).

    Can also be raised for client-side validation issues before sending request.
    """

    # No additional methods needed currently


class RateLimitError(APIError):
    """Represents hitting the API rate limit (429 Too Many Requests)."""

    # No additional methods needed currently


class TimeoutError(AireloomError):
    """Represents a request timeout error."""

    def __init__(self, message: str, *, request: httpx.Request | None = None):
        # Timeout errors typically don't have a response, but do have the request
        super().__init__(message, response=None) # Base class handles message
        self.request = request # Store the request associated with the timeout

    def __str__(self) -> str:
        if self.request:
            return f"{self.message} (URL: {self.request.url})"
        return self.message


class NetworkError(AireloomError):
    """Represents a network connection error (e.g., DNS, connection refused)."""

    def __init__(self, message: str, *, request: httpx.Request | None = None):
        # Network errors might not have a response, but have the failing request
        super().__init__(message, response=None)
        self.request = request

    def __str__(self) -> str:
        if self.request:
            return f"{self.message} (URL: {self.request.url})"
        return self.message


class ConfigurationError(AireloomError):
    """Represents an error in the library's configuration."""

    def __init__(self, message: str):
        # Configuration errors typically don't have an HTTP response
        super().__init__(message, response=None)


class AuthError(AireloomError):
    """Raised when an authentication error occurs, e.g., fetching a token fails."""



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\log_config.py
#
# ------------------------------------------------------

# aireloom/log_config.py
import sys

from loguru import logger


def configure_logging(level: str = "INFO", sink=sys.stderr):
    """
    Configures Loguru logger.

    Removes default handlers and adds a new one with the specified level and sink.

    Args:
        level: The minimum logging level (e.g., "DEBUG", "INFO", "WARNING").
        sink: The output sink (e.g., sys.stderr, "file.log").
    """
    logger.remove()  # Remove default handler
    logger.add(
        sink,
        level=level.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    logger.info(
        f"Loguru logger configured with level={level.upper()} writing to {sink}"
    )


# Example Usage:
# from .log_config import configure_logging
# configure_logging(level="DEBUG")
# logger.debug("This is a debug message.")



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\session.py
#
# ------------------------------------------------------

"""Main user-facing session class for interacting with the OpenAIRE Graph API and Scholexplorer."""

import http
from collections.abc import AsyncIterator
from typing import Any, TypeVar

import httpx
from loguru import logger

from .auth import AuthStrategy, NoAuth
from .client import AireloomClient
from .constants import (
    DEFAULT_PAGE_SIZE,
    OPENAIRE_GRAPH_API_BASE_URL,
    OPENAIRE_SCHOLIX_API_BASE_URL,
)
from .endpoints import (
    DATA_SOURCES,
    ENDPOINT_DEFINITIONS,
    ORGANIZATIONS,
    PROJECTS,
    RESEARCH_PRODUCTS,
    SCHOLIX,
)
from .exceptions import AireloomError, ValidationError
from .log_config import configure_logging
from .models import (
    ApiResponse,
    BaseEntity,
    DataSource,
    DataSourceResponse,
    Organization,
    OrganizationResponse,
    Project,
    ProjectResponse,
    ResearchProduct,
    ResearchProductResponse,
    ScholixRelationship,
    ScholixResponse,
)

configure_logging()

GraphApiEntityType = TypeVar(
    "GraphApiEntityType", ResearchProduct, Organization, DataSource, Project
)
GraphApiResponseType = TypeVar("GraphApiResponseType", bound=ApiResponse)


class AireloomSession:
    """Provides methods to interact with the OpenAIRE Graph API and Scholexplorer API."""

    def __init__(
        self,
        auth_strategy: AuthStrategy | None = None,
        timeout: int | None = None,
        api_base_url: str | None = None,
        scholix_base_url: str | None = None,
    ):
        """Initializes the Aireloom session.

        Args:
            auth_strategy:  Authentication strategy (e.g., NoAuth(), TokenAuth(...)).
                            Defaults to NoAuth.
            timeout: Default request timeout in seconds.
            api_base_url: Base URL for the OpenAIRE Graph API.
            scholix_base_url: Base URL for the Scholexplorer API.
        """
        self._auth_strategy = auth_strategy or NoAuth()
        self._api_base_url = api_base_url or OPENAIRE_GRAPH_API_BASE_URL
        self._scholix_base_url = scholix_base_url or OPENAIRE_SCHOLIX_API_BASE_URL

        self._api_client = AireloomClient(
            auth_strategy=self._auth_strategy,
            base_url=self._api_base_url,
        )
        logger.info(f"AireloomSession initialized for API: {self._api_base_url}")
        logger.info(f"Scholexplorer configured for: {self._scholix_base_url}")

        self._model_map: dict[
            str, dict[str, type[BaseEntity | ApiResponse | ScholixResponse]]
        ] = {
            RESEARCH_PRODUCTS: {
                "entity": ResearchProduct,
                "response": ResearchProductResponse,
            },
            ORGANIZATIONS: {"entity": Organization, "response": OrganizationResponse},
            DATA_SOURCES: {"entity": DataSource, "response": DataSourceResponse},
            PROJECTS: {"entity": Project, "response": ProjectResponse},
            # Scholix has a different structure, handled separately but mapped for validation
            SCHOLIX: {"entity": ScholixRelationship, "response": ScholixResponse},
        }

    # --- Helper Methods --- #

    def _validate_filters(self, entity_path: str, filters: dict[str, Any]) -> None:
        """Validates filter keys and attempts type conversion based on endpoint definitions."""
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path definition: {entity_path}")

        valid_filters = ENDPOINT_DEFINITIONS[entity_path].get("filters", {})
        if not valid_filters and filters:
            logger.warning(
                f"Filters provided for {entity_path}, but none are defined. Ignoring filters: {filters}"
            )
            return
        if not valid_filters:
            return

        for key, value in filters.items():
            if key not in valid_filters:
                raise ValidationError(
                    f"Invalid filter key for {entity_path}: '{key}'. Valid keys: {list(valid_filters)}"
                )

            try:
                filters[key] = self._validate_and_convert_filter_value(
                    key, value, valid_filters[key].get("type", "any")
                )
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Invalid type/value for filter '{key}'. Expected {valid_filters[key].get('type', 'any')}, got {type(value).__name__}. {e}"
                ) from e

    def _validate_and_convert_filter_value(
        self, key: str, value: Any, expected_type_str: str
    ) -> Any:
        """Validates and converts a single filter value based on the expected type string."""
        current_type = type(value)

        type_map = {
            "string": str,
            "integer": int,
            "boolean": bool,
            # Add other types here if needed (e.g., "list": list)
        }

        if expected_type_str == "any" or expected_type_str not in type_map:
            return value

        target_type = type_map[expected_type_str]

        if isinstance(value, target_type):
            return value

        logger.warning(
            f"Filter '{key}' expects {expected_type_str}, got {current_type.__name__}. Attempting conversion."
        )

        # Handle boolean string conversion explicitly
        if target_type is bool and isinstance(value, str):
            lower_val = value.lower()
            if lower_val in ["true", "1", "yes"]:
                return True
            if lower_val in ["false", "0", "no"]:
                return False
            raise ValueError("String cannot be reliably converted to boolean")

        # General conversion attempt
        try:
            return target_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Conversion to {expected_type_str} failed") from e

    def _validate_sort(self, entity_path: str, sort_by: str | None) -> None:
        """Validates the sort field against endpoint definitions."""
        if not sort_by:
            return
        if entity_path not in ENDPOINT_DEFINITIONS:
            raise ValueError(f"Unknown entity path: {entity_path}")

        valid_sort_fields = ENDPOINT_DEFINITIONS[entity_path]["sort_fields"]
        # Sort format can be "field", "field asc", "field desc"
        sort_field = sort_by.split()[0]
        if sort_field not in valid_sort_fields:
            raise ValidationError(
                f"Invalid sort field for {entity_path}: '{sort_field}'"
            )

    def _build_params(
        self, page: int, page_size: int, sort_by: str | None, filters: dict[str, Any]
    ) -> dict[str, Any]:
        """Builds the query parameter dictionary."""
        params = {"page": page, "pageSize": page_size}
        if sort_by:
            params["sortBy"] = sort_by
        params.update(filters)
        # Remove None values, encode others safely
        return {k: v for k, v in params.items() if v is not None}

    async def _get_single_entity(
        self, entity_path: str, entity_id: str, entity_model: type[GraphApiEntityType]
    ) -> GraphApiEntityType:
        """Generic method to fetch a single entity by ID."""
        endpoint = f"{entity_path}/{entity_id}"
        try:
            response = await self._api_client.request("GET", endpoint)
            # Parse directly into the entity model
            return entity_model.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            # Use http.HTTPStatus constant
            if e.response.status_code == http.HTTPStatus.NOT_FOUND:
                raise AireloomError(
                    f"{entity_model.__name__} with ID '{entity_id}' not found."
                ) from e
            raise
        except Exception as e:
            if isinstance(e, AireloomError):
                raise e
            raise AireloomError(
                f"Failed to fetch {entity_model.__name__} {entity_id}: {e}"
            ) from e

    async def _search_entities(
        self,
        entity_path: str,
        response_model: type[GraphApiResponseType],
        params: dict[str, Any],
    ) -> GraphApiResponseType:
        """Generic method to search for entities."""
        try:
            response = await self._api_client.request("GET", entity_path, params=params)
            return response_model.model_validate(response.json())
        except Exception as e:
            if isinstance(e, AireloomError | ValidationError):
                raise e
            raise AireloomError(f"Failed to search {entity_path}: {e}") from e

    async def _iterate_entities(
        self,
        entity_path: str,
        entity_model: type[GraphApiEntityType],
        params: dict[str, Any],
    ) -> AsyncIterator[GraphApiEntityType]:
        """Generic method to iterate through all results using cursor pagination."""
        # Use cursor pagination: start with '*', remove page/size if present
        current_params = params.copy()
        current_params.pop("page", None)
        current_params["cursor"] = "*"
        if "size" not in current_params:
            current_params["size"] = DEFAULT_PAGE_SIZE

        while True:
            try:
                response = await self._api_client.request(
                    "GET", entity_path, params=current_params
                )
                data = response.json()
                api_response = ApiResponse[entity_model].model_validate(data)

                if not api_response.results:
                    break

                for result in api_response.results:
                    yield result

                next_cursor = api_response.header.nextCursor
                if not next_cursor:
                    break

                current_params["cursor"] = next_cursor

            except Exception as e:
                if isinstance(e, AireloomError | ValidationError):
                    raise e
                logger.exception(
                    f"Failed during iteration of {entity_path}"
                )
                raise AireloomError(
                    f"Failed during iteration of {entity_path}: {e}"
                ) from e

    # --- Public Methods for Graph API --- #

    async def get_research_product(self, product_id: str) -> ResearchProduct:
        """Retrieves a single Research Product by its ID."""
        return await self._get_single_entity(
            RESEARCH_PRODUCTS, product_id, ResearchProduct
        )

    async def search_research_products(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> ResearchProductResponse:
        """Searches for Research Products.

        Args:
            page: Page number (1-indexed).
            page_size: Number of results per page.
            sort_by: Field to sort by (e.g., 'title asc', 'publicationdate desc').
            **filters: Keyword arguments for filtering (e.g., country='US', openAccess=True).

        Returns:
            A ResearchProductResponse object containing results and header info.
        """
        self._validate_filters(RESEARCH_PRODUCTS, filters)
        self._validate_sort(RESEARCH_PRODUCTS, sort_by)
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            **filters,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_entities(
            RESEARCH_PRODUCTS, ResearchProductResponse, params
        )

    async def iterate_research_products(
        self,
        page_size: int = 100,
        sort_by: str | None = None,
        **filters: Any,
    ) -> AsyncIterator[ResearchProduct]:
        """Iterates through all Research Product results matching the criteria.

        Uses cursor-based pagination for efficiency.

        Args:
            page_size: Number of results to fetch per API call during iteration.
            sort_by: Field to sort by.
            **filters: Keyword arguments for filtering.

        Yields:
            ResearchProduct objects.
        """
        self._validate_filters(RESEARCH_PRODUCTS, filters)
        self._validate_sort(RESEARCH_PRODUCTS, sort_by)
        # Build params *without* page, ensure size is present
        params = {
            "page": 1,
            "pageSize": page_size,
            "sortBy": sort_by,
            **filters,
        }
        params.pop("page", None)

        async for item in self._iterate_entities(
            RESEARCH_PRODUCTS, ResearchProduct, params
        ):
            yield item

    async def get_organization(self, org_id: str) -> Organization:
        """Retrieves a single Organization by its ID."""
        return await self._get_single_entity(ORGANIZATIONS, org_id, Organization)

    async def search_organizations(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> OrganizationResponse:
        """Searches for Organizations."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(ORGANIZATIONS, OrganizationResponse, params)

    async def iterate_organizations(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[Organization]:
        """Iterates through all Organization results."""
        self._validate_filters(ORGANIZATIONS, filters)
        self._validate_sort(ORGANIZATIONS, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(ORGANIZATIONS, Organization, params):
            yield item

    async def get_data_source(self, source_id: str) -> DataSource:
        """Retrieves a single Data Source by its ID."""
        return await self._get_single_entity(DATA_SOURCES, source_id, DataSource)

    async def search_data_sources(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> DataSourceResponse:
        """Searches for Data Sources."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(DATA_SOURCES, DataSourceResponse, params)

    async def iterate_data_sources(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[DataSource]:
        """Iterates through all Data Source results."""
        self._validate_filters(DATA_SOURCES, filters)
        self._validate_sort(DATA_SOURCES, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(DATA_SOURCES, DataSource, params):
            yield item

    async def get_project(self, project_id: str) -> Project:
        """Retrieves a single Project by its ID."""
        return await self._get_single_entity(PROJECTS, project_id, Project)

    async def search_projects(
        self,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort_by: str | None = None,
        **filters: Any,
    ) -> ProjectResponse:
        """Searches for Projects."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(page, page_size, sort_by, filters)
        return await self._search_entities(PROJECTS, ProjectResponse, params)

    async def iterate_projects(
        self, page_size: int = 100, sort_by: str | None = None, **filters: Any
    ) -> AsyncIterator[Project]:
        """Iterates through all Project results."""
        self._validate_filters(PROJECTS, filters)
        self._validate_sort(PROJECTS, sort_by)
        params = self._build_params(
            page=1, page_size=page_size, sort_by=sort_by, filters=filters
        )
        params.pop("page", None)
        async for item in self._iterate_entities(PROJECTS, Project, params):
            yield item

    # --- Scholexplorer Methods --- #

    async def search_scholix_links(
        self,
        page: int = 0,
        page_size: int = DEFAULT_PAGE_SIZE,
        **filters: Any,
    ) -> ScholixResponse:
        """Searches for Scholexplorer relationship links.

        Args:
            page: The page number to retrieve (0-indexed).
            page_size: The number of results per page.
            **filters: Keyword arguments corresponding to valid Scholexplorer filters
                       (e.g., sourcePid, targetPid, relationshipType, linkProviderName).

        Returns:
            A ScholixResponse object containing the results for the requested page.

        Raises:
            ValidationError: If invalid filter keys are provided.
            AireloomError: For API communication errors or unexpected issues.
        """
        # Use a mutable copy for validation side-effects
        mutable_filters = filters.copy()
        self._validate_filters(SCHOLIX, mutable_filters)

        # Scholexplorer uses 0-based page, size is 'rows'
        params = {
            "page": page,
            "rows": page_size,
            **mutable_filters,
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await self._api_client.request(
                method="GET",
                path=SCHOLIX,
                params=params,
                base_url_override=self._scholix_base_url,
            )
            return ScholixResponse.model_validate(response.json())
        except Exception as e:
            # Use | for isinstance check
            if isinstance(e, AireloomError | ValidationError):
                raise e
            logger.exception(f"Failed to search {SCHOLIX}")  # Log exception details
            raise AireloomError(f"Failed to search {SCHOLIX}: {e}") from e

    async def iterate_scholix_links(
        self,
        page_size: int = DEFAULT_PAGE_SIZE,
        **filters: Any,
    ) -> AsyncIterator[ScholixRelationship]:
        """Iterates through all Scholexplorer relationship links matching the filters.

        Handles pagination automatically based on 'totalPages'.

        Args:
            page_size: The number of results per page during iteration.
            **filters: Keyword arguments corresponding to valid Scholexplorer filters.

        Yields:
            ScholixRelationship objects matching the query.

        Raises:
            ValidationError: If invalid filter keys are provided.
            AireloomError: For API communication errors or unexpected issues.
        """
        # Validate filters first (validation modifies the dict if types need conversion)
        mutable_filters = filters.copy()
        self._validate_filters(SCHOLIX, mutable_filters)

        current_page = 0
        total_pages = 1 # Assume at least one page initially

        while current_page < total_pages:
            logger.debug(
                f"Iterating Scholix page {current_page + 1}/{total_pages if total_pages > 1 else '?'}"
            )
            try:
                # Call search_scholix_links, passing page_size explicitly,
                # and validated filters via **mutable_filters.
                response_data = await self.search_scholix_links(
                    page=current_page,
                    page_size=page_size, # Pass page_size directly
                    **mutable_filters, # Pass validated filters
                )

                if not response_data.result:
                    logger.debug("No results found on this page, stopping iteration.")
                    break

                for link in response_data.result:
                    yield link

                # Update total_pages from the first response, then check if done
                if current_page == 0:
                    total_pages = response_data.totalPages
                    logger.debug(f"Total pages reported by Scholix: {total_pages}")

                # Check if we've processed the last page
                if current_page >= total_pages - 1:
                    logger.debug("Last page processed, stopping iteration.")
                    break

                current_page += 1

            except Exception as e:
                # Use | for isinstance check
                if isinstance(e, AireloomError | ValidationError):
                    raise e
                logger.exception(
                    f"Failed during iteration of {SCHOLIX} on page {current_page}"
                )  # Log exception
                raise AireloomError(
                    f"Failed during iteration of {SCHOLIX} on page {current_page}: {e}"
                ) from e
        logger.debug("Scholix iteration finished.")

    async def close(self) -> None:
        """Closes the underlying HTTP client session."""
        await self._api_client.aclose()

    async def __aenter__(self) -> "AireloomSession":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()



# -------------------------------------------------------
#
# C:\dev\AIREloom\aireloom\types.py
#
# ------------------------------------------------------

# aireloom/types.py
from collections.abc import Mapping
from typing import Any

import httpx
from pydantic import BaseModel, Field


class RequestData(BaseModel):
    """Encapsulates data for a single HTTP request attempt."""

    method: str
    url: str
    params: Mapping[str, Any] | None = None
    json_data: Any | None = None
    data: Mapping[str, Any] | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    model_config = dict(extra="allow")

    def build_request(self) -> httpx.Request:
        """Builds an httpx.Request object from the stored data."""
        return httpx.Request(
            method=self.method,
            url=self.url,
            params=self.params,
            json=self.json_data,
            data=self.data,
            headers=self.headers,
        )



