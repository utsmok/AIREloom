"""Defines OpenAIRE API endpoint paths, filter models, and related configurations.

This module centralizes the definitions for various OpenAIRE API endpoints,
including their relative paths and Pydantic models for request filter parameters.
It also provides the ENDPOINT_DEFINITIONS registry mapping each endpoint path to
its filter model and valid sort fields.

The filter models ensure type safety and validation for parameters passed to the
API client's search and iteration methods. Field names mirror the OpenAIRE Graph
API V3 query parameters exactly (see the V3 OpenAPI spec at
https://api.openaire.eu/graph/swagger-ui/index.html ). All Graph filter models
use ``extra="forbid"`` so typos raise a clear validation error.

Note: V3 filter values containing spaces, parentheses, or logical operators must
be double-quoted (e.g. ``accessRightLabel='"Open Access"'``) and support inline
``OR``/``AND``/``NOT``. ``logicalOperator`` now also accepts ``"NOT"``.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RESEARCH_PRODUCTS = "research-products"
ORGANIZATIONS = "organizations"
DATA_SOURCES = "datasources"
PROJECTS = "projects"
PERSONS = "persons"
SCHOLIX = "Links"
LINKS = "research-products/links"


class ResearchProductsFilters(BaseModel):
    """Filter model for the Research Products V3 endpoint (``/v3/research-products``).

    Field names mirror the V3 query parameters exactly. See the V3 OpenAPI spec
    for the authoritative list and allowed values. Most string fields support
    inline logical operators (``OR``/``AND``/``NOT``) with double-quoted values.

    Notable V3 changes from V1/V2:
        - ``authorOrcid`` renamed to ``authorId``.
        - ``bestOpenAccessRightLabel`` renamed to ``accessRightLabel``
          (allowed: Open Access, Closed Access, Restricted, Open Source, Embargo,
          Unknown).
        - ``sdg`` (was ``list[str]``) renamed to ``sdgLabel`` (``str``; use inline
          OR for multiple, e.g. ``sdgLabel='"3. Good health" OR "4. Education"'``).
        - 17 new fields added (publication-year filters, ``language``, ``hasLicense``,
          ``relProject``, ``relFunder``, ``relFundingLevel{0,1,2}Id``, ``source``,
          ``eoscIfGuidelines``, ``subCommunity``, ``relCommunityName``,
          ``relOrganization``, ``relHostingDataSource``, ``excludePubDateRange``).
    """

    search: str | None = None
    mainTitle: str | None = None
    description: str | None = None
    id: str | None = None
    pid: str | None = None
    originalId: str | None = None
    type: Literal["publication", "dataset", "software", "other"] | None = None
    fromPublicationDate: date | None = None
    toPublicationDate: date | None = None
    fromPublicationYear: int | None = None
    toPublicationYear: int | None = None
    publicationYear: str | None = None
    excludePubDateRange: bool | None = None
    subjects: list[str] | None = None
    language: str | None = None
    countryCode: str | None = None
    authorFullName: str | None = None
    authorId: str | None = None
    publisher: str | None = None
    accessRightLabel: str | None = None
    influenceClass: str | None = None
    impulseClass: str | None = None
    popularityClass: str | None = None
    citationCountClass: str | None = None
    instanceType: str | None = None
    sdgLabel: str | None = None
    fos: list[str] | None = None
    isPeerReviewed: bool | None = None
    isInDiamondJournal: bool | None = None
    isPubliclyFunded: bool | None = None
    hasLicense: bool | None = None
    isGreen: bool | None = None
    openAccessColor: str | None = None
    eoscIfGuidelines: str | None = None
    relOrganizationId: str | None = None
    relOrganization: str | None = None
    relCommunityId: str | None = None
    relCommunityName: str | None = None
    subCommunity: str | None = None
    relProjectId: str | None = None
    relProjectCode: str | None = None
    relProject: str | None = None
    hasProjectRel: bool | None = None
    relProjectFundingShortName: str | None = None
    relProjectFundingStreamId: str | None = None
    relFunder: str | None = None
    relFundingLevel0Id: str | None = None
    relFundingLevel1Id: str | None = None
    relFundingLevel2Id: str | None = None
    relHostingDataSourceId: str | None = None
    relHostingDataSource: str | None = None
    relCollectedFromDatasourceId: str | None = None
    source: str | None = None
    rorId: str | None = None
    logicalOperator: Literal["AND", "OR", "NOT"] | None = None

    model_config = ConfigDict(extra="forbid")


class OrganizationsFilters(BaseModel):
    """Filter model for the Organizations V3 endpoint (``/v3/organizations``).

    Attributes:
        search (str | None): Search term for the organization.
        legalName (str | None): Legal name of the organization.
        legalShortName (str | None): Legal short name of the organization.
        id (str | None): OpenAIRE id for the organization.
        pid (str | None): Persistent identifier for the organization.
        countryCode (str | None): Country code of the organization.
        relCommunityId (str | None): Related community ID.
        relCollectedFromDatasourceId (str | None): ID of the datasource from which this was collected.
        logicalOperator (Literal["AND", "OR", "NOT"] | None): How multiple filters are combined (default: AND).
    """

    search: str | None = None
    legalName: str | None = None
    legalShortName: str | None = None
    id: str | None = None
    pid: str | None = None
    countryCode: str | None = None
    relCommunityId: str | None = None
    relCollectedFromDatasourceId: str | None = None
    logicalOperator: Literal["AND", "OR", "NOT"] | None = None

    model_config = ConfigDict(extra="forbid")


class DataSourcesFilters(BaseModel):
    """Filter model for the Data Sources V3 endpoint (``/v3/datasources``).

    Field names mirror the V3 query parameters exactly. V3 adds 8 new fields:
    ``collectedFromName``, ``compatibilityId``, ``compatibilityName``, ``country``,
    ``eoscdatasourcetype``, ``jurisdiction``, ``odLanguages``, ``thematic``.
    """

    search: str | None = None
    officialName: str | None = None
    englishName: str | None = None
    legalShortName: str | None = None
    id: str | None = None
    pid: str | None = None
    subjects: list[str] | None = None
    dataSourceTypeName: str | None = None
    contentTypes: list[str] | None = None
    relOrganizationId: str | None = None
    relCommunityId: str | None = None
    relCollectedFromDatasourceId: str | None = None
    collectedFromName: str | None = None
    compatibilityId: str | None = None
    compatibilityName: str | None = None
    country: str | None = None
    eoscdatasourcetype: str | None = None
    jurisdiction: str | None = None
    odLanguages: str | None = None
    thematic: bool | None = None
    logicalOperator: Literal["AND", "OR", "NOT"] | None = None

    model_config = ConfigDict(extra="forbid")


class ProjectsFilters(BaseModel):
    """Filter model for the Projects V3 endpoint (``/v3/projects``).

    Field names mirror the V3 query parameters exactly. Notable V3 changes:
        - ``grantID`` removed (no longer a V3 parameter).
        - ``fromStartDate``/``toStartDate``/``fromEndDate``/``toEndDate`` changed
          from ``date`` to ``str`` (V3 accepts bare years, e.g. ``"2022"``).
        - 13 new fields added (year filters, ``funder``, ``country``,
          ``fundinglevel{0,1,2}Id``, ``projectOAMandatePublications``).

    Note:
        ``funder`` returned 0 results for all values tested as of 2026-07; prefer
        ``fundingShortName``. Kept for forward compatibility.
    """

    search: str | None = None
    title: str | None = None
    keywords: list[str] | None = None
    id: str | None = None
    code: str | None = None
    acronym: str | None = None
    callIdentifier: str | None = None
    fundingShortName: str | None = None
    fundingStreamId: str | None = None
    funder: str | None = None
    fromStartDate: str | None = None
    toStartDate: str | None = None
    fromEndDate: str | None = None
    toEndDate: str | None = None
    fromStartYear: str | None = None
    toStartYear: str | None = None
    fromEndYear: str | None = None
    toEndYear: str | None = None
    startYear: str | None = None
    endYear: str | None = None
    activeYear: str | None = None
    country: str | None = None
    fundinglevel0Id: str | None = None
    fundinglevel1Id: str | None = None
    fundinglevel2Id: str | None = None
    projectOAMandatePublications: str | None = None
    relOrganizationName: str | None = None
    relOrganizationId: str | None = None
    relCommunityId: str | None = None
    relOrganizationCountryCode: str | None = None
    relCollectedFromDatasourceId: str | None = None
    logicalOperator: Literal["AND", "OR", "NOT"] | None = None

    model_config = ConfigDict(extra="forbid")


class ScholixFilters(BaseModel):
    """Filter model for Scholix API endpoint.

    Attributes:
        sourcePid (str | None): Persistent identifier of the source entity.
        targetPid (str | None): Persistent identifier of the target entity.
        sourcePublisher (str | None): Publisher of the source entity.
        targetPublisher (str | None): Publisher of the target entity.
        sourceType (Literal["Publication", "Dataset", "Software", "Other"] | None): Type of the source entity.
        targetType (Literal["Publication", "Dataset", "Software", "Other"] | None): Type of the target entity.
        relation (str | None): Type of relation between the source and target entities.
        from_date (date | None): Start date of the relation (API calls use "from").
        to_date (date | None): End date of the relation (API calls use "to").
    """

    sourcePid: str | None = None
    targetPid: str | None = None
    sourcePublisher: str | None = None
    targetPublisher: str | None = None
    sourceType: Literal["Publication", "Dataset", "Software", "Other"] | None = None
    targetType: Literal["Publication", "Dataset", "Software", "Other"] | None = None
    relation: str | None = None
    linkProvider: str | None = None
    sourcePidType: str | None = None
    targetPidType: str | None = None
    from_date: date | None = Field(default=None, alias="from")  # API uses "from"
    to_date: date | None = Field(default=None, alias="to")  # API uses "to"

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class LinksFilters(BaseModel):
    """Filter model for Graph API /research-products/links endpoint.

    These filters are for the Graph API's built-in link retrieval endpoint,
    which is separate from the Scholix API. Parameters accept singular string values
    (unlike other Graph API filters which accept arrays).

    Reference: https://api.openaire.eu/graph/v3/research-products/links
    """

    sourcePid: str | None = Field(
        default=None, description="Filter by source persistent identifier (e.g. DOI)"
    )
    targetPid: str | None = Field(
        default=None, description="Filter by target persistent identifier"
    )
    sourcePublisher: str | None = Field(
        default=None, description="Filter by source publisher name"
    )
    targetPublisher: str | None = Field(
        default=None, description="Filter by target publisher name"
    )
    sourceType: str | None = Field(
        default=None,
        description="Filter by source type: publication, dataset, software, other",
    )
    targetType: str | None = Field(
        default=None,
        description="Filter by target type: publication, dataset, software, other",
    )
    relation: str | None = Field(
        default=None, description="Filter by specific relationship type"
    )
    fromDate: str | None = Field(
        default=None, description="From date (YYYY or YYYY-MM-DD)"
    )
    toDate: str | None = Field(default=None, description="To date (YYYY or YYYY-MM-DD)")

    model_config = ConfigDict(extra="forbid")


class PersonsFilters(BaseModel):
    """Filter model for the Persons V3 endpoint (``/v3/persons``).

    All six filter parameters are functional in V3. (In V1/V2, ``givenName`` and
    ``lastName`` returned HTTP 500; both are fixed in V3.)

    Attributes:
        search (str | None): Keyword search for the person.
        id (str | None): OpenAIRE identifier.
        originalId (str | None): Original identifier (e.g. ORCID).
        givenName (str | None): Person's given (first) name.
        lastName (str | None): Person's family (last) name.
        logicalOperator (Literal["AND", "OR", "NOT"] | None): How multiple filters are combined.
    """

    search: str | None = None
    id: str | None = None
    originalId: str | None = None
    givenName: str | None = None
    lastName: str | None = None
    logicalOperator: Literal["AND", "OR", "NOT"] | None = None

    model_config = ConfigDict(extra="forbid")


# Basic definition structure: {path: {'filters_model': PydanticModel, 'sort': dict()}}
ENDPOINT_DEFINITIONS = {
    RESEARCH_PRODUCTS: {
        "filters_model": ResearchProductsFilters,
        "sort": {
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
        "filters_model": OrganizationsFilters,
        "sort": {"relevance": {}},
    },
    DATA_SOURCES: {
        "filters_model": DataSourcesFilters,
        "sort": {"relevance": {}},
    },
    PROJECTS: {
        "filters_model": ProjectsFilters,
        "sort": {
            "relevance": {},
            "startDate": {},
            "endDate": {},
        },
    },
    PERSONS: {
        "filters_model": PersonsFilters,
        "sort": {"relevance": {}},
    },
    SCHOLIX: {
        "filters_model": ScholixFilters,
        "sort": {},
    },
}
