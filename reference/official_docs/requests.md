This guide provides examples of how to make requests to the OpenAIRE Graph API using different programming languages.

## Using `curl`[​](https://graph.openaire.eu/docs/apis/graph-api/#using-curl "Direct link to heading")

```bash
curl -X GET "https://api.openaire.eu/graph/v1/researchProducts?search=OpenAIRE%20Graph&type=publication&page=1&pageSize=10&sortBy=relevance%20DESC" -H "accept: application/json"
```

## Using Python (with `requests` library)[​](https://graph.openaire.eu/docs/apis/graph-api/#using-python-with-requests-library "Direct link to heading")

```python
import requestsurl = "https://api.openaire.eu/graph/v1/researchProducts"params = {    "search": "OpenAIRE Graph",    "type": "publication",    "page": 1,    "pageSize": 10,    "sortBy": "relevance DESC"}headers = {    "accept": "application/json"}response = requests.get(url, headers=headers, params=params)if response.status_code == 200:    data = response.json()    print(data)else:    print(f"Failed to retrieve data: {response.status_code}")
```

note

Note that when using `curl` you should ensure that the URL is properly encoded, especially when using special characters or spaces in the query parameters. On the contrary, the `requests` library in Python takes care of URL encoding automatically.

[

](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging)