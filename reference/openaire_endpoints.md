
# Endpoints
Base url: https://api.openaire.eu/graph/

Research products endpoint: /researchProducts
Organizations endpoint: /organizations
Data sources endpoint: /dataSources
Projects endpoint: /projects

# Examples


Get research products that contain both "climate" and "change":

[https://api.openaire.eu/graph/researchProducts?search=climate%20AND%20change](https://api.openaire.eu/graph/researchProducts?search=climate%20AND%20change)

Get research products that are classified with both Fields of Study (FOS) "03 medical and health sciences" and "0502 economics and business":

[https://api.openaire.eu/graph/researchProducts?fos="03 medical and health sciences" AND "0502 economics and business"](https://api.openaire.eu/graph/researchProducts?fos=%2203%20medical%20and%20health%20sciences%22%20AND%20%220502%20economics%20and%20business%22)

Get research products with the OpenAIRE ids doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108 or pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0:

[https://api.openaire.eu/graph/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0](https://api.openaire.eu/graph/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0)

Get projects that are connected to organizations in the US or Greece:

[https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US%20OR%20GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US%20OR%20GR)

or by using the same query parameter multiple times: [https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR)

or just using commas:
[https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US,GR](https://api.openaire.eu/graph/projects?relOrganizationCountryCode=US,GR)

Get research products that contain "semantic" but not "web":

[https://api.openaire.eu/graph/researchProducts?search=semantic%20NOT%20web](https://api.openaire.eu/graph/researchProducts?search=semantic%20NOT%20web)

Get all data sources that are not journals:

[https://api.openaire.eu/graph/dataSources?dataSourceTypeName=NOT%20Journal](https://api.openaire.eu/graph/dataSources?dataSourceTypeName=NOT%20Journal)

Get research products published after 2020-01-01 and sort them by the publication date in descending order:

[https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC](https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)

Get research products with the keyword "COVID-19" and sort them by their (citation-based) popularity:
[https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC](https://api.openaire.eu/graph/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)






# Response format

{
    header: {
        numFound: 36818386,
        maxScore: 1,
        queryTime: 21,
        page: 1,
        pageSize: 10
        nextCursor: "AoI/D2M2NGU1YjVkNTQ4Nzo6NjlmZTBmNjljYzM4YTY1MjI5YjM3ZDRmZmIyMTU1NDAIP4AAAA=="   // note: only when cursor-based paging is active
    },
    results: [
        ...
    ]
}

# Parameters

## Sorting

`sortBy`:
    Defines the field and the sort direction. The format should be `fieldname` `sortDirection`, where the `sortDirection` can be either `ASC` or D`ESC.
    The default sorting is based on the relevance score of the search results.
    Valid values for `fieldname` depends on the endpoint:
    `researchProducts`: relevance, publicationDate, dateOfCollection, influence, popularity, citationCount, impulse
    `organizations`: relevance
    `dataSources`: relevance
    `projects`: relevance, startDate, endDate

## Paging
### Up to 10000 records

`page`:
    Specifies the page number of the results you want to retrieve. Page numbering starts from 1.
`pageSize`:
    Defines the number of results to be returned per page. This helps limit the amount of data returned in a single request, making it easier to process.

### Cursor based (no maximum)
`cursor`:
    initial value is `*`. response.header.nextCursor holds the value for the next set of results.

# Filters

Filters can be combined without limit. By default multiple filter params are joined using `AND`. `OR` and `NOT` operators are available.

Each endpoint has a specific set of valid filters.

## Research Products

`search`
    Search in the content of the research product.
`mainTitle`
	Search in the research product's main title.
`description`
	Search in the research product's description.
`id`
	The OpenAIRE id of the research product.
`pid`
	The persistent identifier of the research product.
`originalId`
	The identifier of the record at the original sources.
`type`
	The type of the research product. One of publication, dataset, software, or other
`fromPublicationDate`
	Gets the research products whose publication date is greater than or equal to the given date. A date formatted as `ΥΥΥΥ` or `YYYY-MM-DD`
`toPublicationDate`
	Gets the research products whose publication date is less than or equal to the given date. A date formatted as `YYYY` or `YYYY-MM-DD`
`subjects`
	List of subjects associated to the research product.
`countryCode`
	The country code for the country associated with the research product.
`authorFullName`
	The full name of the authors involved in producing this research product.
`authorOrcid`
	The ORCiD of the authors involved in producing this research product.
`publisher`
	The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource.
`bestOpenAccessRightLabel`
	The best open access rights among the research product's instances. One of `OPEN SOURCE`, `OPEN`, `EMBARGO`, `RESTRICTED`, `CLOSED`, `UNKNOWN`
`influenceClass`
	Citation-based indicator that reflects the overall impact of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of influence respectively.
`impulseClass`
	Citation-based indicator that reflects the initial momentum of a research product directly after its publication. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of impulse respectively
`popularityClass`
	Citation-based indicator that reflects current impact or attention of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of popularity respectively.
`citationCountClass`
	Citation-based indicator that reflects the overall impact of a research product by summing all its citations. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of citation count respectively.
`instanceType`
    [Only for publications]	Retrieve publications of the given instance type. Check [here](https://api.openaire.eu/vocabularies/dnet:publication_resource) for all possible instance type values.
`sdg`
    [Only for publications]	Retrieves publications classified with the respective Sustainable Development Goal number. Integer in the range `[1, 17]`
`fos`
    [Only for publications]	Retrieves publications classified with a given Field of Science (FOS). A FOS classification identifier (see [here](https://explore.openaire.eu/assets/common-assets/vocabulary/fos.json) for details).
`isPeerReviewed`
    [Only for publications]	Indicates whether the publications are peerReviewed or not. (Boolean)
`isInDiamondJournal`
    [Only for publications]	Indicates whether the publication was published in a diamond journal or not. (Boolean)
`isPubliclyFunded`
    [Only for publications]	Indicates whether the publication was publicly funded or not. (Boolean)
`isGreen`
    [Only for publications]	Indicates whether the publication was published following the green open access model. (Boolean)
`openAccessColor`
    [Only for publications]	Specifies the Open Access color of the publication. One of `bronze`, `gold`, or `hybrid`
`relOrganizationId`
    Retrieve research products connected to the organization (with OpenAIRE id).
`relCommunityId`
    Retrieve research products connected to the community (with OpenAIRE id).
`relProjectId`
    Retrieve research products connected to the project (with OpenAIRE id).
`relProjectCode`
    Retrieve research products connected to the project with code.
`hasProjectRel`
    Retrieve research products that are connected to a project. (Boolean)
`relProjectFundingShortName`
    Retrieve research products connected to a project that has a funder with the given short name.
`relProjectFundingStreamId`
    Retrieve research products connected to a project that has the given funding identifier.
`relHostingDataSourceId`
    Retrieve research products hosted by the data source (with OpenAIRE id).
`relCollectedFromDatasourceId`
    Retrieve research products collected from the data source (with OpenAIRE id).

# Organizations

`search`
	Search in the content of the organization.
`legalName`
	The legal name of the organization.
`legalShortName`
	The legal name of the organization in short form.
`id`
	The OpenAIRE id of the organization.
`pid`
	The persistent identifier of the organization.
`countryCode`
	The country code of the organization.
`relCommunityId`
	Retrieve organizations connected to the community (with OpenAIRE id).
`relCollectedFromDatasourceId`
	Retrieve organizations collected from the data source (with OpenAIRE id).

# Data sources

`search`
	Search in the content of the data source.
`officialName`
	The official name of the data source.
`englishName`
	The English name of the data source.
`legalShortName`
	The legal name of the organization in short form.
`id`
	The OpenAIRE id of the data source.
`pid`
	The persistent identifier of the data source.
`subjects`
	List of subjects associated to the datasource.
`dataSourceTypeName`
	The data source type; see all possible values here .
`contentTypes`
	Types of content in the data source, as defined by OpenDOAR.
`relOrganizationId`
	Retrieve data sources connected to the organization (with OpenAIRE id).
`relCommunityId`
	Retrieve data sources connected to the community (with OpenAIRE id).
`relCollectedFromDatasourceId`
	Retrieve data sources collected from the data source (with OpenAIRE id).

# Projects

`search`
	Search in the content of the projects.
`title`
	Search in the project's title.
`keywords`
	The project's keywords.
`id`
	The OpenAIRE id of the project.
`code`
	The grant agreement (GA) code of the project.
`acronym`
	Project's acronym.
`callIdentifier`
	The identifier of the research call.
`fundingShortName`
	The short name of the funder.
`fundingStreamId`
	The identifier of the funding stream.
`fromStartDate`
	Gets the projects with start date greater than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`toStartDate`
	Gets the projects with start date less than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`fromEndDate`
	Gets the projects with end date greater than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`toEndDate`
	Gets the projects with end date less than or equal to the given date. Please provide a date formatted as YYYY or YYYY-MM-DD.
`relOrganizationName`
	The name or short name of the related organization.
`relOrganizationId`
	The organization identifier of the related organization.
`relCommunityId`
	Retrieve projects connected to the community (with OpenAIRE id).
`relOrganizationCountryCode`
	The country code of the related organizations.
`relCollectedFromDatasourceId`
	Retrieve projects collected from the data source (with OpenAIRE id).
