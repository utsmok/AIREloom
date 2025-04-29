This is a guide on how to search for specific entities using the OpenAIRE Graph API.

## Endpoints[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#endpoints "Direct link to heading")

Currently, the Graph API supports the following entity types:

- Research products - endpoint: [`GET /researchProducts`](https://api.openaire.eu/graph/v1/researchProducts)
- Organizations - endpoint: [`GET /organizations`](https://api.openaire.eu/graph/v1/organizations)
- Data sources - endpoint: [`GET /dataSources`](https://api.openaire.eu/graph/v1/dataSources)
- Projects - endpoint: [`GET /projects`](https://api.openaire.eu/graph/v1/projects)

Each of these endpoints can be used to list all entities of the corresponding type. Listing such entities can be more useful when using the [filtering](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results), [sorting](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#sorting), and [paging](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#paging) capabilities of the Graph API.

## Response[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#response "Direct link to heading")

The response of the aforementioned endpoints is an object of the following type:

```json
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        page: 1,        pageSize: 10    },    results: [        ...    ]}
```

It contains a `header` object with the following fields:

- `numFound`: the total number of entities found
- `maxScore`: the maximum relevance score of the search results
- `queryTime`: the time in milliseconds that the search took
- `page`: the current page of the search results (when using basic pagination)
- `pageSize`: the number of entities per page
- `nextCursor`: the next page cursor (when using cursor-based pagination, see: [paging](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging#paging)

Finally, the `results` field contains an array of entities of the corresponding type (i.e., [Research product](https://graph.openaire.eu/docs/data-model/entities/research-product), [Organization](https://graph.openaire.eu/docs/data-model/entities/organization), [Data Source](https://graph.openaire.eu/docs/data-model/entities/data-source), or [Project](https://graph.openaire.eu/docs/data-model/entities/project)).

[

](https://graph.openaire.eu/docs/apis/graph-api/getting-a-single-entity)