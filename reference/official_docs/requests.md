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


## Authentication & limits
The OpenAIRE APIs are free-to-use by any third-party service and can be accessed over HTTPS both by authenticated and unauthenticated requests. The rate limit for the former type of requests is up to 7200 requests per hour, while the latter is up to 60 requests per hour.

To make an authenticated request, you must first register. Then, you can go to the personal access token page in your account, copy your token and use it for up to one hour, find out more.

Our OAuth 2.0 implementation, conforms to the OpenID Connect specification, and is OpenID Certified. OpenID Connect is a simple identity layer on top of the OAuth 2.0 protocol. For more information about OAuth2.0 please visit the OAuth2.0 official site. For more information about OpenID Connect please visit the OpenID Connect official site. Also, check here for more information on our Privacy Policy.

### Quality of service
OpenAIRE API services are running in production 24/7 within the OpenAIRE infrastructure premises deployed at the data center facilities of the Interdisciplinary Centre for Mathematical and Computational Modelling (ICM).

### License
OpenAIRE Graph license is CC-BY: the records returned by the service can be freely re-used by commercial and non-commercial partners under CC-BY license, hence as long as OpenAIRE is acknowledged as a data source.


[

](https://graph.openaire.eu/docs/apis/graph-api/searching-entities/sorting-and-paging)