# aireloom/models/research_product.py
"""Pydantic models for representing OpenAIRE Research Product entities.

This module defines the Pydantic model for an OpenAIRE Research Product,
which can be a publication, dataset, software, or other research output.
It includes various nested models to represent complex fields like authors,
persistent identifiers (PIDs), access rights, citation impacts, instances, etc.,
based on the OpenAIRE data model documentation.
Reference: https://graph.openaire.eu/docs/data-model/entities/research-product
"""

import logging
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from .._helpers import extract_all_pids_by_scheme, extract_pid_by_scheme
from .base import ApiResponse, BaseEntity
from .safe_types import SafeList, SafeStr

OpenAccessRouteType = Literal["gold", "green", "hybrid", "bronze"]
"""Type alias for allowed Open Access routes (e.g., gold, green)."""

RefereedType = Literal["peerReviewed", "nonPeerReviewed", "UNKNOWN"]
"""Type alias for refereed status (e.g., peerReviewed, nonPeerReviewed)."""

ResearchProductType = Literal["publication", "dataset", "software", "other"]
"""Type alias for the type of research product (e.g., publication, dataset)."""

logger = logging.getLogger(__name__)


# Sub-models for nested structures


class Pid(BaseModel):
    """Represents a Persistent Identifier (PID) with its scheme and value.

    Attributes:
        scheme: The scheme of the PID (e.g., "doi", "orcid", "handle").
        value: The actual value of the PID.
    """

    scheme: SafeStr = ""
    value: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class Author(BaseModel):
    """Represents an author of a research product.

    Attributes:
        fullName: The full name of the author.
        rank: The rank or order of the author in an author list.
        name: The given name(s) of the author.
        surname: The surname or family name of the author.
        pid: A dictionary representing a persistent identifier for the author (e.g., ORCID).
    """

    fullName: SafeStr = ""
    rank: int | None = None
    name: SafeStr = ""
    surname: str | None = None
    pid: dict | None = None

    model_config = ConfigDict(extra="allow")


class BestAccessRight(BaseModel):
    """Represents the best determined access right for a research product.

    Attributes:
        code: The code representing the access right (e.g., "OPEN").
        label: A human-readable label for the access right (e.g., "Open Access").
        scheme: The scheme or vocabulary defining the access right code.
    """

    code: SafeStr = ""
    label: SafeStr = ""
    scheme: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeBestAccessRight = Annotated[BestAccessRight, BeforeValidator(lambda v: BestAccessRight() if v is None else v)]


class ResultCountry(BaseModel):
    """Represents the country associated with a research product or entity.

    Attributes:
        code: The ISO 3166-1 alpha-2 country code.
        label: The human-readable name of the country.
    """

    code: SafeStr = ""
    label: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeResultCountry = Annotated[ResultCountry, BeforeValidator(lambda v: ResultCountry() if v is None else v)]


class CitationImpact(BaseModel):
    """Captures various citation-based impact metrics for a research product.

    Attributes:
        influence: A numerical score representing influence (meaning may vary).
        influenceClass: A categorical classification of influence (e.g., C1-C5).
        citationCount: The total number of citations received.
        citationClass: A categorical classification based on citation count.
        popularity: A numerical score representing popularity.
        popularityClass: A categorical classification of popularity.
        impulse: A numerical score representing research impulse or momentum.
        impulseClass: A categorical classification of impulse.
    """

    influence: float | None = None
    influenceClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    citationCount: int | None = None
    citationClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    popularity: float | None = None
    popularityClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None
    impulse: float | None = None
    impulseClass: Literal["C1", "C2", "C3", "C4", "C5"] | None = None

    model_config = ConfigDict(extra="allow")


SafeCitationImpact = Annotated[CitationImpact, BeforeValidator(lambda v: CitationImpact() if v is None else v)]


