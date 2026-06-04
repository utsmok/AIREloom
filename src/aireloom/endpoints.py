"""Defines OpenAIRE API endpoint paths, filter models, and related configurations.

This module centralizes the definitions for various OpenAIRE API endpoints,
including their relative paths and Pydantic models for request filter parameters.
It also provides utility functions related to endpoint configurations, such as
retrieving valid sort fields for an endpoint.

The filter models ensure type safety and validation for parameters passed to
the API client's search and iteration methods.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RESEARCH_PRODUCTS = "researchProducts"
ORGANIZATIONS = "organizations"
DATA_SOURCES = "dataSources"
PROJECTS = "projects"
PERSONS = "persons"
SCHOLIX = "Links"
LINKS = "researchProducts/links"


class ResearchProductsFilters(BaseModel):
    """Filter model for Research Products API endpoint.

    Attributes:
        search (str | None): Search term for the research product.
        mainTitle (str | None): Main title of the research product.
        description (str | None): Description of the research product.
        id (str | None): OpenAIRE id for the research product.
        pid (str | None): Persistent identifier for the research product.
        originalId (str | None): Original identifier for the research product.
        type (Literal["publication", "dataset", "software", "other"] | None): Type of the research product.
        fromPublicationDate (date | None): Start date of publication (inclusive).
        toPublicationDate (date | None): End date of publication (inclusive).
        subjects (list[str] | None): List of subjects associated with the research product.
        countryCode (str | None): Country code of the research product.
        authorFullName (str | None): Full name of the author.
        authorOrcid (str | None): ORCID of the author.
        publisher (str | None): Publisher of the research product.
        bestOpenAccessRightLabel (str | None): Best open access right label.
        influenceClass (str | None): Influence class of the research product.
        impulseClass (str | None): Impulse class of the research product.
        popularityClass (str | None): Popularity class of the research product.
        citationCountClass (str | None): Citation count class of the research product.
        instanceType (str | None): Instance type of the research product.
        sdg (list[str] | None): List of SDG goals associated with the research product.
        fos (list[str] | None): List of field of studies associated with the research product.
        isPeerReviewed (bool | None): Flag indicating if the research product is peer-reviewed.
        isInDiamondJournal (bool | None): Flag indicating if the research product is in a diamond journal.
        isPubliclyFunded (bool | None): Flag indicating if the research product is publicly funded.
        isGreen (bool | None): Flag indicating if the research product is green open access.
        openAccessColor (str | None): Color representing the open access status.
        relOrganizationId (str | None): Related organization ID.
        relCommunityId (str | None): Related community ID.
        relProjectId (str | None): Related project ID.
        relProjectCode (str | None): Related project code.
        hasProjectRel (bool | None): Flag indicating if the research product has a related project.
        relProjectFundingShortName (str | None): Short name of the project funding.
        relProjectFundingStreamId (str | None): ID of the project funding stream.
        relHostingDataSourceId (str | None): ID of the hosting data source.
        relCollectedFromDatasourceId (str | None): ID of the datasource from which this was collected.
        rorId (str | None): ROR identifier for an affiliated organization.
        logicalOperator (Literal["AND", "OR"] | None): How multiple filters are combined (default: AND).



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
    subjects: list[str] | None = None
    countryCode: str | None = None
    authorFullName: str | None = None
    authorOrcid: str | None = None
    publisher: str | None = None
    bestOpenAccessRightLabel: str | None = None
    influenceClass: str | None = None
    impulseClass: str | None = None
    popularityClass: str | None = None
    citationCountClass: str | None = None
    instanceType: str | None = None
    sdg: list[str] | None = None
    fos: list[str] | None = None
    isPeerReviewed: bool | None = None
    isInDiamondJournal: bool | None = None
    isPubliclyFunded: bool | None = None
    isGreen: bool | None = None
    openAccessColor: str | None = None
    relOrganizationId: str | None = None
    relCommunityId: str | None = None
    relProjectId: str | None = None
    relProjectCode: str | None = None
    hasProjectRel: bool | None = None
    relProjectFundingShortName: str | None = None
    relProjectFundingStreamId: str | None = None
    relHostingDataSourceId: str | None = None
    relCollectedFromDatasourceId: str | None = None
    rorId: str | None = None
    logicalOperator: Literal["AND", "OR"] | None = None

    model_config = ConfigDict(extra="forbid")


class OrganizationsFilters(BaseModel):
    """Filter model for Organizations API endpoint.

    Attributes:
        search (str | None): Search term for the organization.
        legalName (str | None): Legal name of the organization.
        legalShortName (str | None): Legal short name of the organization.
        id (str | None): OpenAIRE id for the organization.
        pid (str | None): Persistent identifier for the organization.
        countryCode (str | None): Country code of the organization.
        relCommunityId (str | None): Related community ID.
        relCollectedFromDatasourceId (str | None): ID of the datasource from which this was collected.
        logicalOperator (Literal["AND", "OR"] | None): How multiple filters are combined (default: AND).
    """

    search: str | None = None
    legalName: str | None = None
    legalShortName: str | None = None
    id: str | None = None
    pid: str | None = None
    countryCode: str | None = None
    relCommunityId: str | None = None
    relCollectedFromDatasourceId: str | None = None
    logicalOperator: Literal["AND", "OR"] | None = None

    model_config = ConfigDict(extra="forbid")


