# Search API

The Search API allows developers to access metadata records of the OpenAIRE Graph by performing queries over research products (i.e., publications, data, software, other research products), and projects.

The API is intended for metadata discovery and exploration only, hence it does not provide access to the whole information space: the number of total results returned by one query is limited to 10,000.

For accessing the whole graph, developers are encouraged to use the OpenAIRE full Graph dataset.




## Endpoints[​](https://graph.openaire.eu/docs/apis/search-api/#endpoints "Direct link to heading")

For research products: [https://api.openaire.eu/search/researchProducts](https://api.openaire.eu/search/researchProducts)

By specific type:

- publications: [https://api.openaire.eu/search/publications](https://api.openaire.eu/search/publications)
- research data: [https://api.openaire.eu/search/datasets](https://api.openaire.eu/search/datasets)
- research software: [https://api.openaire.eu/search/software](https://api.openaire.eu/search/software)
- other research products: [https://api.openaire.eu/search/other](https://api.openaire.eu/search/other)

## General parameters[​](https://graph.openaire.eu/docs/apis/search-api/#general-parameters "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/researchProducts](https://api.openaire.eu/search/researchProducts)

| Parameter | Option | Description |
| --- | --- | --- |
| page | integer | Page number of the search results. |
| size | integer | Number of results per page. |
| format | json \| xml \| csv \| tsv | The format of the response. The default is xml. |
| model | openaire \| sygma | The data model of the response. Default is openaire. Model sygma is a simplified version of the openaire model. For sygma, only the xml format is available. The relative XML schema is available [here](https://www.openaire.eu/schema/sygma/oaf_sygma_v2.1.xsd). |
| sortBy | `sortBy=field,[ascending\\|descending]`   **'field'** can one of: - `dateofcollection` - `resultstoragedate` - `resultstoragedate` - `resultembargoenddate` - `resultembargoendyear` - `resultdateofacceptance` - `resultacceptanceyear` - `influence` - `popularity` - `citationCount` - `impulse` Multiple sorting is supported by repeating the `sortBy` parameter. | The sorting order of the specified field. |
| hasECFunding | true \| false | If hasECFunding is true gets the entities funded by the EC. If hasECFunding is false gets the entities related to projects not funded by the EC. |
| hasWTFunding | true \| false | If hasWTFunding is true gets the entities funded by Wellcome Trust. The results are the same as those obtained with `funder=wt`. If hasWTFunding is false gets the entities related to projects not funded by Wellcome Trust. |
| funder | WT \| EC \| ARC \| ANDS \| NSF \| FCT \| NHMRC | Search for entities by funder. |
| fundingStream | ... | Search for entities by funding stream. |
| FP7scientificArea | ... | Search for FP7 entities by scientific area. |
| keywords | White-space separated list of keywords. | This parameter is used to support a keyword search functionality in various fields (e.g., for research products the keywords are used to search in the product’s title, description, authors, etc). Regarding the semantics, when you provide multiple keywords, all keywords should be present, hence the correct interpretation is `kwd1 AND kw2`. |
| doi | Comma separated list of DOIs.   Alternatively, it is possible to repeat the parameter for each requested doi. | Gets the research products with the given DOIs, if any. |
| orcid | Comma separated list of ORCID iDs of authors.   Alternatively, it is possible to repeat the parameter for each author ORCID iD. | Gets the research products linked to the given ORCID iD of an author, if any. |
| fromDateAccepted | Date formatted as `YYYY-MM-DD` | Gets the research products whose date of acceptance is greater than or equal the given date. |
| toDateAccepted | Date formatted as `YYYY-MM-DD` | Gets the research products whose date of acceptance is less than or equal the given date. |
| title | White-space separated list of keywords. | Gets the research products whose titles contain the given list of keywords. |
| author | White-space separated list of names and/or surnames. | Search for research products by authors. |
| OA | true \| false | If OA is true gets Open Access research products. If OA is false gets the non Open Access research products |
| projectID | The given grant identifier of the project | Search for research products of the project with the specified projectID |
| country | 2 letter country code | Search for research products associated to the country code |
| influence | Accepted values:   `C1` for top 0.01% in terms of influence   `C2` for top 0.1% in terms of influence   `C3` for top 1% in terms of influence   `C4` for top 10% in terms of influence   `C5` for average/low in terms of influence      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?influence=C1&influence=C2` | Search for research products based on their influence. |
| popularity | Accepted values:   `C1` for top 0.01% in terms of popularity   `C2` for top 0.1% in terms of popularity   `C3` for top 1% in terms of popularity   `C4` for top 10% in terms of popularity   `C5` for average/low in terms of popularity      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?popularity=C1&popularity=C2` | Search for research products based on their popularity. |
| impulse | Accepted values:   `C1` for top 0.01% in terms of impulse   `C2` for top 0.1% in terms of impulse   `C3` for top 1% in terms of impulse   `C4` for top 10% in terms of impulse   `C5` for average/low in terms of impulse      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?impulse=C1&impulse=C2` | Search for research products based on their impulse. |
| citationCount | Accepted values:   `C1` for top 0.01% in terms of citation count   `C2` for top 0.1% in terms of citation count   `C3` for top 1% in terms of citation count   `C4` for top 10% in terms of citation count   `C5` for average/low in terms of citation count      Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?citationCount=C1&citationCount=C2` | Search for research products based on their number of citations. |
| openaireProviderID | Comma separated list of identifiers. | Search for research products by openaire data provider identifier.   Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. |
| openaireProjectID | Comma separated list of identifiers.   Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. | Search for research products by openaire project identifier. Alternatively, it is possible to repeat the parameter for each provider id. In both cases, provider identifiers will form a query with OR semantics. |
| hasProject | true \| false | If hasProject is true gets the research products that have a link to a project. If hasProject is false gets the publications with no links to projects. |
| FP7ProjectID | ... | Search for research products associated to a FP7 project with the given grant number. It is equivalent to a query by `funder=FP7&projectID={grantID}` |

## Parameters for publications[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-publications "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/publications](https://api.openaire.eu/search/publications)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| instancetype | Comma separated list of publication types. Check [here](http://api.openaire.eu/vocabularies/dnet:publication_resource) to see the possible values | Gets the publication of the given type, if any. |
| originalId | Comma separated list of original identifiers as we get them from the data source.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the publication with the given openaire identifier, if any. |
| sdg | The number of the Sustainable Development Goals `[1-17]`.   Check [here](https://sdgs.un.org/goals) to see the Sustainable Developemnt Goals. | Gets the publications that are classified with the respective Sustainable Development Goal number. |
| fos | The Field of Science classification value.   Check [here](https://graph.openaire.eu/docs/assets/files/athenarc_fos_hierarchy-3b6e1c7197e46bd3a3e9790115a8dec9.json) to see the Field of Science classification values | Gets the publications that are classified with the respective Field of Science classification value. |
| openairePublicationID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the publication with the given openaire identifier, if any. |
| peerReviewed | Accepted values:   true \| false | Specify if the publications are peerReviewed or not. |
| diamondJournal | Accepted values:   true \| false | Specify if the publications are published in a diamond journal or not. |
| publiclyFunded | Accepted values:   true \| false | Specify if the publications are publicly funded or not. |
| green | Accepted values:   true \| false | Specify if the publications are green open access or not. |
| openAccessColor | Accepted values:   `gold`\| `bronze`\| `hybrid`   Comma separated list of values or repeat of the parameter for each value will form a query with OR semantics, eg. `?openAccessColor=gold&openAccessColor=hybrid` | Specify the open access color of a publication. |

## Parameters for research data[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-research-data "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/datasets](https://api.openaire.eu/search/datasets)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireDatasetID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the research data with the given openaire identifier, if any. |

## Parameters for research software[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-research-software "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/software](https://api.openaire.eu/search/software)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireSoftwareID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the research software with the given openaire identifier, if any. |

## Parameters for other research products[​](https://graph.openaire.eu/docs/apis/search-api/#parameters-for-other-research-products "Direct link to heading")

Endpoint: [https://api.openaire.eu/search/other](https://api.openaire.eu/search/other)

You can use all the [general research products parameters](https://graph.openaire.eu/docs/apis/search-api/#general-parameters) as well as those in the following table.

| Parameter | Option | Description |
| --- | --- | --- |
| openaireOtherID | Comma separated list of OpenAIRE identifiers.   Alternatively, it is possible to repeat the parameter for each requested identifier. | Gets the other research products with the given openaire identifier, if any. |


## Searching for projects

## Endpoints

For research projects: [http://api.openaire.eu/search/projects](http://api.openaire.eu/search/projects)

## Parameters

| Parameter | Option | Description |
| --- | --- | --- |
| page | integer | Page number of the search results. |
| size | integer | Number of results per page. |
| format | json \| xml \| csv \| tsv | The format of the response. The default is xml. |
| model | openaire \| sygma | The data model of the response. Default is openaire. Model sygma is a simplified version of the openaire model. For sygma, only the xml format is available. The relative XML schema is available [here](https://www.openaire.eu/schema/sygma/oaf_sygma_v2.1.xsd). |
| sortBy | `sortBy=field,[ascending\\|descending]`; **'field'** is one of: `projectstartdate`, `projectstartyear`, `projectenddate`, `projectendyear`, `projectduration` | The sorting order of the specified field. |
| hasECFunding | true \| false | If hasECFunding is true gets the entities funded by the EC. If hasECFunding is false gets the entities related to projects not funded by the EC. |
| hasWTFunding | true \| false | If hasWTFunding is true gets the entities funded by Wellcome Trust. The results are the same as those obtained with `funder=wt`. If hasWTFunding is false gets the entities related to projects not funded by Wellcome Trust. |
| funder | WT \| EC \| ARC \| ANDS \| NSF \| FCT \| NHMRC | Search for entities by funder. |
| fundingStream | ... | Search for entities by funding stream. |
| FP7scientificArea | ... | Search for FP7 entities by scientific area. |
| keywords | White-space separated list of keywords. | N/A |
| sortBy | `sortBy=field,[ascending\\|descending]`; **'field'** is one of: `projectstartdate`, `projectstartyear`, `projectenddate`, `projectendyear`, `projectduration` | The sorting order of the specified field. |
| grantID | Comma separated list of grant identifiers. | Gets the project with the given grant identifier, if any. |
| openairePublicationID | Comma separated list of OpenAIRE identifiers. | Gets the publication with the given openaire identifier, if any. |
| name | White-space separated list of keywords. | Gets the projects whose names contain the given list of keywords. Using double quotes `"` you get an exact match, if any. |
| acronym | N/A | Gets the project with the given acronym, if any. |
| callID | N/A | Search for projects by call identifier. |
| startYear | Year formatted as `YYYY` | Gets the projects that started in the given year. |
| endYear | Year formatted as `YYYY`. | Gets the projects that ended in the given year. |
| participantCountries | Comma separeted list of 2 letter country codes. | Search for projects by participant countries. |
| participantAcronyms | White space separeted list of acronyms of institutions. | Search for projects by participant institutions. |

Version: 10.2.0

## Response metadata format

In this page, we elaborate on the metadata response format, as well as response headers and errors.

## Main response

The OpenAIRE Search API supports the following types of response formats:

- XML
- JSON
- CSV
- TSV

In the next paragraphs, we elaborate on the respective metadata formats.

### XML/JSON

The default format of delivered records is oaf (OpenAIRE Format - current version 1.0):

- XML schema: [https://www.openaire.eu/schema/1.0/oaf-1.0.xsd](https://www.openaire.eu/schema/1.0/oaf-1.0.xsd)
- Documentation: [https://www.openaire.eu/schema/1.0/doc/oaf-1.0.html](https://www.openaire.eu/schema/1.0/doc/oaf-1.0.html)

For the list of changes [click here](https://www.openaire.eu/openaire-xml-schema-change-announcement).

Note that latest versions of the XML schema and documentation are also available at the following permanent links:

- XML schema: [https://www.openaire.eu/schema/latest/oaf.xsd](https://www.openaire.eu/schema/latest/oaf.xsd)
- Documentation: [https://www.openaire.eu/schema/latest/doc/oaf.html](https://www.openaire.eu/schema/latest/doc/oaf.html)

Older versions:

- oaf v0.3 [XML schema](https://www.openaire.eu/schema/0.3/oaf-0.3.xsd) and [documentation](https://www.openaire.eu/schema/0.3/doc/oaf-0.3.html)
- oaf v0.2 [XML schema](https://www.openaire.eu/schema/0.2/oaf-0.2.xsd) and [documentation](https://www.openaire.eu/schema/0.2/doc/oaf-0.2.html)
- oaf v0.1 [XML schema](https://www.openaire.eu/schema/0.1/oaf-0.1.xsd) and [documentation](https://www.openaire.eu/schema/0.1/doc/oaf-0.1.html)

### CSV/TSV

The API returns in comma-separated files (CSV) or tab-separated files (TSV) the following fields:

- Title
- AUthors
- Publicatioy year
- DOI
- Download from
- Publication type
- Journal
- Funder
- Project name (GA Number)
- Access

## Headers

| Name | Description |
| --- | --- |
| x-ratelimit-limit | The maximum number of requests allowed for the client in one time window. |
| x-ratelimit-used | The number of requests already made by the client in the current time window. |

The OpenAIRE APIs use a sliding time window of one hour.

## Errors

### General

404 - Not found

```json
{
    "error": "Not found",
    "description": "Invald request path."
}
```

429 - Rate limit abuse

```json
{
    "error": "Too many requests",
    "description": "Request rate exceeded. Slow down."
}
```

### Only for authenticated requests

400 - Missing grant type

```json
{
    "error": "invalid_request",
    "error_description": "Missing grant type"
}
```

400 - Wrong grant type

```json
{
    "error": "unsupported_grant_type",
    "error_description": "Unsupported grant type: ..."
}
```

400 - Missing Refresh Token

```json
{  
    "status" : "error", 
    "code" : "400", 
    "message" : "Bad Request", 
    "description" : "Missing refreshToken parameter" 
}
```

401 - Missing username or/and password

```json
{
    "error": "unauthorized",
    "error_description": "Client id must not be empty!"
}
```

401 - Wrong username or/and password

```json
{
    "error": "unauthorized",
    "error_description": "Bad credentials"
}
```

401 - Invalid Refresh Token (for authenticated requests)

```json
{  
    "status" : "error", 
    "code" : "401", 
    "message" : "Unauthorised", 
    "description" : "Invalid refreshToken token" 
}
```

401 - Invalid client assertion

```json
{
    "error":"invalid_client",
    "error_description":"Bad client credentials"
}
```

401 - Client assertion for missing service

```json
{
    "error":"invalid_client",
    "error_description":"Could not find client {SERVICE_ID}"
}
```

401 - Expired signed jwt

```json
{
    "error":"unauthorized",
    "error_description":"Assertion Token in expired: {EXPIRATION_TIME}"
}
```

403 - Invalid Access Token
```json
{
    "error": "Token invalid",
    "description": "Authorization header value invalid."
}
```