class UsageCounts(BaseModel):
    """Represents usage counts for a research product, like downloads and views.

    Includes a validator to coerce string values from the API into integers.

    Attributes:
        downloads: The number of times the research product has been downloaded.
        views: The number of times the research product has been viewed.
    """

    downloads: int | None = None
    views: int | None = None

    @field_validator("downloads", "views", mode="before")
    @classmethod
    def coerce_str_to_int(cls, v: Any) -> int | None:
        """Coerces string count values to integers, also handling None and logging errors.

        Args:
            v: The value to coerce.

        Returns:
            The value as an integer, or None if coercion is not possible or input is None.
        """
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


SafeUsageCounts = Annotated[UsageCounts, BeforeValidator(lambda v: UsageCounts() if v is None else v)]


class Indicator(BaseModel):
    """Container for various impact indicators of a research product.

    Attributes:
        citationImpact: A `CitationImpact` object detailing citation metrics.
        usageCounts: A `UsageCounts` object detailing view and download counts.
    """

    citationImpact: SafeCitationImpact = Field(default_factory=CitationImpact)
    usageCounts: SafeUsageCounts = Field(default_factory=UsageCounts)

    model_config = ConfigDict(extra="allow")


SafeIndicator = Annotated[Indicator, BeforeValidator(lambda v: Indicator() if v is None else v)]


class AccessRight(BaseModel):
    """Represents the access rights associated with an instance of a research product.

    Attributes:
        code: A code representing the access right (e.g., "OPEN", "RESTRICTED").
        label: A human-readable label for the access right.
        openAccessRoute: The Open Access route, if applicable (e.g., "gold", "green").
        scheme: The scheme defining the access right codes.
    """

    code: SafeStr = ""
    label: SafeStr = ""
    openAccessRoute: OpenAccessRouteType | None = None
    scheme: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeAccessRight = Annotated[AccessRight, BeforeValidator(lambda v: AccessRight() if v is None else v)]


class ArticleProcessingCharge(BaseModel):
    """Represents Article Processing Charge (APC) information.

    Attributes:
        amount: The amount of the APC, typically as a string to accommodate various formats.
        currency: The currency code for the APC amount (e.g., "EUR", "USD").
    """

    amount: str | None = None
    currency: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class ResultPid(BaseModel):
    """Represents a Persistent Identifier (PID) within a result context.

    Note: This model appears functionally identical to the top-level `Pid` model.
    Consider aliasing or reusing `Pid` if their semantics are indeed the same.

    Attributes:
        scheme: The scheme of the PID.
        value: The value of the PID.
    """

    scheme: SafeStr = ""
    value: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class License(BaseModel):
    """Represents license information.

    Note: This model was marked as potentially unused in the original API response
    analysis. It's kept for completeness but might not be populated.
    The `Instance.license` field is currently a simple string.

    Attributes:
        code: A code for the license (e.g., "CC-BY-4.0").
        label: A human-readable label for the license.
    """

    code: SafeStr = ""
    label: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class CollectedFrom(BaseModel):
    """Represents the data source from which an instance was collected."""

    name: SafeStr = ""
    id: str | None = None

    model_config = ConfigDict(extra="allow")


SafeCollectedFrom = Annotated[CollectedFrom, BeforeValidator(lambda v: CollectedFrom() if v is None else v)]


class HostedBy(BaseModel):
    """Represents the data source hosting an instance."""

    name: SafeStr = ""
    id: str | None = None

    model_config = ConfigDict(extra="allow")


SafeHostedBy = Annotated[HostedBy, BeforeValidator(lambda v: HostedBy() if v is None else v)]