class DataSourcesFilters(BaseModel):
    """Filter model for Data Sources API endpoint.


    Attributes:
        search (str | None): Search term for the data source.
        officialName (str | None): Official name of the data source.
        englishName (str | None): English name of the data source.
        legalShortName (str | None): Legal short name of the data source.
        id (str | None): OpenAIRE id for the data source.
        pid (str | None): Persistent identifier for the data source.
        subjects (list[str] | None): List of subjects associated with the data source.
        dataSourceTypeName (str | None): Type name of the data source.
        contentTypes (list[str] | None): List of content types available in the data source.
        relOrganizationId (str | None): Related organization ID.
        relCommunityId (str | None): Related community ID.
        relCollectedFromDatasourceId (str | None): ID of the datasource from which this was collected.
        logicalOperator (Literal["AND", "OR"] | None): How multiple filters are combined (default: AND).
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
    logicalOperator: Literal["AND", "OR"] | None = None

    model_config = ConfigDict(extra="forbid")


class ProjectsFilters(BaseModel):
    """Filter model for Projects API endpoint.

    Attributes:
        search (str | None): Search term for the project.
        title (str | None): Title of the project.
        keywords (list[str] | None): List of keywords associated with the project.
        id (str | None): OpenAIRE id for the project.
        code (str | None): Code of the project.
        grantID (str | None): Grant ID associated with the project.
        acronym (str | None): Acronym of the project.
        callIdentifier (str | None): Call identifier of the project.
        fundingShortName (str | None): Short name of the funder.
        fundingStreamId (str | None): Funding stream ID associated with the project.
        fromStartDate (date | None): Start date of the project (inclusive).
        toStartDate (date | None): End date of the project (inclusive).
        fromEndDate (date | None): End date of the project (inclusive).
        toEndDate (date | None): End date of the project (inclusive).
        relOrganizationName (str | None): Name of the related organization.
        relOrganizationId (str | None): ID of the related organization.
        relCommunityId (str | None): ID of the related community.
        relOrganizationCountryCode (str | None): Country code of the related organization.
        relCollectedFromDatasourceId (str | None): ID of the datasource from which this was collected.
        logicalOperator (Literal["AND", "OR"] | None): How multiple filters are combined (default: AND).


    """

    search: str | None = None
    title: str | None = None
    keywords: list[str] | None = None
    id: str | None = None
    code: str | None = None
    grantID: str | None = None
    acronym: str | None = None
    callIdentifier: str | None = None
    fundingShortName: str | None = None
    fundingStreamId: str | None = None
    fromStartDate: date | None = None
    toStartDate: date | None = None
    fromEndDate: date | None = None
    toEndDate: date | None = None
    relOrganizationName: str | None = None
    relOrganizationId: str | None = None
    relCommunityId: str | None = None
    relOrganizationCountryCode: str | None = None
    relCollectedFromDatasourceId: str | None = None
    logicalOperator: Literal["AND", "OR"] | None = None

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
    from_date: date | None = Field(default=None, alias="from")  # API uses "from"
    to_date: date | None = Field(default=None, alias="to")  # API uses "to"

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class LinksFilters(BaseModel):
    """Filter model for Graph API /researchProducts/links endpoint.

    These filters are for the Graph API's built-in link retrieval endpoint,
    which is separate from the Scholix API. Parameters accept singular string values
    (unlike other Graph API filters which accept arrays).

    Reference: https://api.openaire.eu/graph/v1/researchProducts/links
    """

    sourcePid: str | None = Field(default=None, description="Filter by source persistent identifier (e.g. DOI)")
    targetPid: str | None = Field(default=None, description="Filter by target persistent identifier")
    sourcePublisher: str | None = Field(default=None, description="Filter by source publisher name")
    targetPublisher: str | None = Field(default=None, description="Filter by target publisher name")
    sourceType: str | None = Field(default=None, description="Filter by source type: publication, dataset, software, other")
    targetType: str | None = Field(default=None, description="Filter by target type: publication, dataset, software, other")
    relation: str | None = Field(default=None, description="Filter by specific relationship type")
    fromDate: str | None = Field(default=None, description="From date (YYYY or YYYY-MM-DD)")
    toDate: str | None = Field(default=None, description="To date (YYYY or YYYY-MM-DD)")

    model_config = ConfigDict(extra="forbid")


class PersonsFilters(BaseModel):
    """Filter model for Persons API endpoint.

    Note: The OpenAIRE API accepts 'givenName' and 'lastName' as filter parameters,
    but they currently cause HTTP 500 errors from the server. Only 'search', 'id',
    and 'originalId' work reliably. These params are kept for forward compatibility.

    Attributes:
        search (str | None): Keyword search for the person.
        id (str | None): OpenAIRE identifier.
        originalId (str | None): Original identifier (e.g. ORCID).
        givenName (str | None): Person's given (first) name. CAUTION: causes API 500.
        lastName (str | None): Person's family (last) name. CAUTION: causes API 500.
        logicalOperator (Literal["AND", "OR"] | None): How multiple filters are combined.
    """

    search: str | None = None
    id: str | None = None
    originalId: str | None = None
    givenName: str | None = None
    lastName: str | None = None
    logicalOperator: Literal["AND", "OR"] | None = None

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
        "sort": {
            "relevance": {},
            "startDate": {},
            "endDate": {},
        },
    },
    SCHOLIX: {
        "filters_model": ScholixFilters,
        "sort": {},
    },
}
