Version: 10.2.0

## Filtering search results

Filters can be used to narrow down the search results based on specific criteria. Filters are provided as query parameters in the request URL (see [here](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/) for the available search entpoints).

Multiple filters can be provided in a single request; they should be formatted as follows:`param1=value1&param2=value2&...&paramN=valueN`.

Examples:

- Get all research products that contain the word `"covid"`, sorted by popularity in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?search=covid&sortBy=popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=covid&sortBy=popularity%20DESC)
- Get all publications that are published after `2019-01-01`:
	[https://api.openaire.eu/graph/v1/researchProducts?type=publication&fromPublicationDate=2019-01-01](https://api.openaire.eu/graph/v1/researchProducts?type=publication&fromPublicationDate=2019-01-01)
- Get the organization with the ROR id `https://ror.org/0576by029`:
	[https://api.openaire.eu/graph/v1/organizations?pid=https://ror.org/0576by029](https://api.openaire.eu/graph/v1/organizations?pid=https://ror.org/0576by029)

## Available parameters

This section provides an overview of the available parameters for each entity type.

### Research products

The following query parameters are available for research products:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the research product. |
| **mainTitle** | Search in the research product's main title. |
| **description** | Search in the research product's description. |
| **id** | The OpenAIRE id of the research product. |
| **pid** | The persistent identifier of the research product. |
| **originalId** | The identifier of the record at the original sources. |
| **type** | The type of the research product. One of `publication`, `dataset`, `software`, or `other` |
| **fromPublicationDate** | Gets the research products whose publication date is greater than or equal to the given date. A date formatted as `ΥΥΥΥ` or `YYYY-MM-DD` |
| **toPublicationDate** | Gets the research products whose publication date is less than or equal to the given date. A date formatted as `YYYY` or `YYYY-MM-DD` |
| **subjects** | List of subjects associated to the research product. |
| **countryCode** | The country code for the country associated with the research product. |
| **authorFullName** | The full name of the authors involved in producing this research product. |
| **authorOrcid** | The ORCiD of the authors involved in producing this research product. |
| **publisher** | The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. |
| **bestOpenAccessRightLabel** | The best open access rights among the research product's instances. One of `OPEN SOURCE`, `OPEN`, `EMBARGO`, `RESTRICTED`, `CLOSED`, `UNKNOWN` |
| **influenceClass** | Citation-based indicator that reflects the overall impact of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of influence respectively. |
| **impulseClass** | Citation-based indicator that reflects the initial momentum of a research product directly after its publication. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of impulse respectively |
| **popularityClass** | Citation-based indicator that reflects current impact or attention of a research product. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of popularity respectively. |
| **citationCountClass** | Citation-based indicator that reflects the overall impact of a research product by summing all its citations. Please, choose a class among `C1`, `C2`, `C3`, `C4`, or `C5` for top 0.01%, top 0.1%, top 1%, top 10%, and average in terms of citation count respectively. |
| **instanceType** `[Only for publications]` | Retrieve publications of the given instance type. Check [here](http://api.openaire.eu/vocabularies/dnet:publication_resource) for all possible instance type values. |
| **sdg** `[Only for publications]` | Retrieves publications classified with the respective Sustainable Development Goal number. Integer in the range \[1, 17\] |
| **fos** `[Only for publications]` | Retrieves publications classified with a given Field of Science (FOS). A FOS classification identifier (see [here](https://explore.openaire.eu/assets/common-assets/vocabulary/fos.json) for details). |
| **isPeerReviewed** `[Only for publications]` | Indicates whether the publications are peerReviewed or not. (Boolean) |
| **isInDiamondJournal** `[Only for publications]` | Indicates whether the publication was published in a diamond journal or not. (Boolean) |
| **isPubliclyFunded** `[Only for publications]` | Indicates whether the publication was publicly funded or not. (Boolean) |
| **isGreen** `[Only for publications]` | Indicates whether the publication was published following the green open access model. (Boolean) |
| **openAccessColor** `[Only for publications]` | Specifies the Open Access color of the publication. One of `bronze`, `gold`, or `hybrid` |
| **relOrganizationId** | Retrieve research products connected to the organization (with OpenAIRE id). |
| **relCommunityId** | Retrieve research products connected to the community (with OpenAIRE id). |
| **relProjectId** | Retrieve research products connected to the project (with OpenAIRE id). |
| **relProjectCode** | Retrieve research products connected to the project with code. |
| **hasProjectRel** | Retrieve research products that are connected to a project. (Boolean) |
| **relProjectFundingShortName** | Retrieve research products connected to a project that has a funder with the given short name. |
| **relProjectFundingStreamId** | Retrieve research products connected to a project that has the given funding identifier. |
| **relHostingDataSourceId** | Retrieve research products hosted by the data source (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve research products collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. (Boolean) |
| **page** | Page number of the results. (Integer) |
| **pageSize** | Number of results per page. Integer in the range \[1, 100\] |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order and `fielaname` is one of `relevance`, `publicationDate`, `dateOfCollection`, `influence`, `popularity`, `citationCount`, `impulse`. Multiple sorting parameters should be comma-separated. |

### Organizations

The following query parameters are available for organizations:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the organization. |
| **legalName** | The legal name of the organization. |
| **legalShortName** | The legal name of the organization in short form. |
| **id** | The OpenAIRE id of the organization. |
| **pid** | The persistent identifier of the organization. |
| **countryCode** | The country code of the organization. |
| **relCommunityId** | Retrieve organizations connected to the community (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve organizations collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order - organizations can only be sorted by `relevance`. |

### Data sources

The following query parameters are available for data sources:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the data source. |
| **officialName** | The official name of the data source. |
| **englishName** | The English name of the data source. |
| **legalShortName** | The legal name of the organization in short form. |
| **id** | The OpenAIRE id of the data source. |
| **pid** | The persistent identifier of the data source. |
| **subjects** | List of subjects associated to the datasource. |
| **dataSourceTypeName** | The data source type; see all possible values [here](https://api.openaire.eu/vocabularies/dnet:datasource_typologies). |
| **contentTypes** | Types of content in the data source, as defined by OpenDOAR. |
| **relOrganizationId** | Retrieve data sources connected to the organization (with OpenAIRE id). |
| **relCommunityId** | Retrieve data sources connected to the community (with OpenAIRE id). |
| **relCollectedFromDatasourceId** | Retrieve data sources collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order - data sources can only be sorted by `relevance`. |

### Projects

The following query parameters are available for projects:

| **Parameter** | **Description** |
| --- | --- |
| **search** | Search in the content of the projects. |
| **title** | Search in the project's title. |
| **keywords** | The project's keywords. |
| **id** | The OpenAIRE id of the project. |
| **code** | The grant agreement (GA) code of the project. |
| **acronym** | Project's acronym. |
| **callIdentifier** | The identifier of the research call. |
| **fundingShortName** | The short name of the funder. |
| **fundingStreamId** | The identifier of the funding stream. |
| **fromStartDate** | Gets the projects with start date greater than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **toStartDate** | Gets the projects with start date less than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **fromEndDate** | Gets the projects with end date greater than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **toEndDate** | Gets the projects with end date less than or equal to the given date. Please provide a date formatted as `YYYY` or `YYYY-MM-DD`. |
| **relOrganizationName** | The name or short name of the related organization. |
| **relOrganizationId** | The organization identifier of the related organization. |
| **relCommunityId** | Retrieve projects connected to the community (with OpenAIRE id). |
| **relOrganizationCountryCode** | The country code of the related organizations. |
| **relCollectedFromDatasourceId** | Retrieve projects collected from the data source (with OpenAIRE id). |
| **debugQuery** | Retrieve debug information for the search query. |
| **page** | Page number of the results. |
| **pageSize** | Number of results per page. |
| **cursor** | Cursor-based pagination. Initial value: `cursor=*` |
| **sortBy** | The field to set the sorting order of the results. Should be provided in the format `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order and `fielaname` is one of `relevance`, `startDate`, `endDate`. Multiple sorting parameters should be comma-separated. |

## Using logical operators

The API supports the use of logical operators `AND`, `OR`, and `NOT` to refine your search queries. These operators help you combine or exclude one or more values for a specific filter.

### AND operator

Use the `AND` operator to retrieve results that include all specified values. This narrows your search.

Examples:

- Get research products that contain both `"climate"` and `"change"`:
	[https://api.openaire.eu/graph/v1/researchProducts?search=climate AND change](https://api.openaire.eu/graph/v1/researchProducts?search=climate%20AND%20change)
- Get research products that are classified with both Fields of Study (FOS) `"03 medical and health sciences"` and `"0502 economics and business"`:
	[https://api.openaire.eu/graph/v1/researchProducts?fos="03 medical and health sciences" AND "0502 economics and business"](https://api.openaire.eu/graph/v1/researchProducts?fos=%2203%20medical%20and%20health%20sciences%22%20AND%20%220502%20economics%20and%20business%22)

### OR operator

Use the `OR` operator to retrieve results that include any of the specified terms. This broadens your search. The same functionality can be achieved by providing multiple times the same query parameter or using a comma to separate the values.

Examples:

- Get research products with the OpenAIRE ids `doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108` or `pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0`:
	[https://api.openaire.eu/graph/v1/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1 OR pmid\_dedup\_\_::1591ebf0e0698ed4a99455ff2ba4adc0](https://api.openaire.eu/graph/v1/researchProducts?id=r3730f562f9e::539da48b3796663b17e6166bb966e5b1%20OR%20pmid_dedup__::1591ebf0e0698ed4a99455ff2ba4adc0)
- Get projects that are connected to organizations in the US or Greece:
	[https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US OR GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US%20OR%20GR)
	or by using the same query parameter multiple times: [https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US&relOrganizationCountryCode=GR)
	or just using comma: [https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US,GR](https://api.openaire.eu/graph/v1/projects?relOrganizationCountryCode=US,GR)

### NOT operator

Use the `NOT` operator to exclude specific terms from your search results. This refines your search by filtering out unwanted results.

Examples:

- Get research products that contain `"semantic"` but not `"web"`:
	[https://api.openaire.eu/graph/v1/researchProducts?search=semantic NOT web](https://api.openaire.eu/graph/v1/researchProducts?search=semantic%20NOT%20web)
- Get all data sources that are not journals:
	[https://api.openaire.eu/graph/v1/dataSources?dataSourceTypeName=NOT Journal](https://api.openaire.eu/graph/v1/dataSources?dataSourceTypeName=NOT%20Journal)