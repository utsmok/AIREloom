The OpenAIRE Graph API allows you to sort and page through the results of your search queries. This enables you to retrieve the most relevant results and manage large result sets more effectively.

## Sorting[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#sorting "Direct link to heading")

Sorting based on specific fields, helps to retrieve data in the preferred order. Sorting is achieved using the `sortBy` parameter, which specifies the field and the direction (ascending or descending) for sorting.

- `sortBy`: Defines the field and the sort direction. The format should be `fieldname sortDirection`, where the `sortDirection` can be either `ASC` for ascending order or `DESC` for descending order.

The field names that can be used for sorting are specific to each entity type and can be found in the `sortBy` field values of the [available paremeters](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results#available-parameters).

Note that the default sorting is based on the `relevance` score of the search results.

Examples:

- Get research products published after `2020-01-01` and sort them by the publication date in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate DESC](https://api.openaire.eu/graph/v1/researchProducts?fromPublicationDate=2020-01-01&sortBy=publicationDate%20DESC)
- Get research products with the keyword `"COVID-19"` and sort them by their (citation-based) popularity:
	[https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=popularity%20DESC)

Note that you can combine multiple sorting conditions by separating them with a comma.

Example:

- Get research products with the keyword `"COVID-19"` and sort them by their publication date in ascending order and then by their popularity in descending order:
	[https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=publicationDate ASC,popularity DESC](https://api.openaire.eu/graph/v1/researchProducts?search=COVID-19&sortBy=publicationDate%20ASC,popularity%20DESC)

## Paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#paging "Direct link to heading")

The OpenAIRE Graph API supports basic and cursor-based pagination. In basic pagination, `page` and `pageSize` parameters are used, enabling you to specify which part of the result set to retrieve and how many results per page.

### Offset-based paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#offset-based-paging "Direct link to heading")

Offset-based paging should be used to retrieve a small dataset only (up to 10000 records).

- `page`: Specifies the page number of the results you want to retrieve. Page numbering starts from 1.
- `pageSize`: Defines the number of results to be returned per page. This helps limit the amount of data returned in a single request, making it easier to process.

Example:

- Get the top 10 most influential research products that contain the phrase "knowledge graphs":
	[https://api.openaire.eu/graph/v1/researchProducts?search="knowledge graphs"&page=1&pageSize=10&sortBy=influence DESC](https://api.openaire.eu/graph/v1/researchProducts?search=%22knowledge%20graphs%22&page=1&pageSize=10&sortBy=influence%20DESC)

response:

```
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        page: 1,        pageSize: 10    },    results: [        ...    ]}
```

### Cursor-based paging[​](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/#cursor-based-paging "Direct link to heading")

Cursor should be used when it is required to retrieve a big dataset (more than 10000 records).

- `cursor`: Cursor-based pagination. Initial value: `cursor=*`.

Example:

- [https://api.openaire.eu/graph/v1/researchProducts?search="knowledge graphs"&pageSize=10&cursor=\*&sortBy=influence DESC](https://api.openaire.eu/graph/v1/researchProducts?search=%22knowledge%20graphs%22&pageSize=10&cursor=*&sortBy=influence%20DESC)

response:

```
{    header: {        numFound: 36818386,        maxScore: 1,        queryTime: 21,        pageSize: 10,        nextCursor: "AoI/D2M2NGU1YjVkNTQ4Nzo6NjlmZTBmNjljYzM4YTY1MjI5YjM3ZDRmZmIyMTU1NDAIP4AAAA=="    },    results: [        ...    ]}
```

Use `nextCursor` value, to get the next page of results.

[

](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/filtering-search-results)