class Instance(BaseModel):
    """Represents a specific instance or manifestation of a research product.

    A research product can have multiple instances, for example, a preprint version,
    a published version in a journal, a copy in a repository, etc. Each instance
    can have its own access rights, license, and location.

    Attributes:
        accessRight: An `AccessRight` object detailing the access conditions for this instance.
        alternateIdentifier: A list of alternative identifiers for this instance.
        articleProcessingCharge: An `ArticleProcessingCharge` object, if applicable.
        license: A string representing the license of this instance.
                 (Note: API sometimes provides this as a simple string).
        collectedFrom: Information about the data source from which this instance was collected.
        hostedBy: Information about the data source hosting this instance.
        distributionLocation: The primary URL or location where this instance can be accessed.
        embargoEndDate: The date when an embargo on this instance ends (YYYY-MM-DD string).
        instanceId: A unique identifier for this specific instance.
        publicationDate: The publication date of this specific instance (YYYY-MM-DD string).
        refereed: The refereed status of this instance (`RefereedType`).
        type: The type of this instance (e.g., "fulltext", "abstract").
        urls: A list of URLs associated with this instance.
    """

    accessRight: SafeAccessRight = Field(default_factory=AccessRight)
    alternateIdentifier: list[dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: ArticleProcessingCharge | None = None
    license: str | None = None
    collectedFrom: SafeCollectedFrom = Field(default_factory=CollectedFrom)
    hostedBy: SafeHostedBy = Field(default_factory=HostedBy)
    distributionLocation: str | None = None
    embargoEndDate: str | None = None
    instanceId: str | None = None
    publicationDate: str | None = None
    refereed: RefereedType | None = None
    type: SafeStr = ""
    urls: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")


class Language(BaseModel):
    """Represents a language associated with a research product.

    Attributes:
        code: The language code (e.g., "en", "fr").
        label: The human-readable name of the language (e.g., "English").
    """

    code: SafeStr = ""
    label: SafeStr = ""

    model_config = ConfigDict(extra="allow")


SafeLanguage = Annotated[Language, BeforeValidator(lambda v: Language() if v is None else v)]


class Subject(BaseModel):
    """Represents a subject classification for a research product.

    The API often returns this as a nested dictionary where the key is the
    scheme (e.g., "ddc", "mesh") and the value is the subject term or code.
    This model captures that structure directly.

    Attributes:
        subject: A dictionary where keys are subject schemes and values are subject terms/codes.
                 Example: `{"fos": "Field of Science", "mesh": "D000001"}`
    """

    subject: dict[str, str] | None = None

    model_config = ConfigDict(extra="allow")


# Container for Publication
class Container(BaseModel):
    """Represents the container of a publication (e.g., journal, book series).

    Attributes:
        edition: The edition of the container.
        iss: The issue number of the container.
        issnLinking: The linking ISSN for a serial publication.
        issnOnline: The ISSN for the online version of a serial.
        issnPrinted: The ISSN for the printed version of a serial.
        name: The name of the container (e.g., journal title).
        sp: Start page of the item within the container.
        ep: End page of the item within the container.
        vol: Volume number of the container.
    """

    edition: str | None = None
    iss: str | None = None
    issnLinking: str | None = None
    issnOnline: str | None = None
    issnPrinted: str | None = None
    name: SafeStr = ""
    sp: str | None = None
    ep: str | None = None
    vol: str | None = None

    model_config = ConfigDict(extra="allow")


SafeContainer = Annotated[Container, BeforeValidator(lambda v: Container() if v is None else v)]


# GeoLocation for Data
class GeoLocation(BaseModel):
    """Represents geolocation information, typically for datasets.

    Attributes:
        box: A bounding box defining a geographical area, often as a string
             of coordinates (e.g., "minLon,minLat,maxLon,maxLat").
        place: A human-readable name for the geographical location.
    """

    box: str | None = None
    place: str | None = None

    model_config = ConfigDict(extra="allow")


SafeGeoLocation = Annotated[GeoLocation, BeforeValidator(lambda v: GeoLocation() if v is None else v)]


# Update main ResearchProduct model
class ResearchProduct(BaseEntity):
    """Model representing an OpenAIRE Research Product entity.

    This is a central model in OpenAIRE, representing various outputs of research
    such as publications, datasets, software, or other types. It aggregates
    numerous metadata fields. Inherits `id` from `BaseEntity`.

    Attributes:
        originalIds: A list of original identifiers for the research product.
        pids: A list of `Pid` objects representing persistent identifiers.
        type: The `ResearchProductType` (e.g., "publication", "dataset").
        mainTitle: The primary title of the research product.
        title: The display title (populated from mainTitle if missing).
        subTitle: An optional subtitle.
        authors: A list of `Author` objects.
        bestAccessRight: A `BestAccessRight` object indicating the determined access status.
        country: A `ResultCountry` object indicating the country associated with the product.
        countries: A list of country objects.
        description: A textual description or abstract of the research product.
        descriptions: Multiple descriptions for the research product.
        publicationDate: The publication date of the research product (YYYY-MM-DD string).
        publisher: The name of the publisher.
        embargoEndDate: The embargo end date.
        contributors: A list of contributor strings.
        sources: A list of source reference strings.
        formats: A list of file format strings.
        coverages: A list of coverage information strings.
        dateOfCollection: The collection timestamp.
        lastUpdateTimeStamp: The last update timestamp (Unix epoch milliseconds).
        indicators: An `Indicator` object containing citation and usage metrics.
        instances: A list of `Instance` objects representing different manifestations
                   or versions of the research product.
        language: A `Language` object for the primary language of the product.
        subjects: A list of `Subject` objects.
        container: A `Container` object if the product is part of a larger collection
                   (e.g., a journal for an article).
        keywords: A list of keywords. A validator attempts to parse comma-separated strings.
        geoLocation: A `GeoLocation` object, typically for datasets.
        geoLocations: A list of geolocation objects, typically for datasets.
        isGreen: Whether the product is green Open Access.
        openAccessColor: The Open Access color (e.g., "bronze", "gold", "hybrid").
        isInDiamondJournal: Whether the product is in a diamond journal.
        publiclyFunded: Whether the product was publicly funded.
        codeRepositoryUrl: URL to the code repository (software products).
        documentationUrls: URLs to documentation (software products).
        programmingLanguage: The programming language (software products).
        size: The size of the dataset.
        version: The version of the dataset.
        contactPeople: Contact persons (other products).
        contactGroups: Contact groups (other products).
        tools: Tools used (other products).
        collectedFrom: Data sources from which this product was collected.
        projects: Related project relationships.
        organizations: Related organization relationships.
        communities: Related community relationships.
    """
    # id is inherited from BaseEntity
    originalIds: SafeList[str] = Field(default_factory=list)
    pids: SafeList[Pid] = Field(default_factory=list)
    type: ResearchProductType | None = None
    mainTitle: SafeStr = ""
    title: SafeStr = ""
    subTitle: SafeStr = ""
    authors: SafeList[Author] = Field(default_factory=list)
    bestAccessRight: SafeBestAccessRight = Field(default_factory=BestAccessRight)
    country: SafeResultCountry = Field(default_factory=ResultCountry)
    countries: list | None = None
    description: SafeStr = ""
    descriptions: SafeList[str] = Field(default_factory=list)
    publicationDate: str | None = None
    publisher: SafeStr = ""
    embargoEndDate: str | None = None
    contributors: SafeList[str] = Field(default_factory=list)
    sources: SafeList[str] = Field(default_factory=list)
    formats: SafeList[str] = Field(default_factory=list)
    coverages: SafeList[str] = Field(default_factory=list)
    dateOfCollection: str | None = None
    lastUpdateTimeStamp: int | None = None
    indicators: SafeIndicator = Field(default_factory=Indicator)
    instances: SafeList[Instance] = Field(default_factory=list)
    language: SafeLanguage = Field(default_factory=Language)
    subjects: SafeList[Subject] = Field(default_factory=list)
    container: SafeContainer = Field(default_factory=Container)
    keywords: SafeList[str] = Field(default_factory=list)
    geoLocation: SafeGeoLocation = Field(default_factory=GeoLocation)
    geoLocations: list | None = None

    # Open Access fields
    isGreen: bool | None = None
    openAccessColor: str | None = None
    isInDiamondJournal: bool | None = None
    publiclyFunded: bool | None = None

    # Subtype-specific fields (Software)
    codeRepositoryUrl: str | None = None
    documentationUrls: SafeList[str] = Field(default_factory=list)
    programmingLanguage: str | None = None

    # Subtype-specific fields (Dataset)
    size: str | None = None
    version: str | None = None

    # Subtype-specific fields (Other)
    contactPeople: list | None = None
    contactGroups: list | None = None
    tools: list | None = None

    # Relationship fields
    collectedFrom: SafeList[CollectedFrom] = Field(default_factory=list)
    projects: list | None = None
    organizations: list | None = None
    communities: list | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @field_validator("keywords", mode="before")
    @classmethod
    def split_keywords(cls, v: Any) -> list[str]:
        """Attempts to split a comma-separated string of keywords into a list.

        If the input `v` is a string, it's split by commas, and each part is stripped
        of whitespace. If `v` is None or not a string, it returns an empty list.

        Args:
            v: The value to parse, expected to be a string or None.

        Returns:
            A list of keyword strings, or [] if input was None or unexpected.
        """
        if v is None:
            return []
        if isinstance(v, str):
            return [kw.strip() for kw in v.split(",") if kw.strip()]
        logger.warning(
            f"Unexpected value for ResearchProduct.keywords: {v}. Expected string or None."
        )
        return []

    @model_validator(mode="before")
    @classmethod
    def get_title_from_main_title(cls, data: Any) -> Any:
        """Populates the `title` field from `mainTitle` if `title` is not present.

        The OpenAIRE API sometimes uses `mainTitle` for the primary title. This
        validator ensures that the `title` field in the Pydantic model is populated
        using `mainTitle` if `title` itself is missing in the input data, effectively
        aliasing `mainTitle` to `title`.

        Args:
            data: The raw input data dictionary before validation.

        Returns:
            The (potentially modified) input data dictionary.
        """
        if isinstance(data, dict) and "mainTitle" in data and ("title" not in data or data["title"] is None):
            data["title"] = data["mainTitle"]
            # Keep mainTitle in data so it populates the explicit field
        return data

    # ── Computed fields ─────────────────────────────────────────────────

    @computed_field
    @property
    def doi(self) -> str | None:
        """First DOI from the pids list."""
        return extract_pid_by_scheme(self.pids, "doi")

    @computed_field
    @property
    def all_dois(self) -> list[str]:
        """All DOI values from the pids list."""
        return extract_all_pids_by_scheme(self.pids, "doi")

    @computed_field
    @property
    def is_open_access(self) -> bool:
        """True when the best access right is OPEN."""
        return self.bestAccessRight.label.upper() == "OPEN"

    @computed_field
    @property
    def open_access_url(self) -> str | None:
        """URL of the first instance whose access right is OPEN."""
        for inst in self.instances:
            if inst.accessRight and inst.accessRight.label and inst.accessRight.label.upper() == "OPEN" and inst.urls:
                return inst.urls[0]
        return None

    @computed_field
    @property
    def citation_count(self) -> int | None:
        """Citation count from indicators, if available."""
        return self.indicators.citationImpact.citationCount

    @computed_field
    @property
    def publication_year(self) -> int | None:
        """Year parsed from publicationDate."""
        if self.publicationDate and len(self.publicationDate) >= 4:
            try:
                return int(self.publicationDate[:4])
            except ValueError:
                return None
        return None

    @computed_field
    @property
    def journal_name(self) -> str | None:
        """Container / journal name, or None when empty."""
        return self.container.name or None

    @computed_field
    @property
    def author_names(self) -> list[str]:
        """Non-empty full names of all authors."""
        return [a.fullName for a in self.authors if a.fullName]

    @computed_field
    @property
    def license(self) -> str | None:
        """First non-empty license string found across instances."""
        for inst in self.instances:
            if inst.license:
                return inst.license
        return None

    def __str__(self) -> str:
        parts = []
        if self.title:
            parts.append(self.title[:80])
        if self.publication_year:
            parts.append(f"({self.publication_year})")
        if self.doi:
            parts.append(f"DOI:{self.doi}")
        return " | ".join(parts) if parts else f"ResearchProduct(id={self.id!r})"

# Define the specific response type for ResearchProduct results
ResearchProductResponse = ApiResponse[ResearchProduct]
"""Type alias for an API response containing a list of `ResearchProduct` entities."""
