This is a guide on how to retrieve detailed information on a single entity using the OpenAIRE Graph API.

## Endpoints[​](https://graph.openaire.eu/docs/apis/graph-api/#endpoints "Direct link to heading")

Currently, the Graph API supports the following entity types:

- Research products - endpoint: `GET /researchProducts/{id}`
- Organizations - endpoint: `GET /organizations/{id}`
- Data sources - endpoint: `GET /dataSources/{id}`
- Projects - endpoint: `GET /projects/{id}`

You can retrieve the data of a single entity by providing the entity's OpenAIRE identifier (id) in the corresponding endpoint. The OpenAIRE id is the primary key of an entity in the OpenAIRE Graph.

note

Note that if you want to retrieve multiple entities based on their OpenAIRE ids, you can use the [search endpoints and filter](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results#or-operator) by the `id` field using `OR`.

## Response[​](https://graph.openaire.eu/docs/apis/graph-api/#response "Direct link to heading")

The response of the Graph API is a [Research product](https://graph.openaire.eu/docs/data-model/entities/research-product), [Organization](https://graph.openaire.eu/docs/data-model/entities/organization), [Data Source](https://graph.openaire.eu/docs/data-model/entities/data-source), or [Project](https://graph.openaire.eu/docs/data-model/entities/project), depending on the endpoint used.

## Example[​](https://graph.openaire.eu/docs/apis/graph-api/#example "Direct link to heading")

In order to retrieve the research product with OpenAIRE id: `doi_dedup___::2b3cb7130c506d1c3a05e9160b2c4108`, you have to perform the following API call:

[https://api.openaire.eu/graph/v1/researchProducts/doi\_dedup\_\_\_::a55b42c0d32a4a24cf99e621623d110e](https://api.openaire.eu/graph/v1/researchProducts/doi_dedup___::a55b42c0d32a4a24cf99e621623d110e)

This will return all the data of the research product with the provided identifier:

```json
{  id: "doi_dedup___::a55b42c0d32a4a24cf99e621623d110e",  mainTitle: "OpenAIRE Graph Dataset",  description: [    "The OpenAIRE Graph is exported as several dataseta, so you can download the parts you are interested into. <strong>publication_[part].tar</strong>: metadata records about research literature (includes types of publications listed here)<br> <strong>dataset_[part].tar</strong>: metadata records about research data (includes the subtypes listed here) <br> <strong>software.tar</strong>: metadata records about research software (includes the subtypes listed here)<br> <strong>otherresearchproduct_[part].tar</strong>: metadata records about research products that cannot be classified as research literature, data or software (includes types of products listed here)<br> <strong>organization.tar</strong>: metadata records about organizations involved in the research life-cycle, such as universities, research organizations, funders.<br> <strong>datasource.tar</strong>: metadata records about data sources whose content is available in the OpenAIRE Graph. They include institutional and thematic repositories, journals, aggregators, funders' databases.<br> <strong>project.tar</strong>: metadata records about project grants.<br> <strong>relation_[part].tar</strong>: metadata records about relations between entities in the graph.<br> <strong>communities_infrastructures.tar</strong>: metadata records about research communities and research infrastructures Each file is a tar archive containing gz files, each with one json per line. Each json is compliant to the schema available at http://doi.org/10.5281/zenodo.8238874. The documentation for the model is available at https://graph.openaire.eu/docs/data-model/ Learn more about the OpenAIRE Graph at https://graph.openaire.eu. Discover the graph's content on OpenAIRE EXPLORE and our API for developers."  ],  type: "dataset",  publicationDate: "2023-08-08",  publisher: "Zenodo",  id: [    {      scheme: "Digital Object Identifier",      value: "10.5281/zenodo.8217359"    }  ],  // for brevity, the rest of the fields are omitted}
```

[

](https://graph.openaire.eu/docs/apis/graph-api/)