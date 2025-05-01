
# AIREloom: An Asynchronous Python Client for OpenAIRE APIs

AIREloom provides a modern, asynchronous interface to interact with the OpenAIRE Graph API and Scholexplorer API, leveraging `httpx` and `pydantic` for robust and efficient data retrieval.

## Features

*   Asynchronous requests using `httpx`.
*   Built-in retry logic for transient network errors and rate limits.
*   Support for multiple authentication strategies:
    *   No Authentication
    *   Static API Token
    *   OAuth2 Client Credentials
*   Pydantic models for response validation and easy data access.
*   Methods for fetching single entities, searching with filters/sorting, and efficient iteration over large result sets using cursor pagination.
*   Interaction with both OpenAIRE Graph API (Research Products, Projects, Organizations, Data Sources) and Scholexplorer API (Scholix links).
*   Configurable via environment variables or `.env` files.


## Installation
Install the `aireloom` package from PyPI, preferably using uv:

```bash
> uv add aireloom
# or
> uv pip install aireloom
```


## Authentication

AIREloom automatically detects the authentication method based on your configuration (environment variables or `.env` file) unless you explicitly provide an `auth_strategy`.

**Environment Variables / `.env` file:**

Create a `.env` or `secrets.env` file in your project root. Prefix environment variables with `AIRELOOM_`.

*   **Static Token:** Set `AIRELOOM_OPENAIRE_API_TOKEN`.
    ```dotenv
    AIRELOOM_OPENAIRE_API_TOKEN="your_static_api_token_here"
    ```
*   **Client Credentials:** Set `AIRELOOM_OPENAIRE_CLIENT_ID` and `AIRELOOM_OPENAIRE_CLIENT_SECRET`. The token URL defaults to the standard OpenAIRE one but can be overridden with `AIRELOOM_OPENAIRE_TOKEN_URL`.
    ```dotenv
    AIRELOOM_OPENAIRE_CLIENT_ID="your_client_id_here"
    AIRELOOM_OPENAIRE_CLIENT_SECRET="your_client_secret_here"
    # AIRELOOM_OPENAIRE_TOKEN_URL="https://custom.token.url/oauth/token" # Optional override
    ```

**Explicit Strategy:**

You can pass an authentication strategy instance directly when creating `AireloomSession`.

```python
import asyncio
from aireloom import AireloomSession
from aireloom.auth import NoAuth, StaticTokenAuth, ClientCredentialsAuth

# 1. No Authentication
no_auth_session = AireloomSession(auth_strategy=NoAuth())

# 2. Static Token
token_auth_session = AireloomSession(auth_strategy=StaticTokenAuth(token="your_token"))

# 3. Client Credentials (reads ID/Secret/URL from env unless provided)
# Ensure AIRELOOM_OPENAIRE_CLIENT_ID and AIRELOOM_OPENAIRE_CLIENT_SECRET are set
cc_auth_session = AireloomSession(
    auth_strategy=ClientCredentialsAuth(
        client_id=None, # Or provide directly: "your_id"
        client_secret=None, # Or provide directly: "your_secret"
        token_url=None # Or provide directly: "your_token_url"
    )
)

# If no strategy is provided, it defaults based on environment variables:
default_session = AireloomSession() # Will use CC if ID/Secret found, then Token, then NoAuth

async def main():
    # Use the session within an async context
    async with default_session as session:
        # ... make API calls ...
        print("Session created with default auth.")
        pass

# Example of running the main function
# if __name__ == "__main__":
#     asyncio.run(main())
```

## Basic Usage: `AireloomSession`

The primary way to interact with the APIs is through `AireloomSession`.

```python
import asyncio
from aireloom import AireloomSession
from aireloom.auth import NoAuth # Or other auth strategies
from aireloom.exceptions import AireloomError

async def run_example():
    # Initialize with desired auth strategy (or let it auto-detect)
    # Use async with for proper client setup and teardown
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        # Example: Get a specific research product
        try:
            # Use a known OpenAIRE ID for a research product
            product_id = "doi_________::001857a5236493680133d59f11040d0f"
            print(f"Attempting to fetch product with ID: {product_id}")
            product = await session.get_research_product(product_id)
            print(f"Fetched Product: {product.mainTitle}")
            # Example of accessing nested Pydantic model data safely
            doi_value = product.get_pid_value('doi') # Helper method in BaseEntity
            print(f"  DOI: {doi_value if doi_value else 'Not available'}")
            print(f"  Type: {product.type}")
            print(f"  Publication Date: {product.publicationDate}")

        except AireloomError as e:
            print(f"An API or client error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run_example())
```

## Retrieving Single Entities

Use the `get_<entity_type>` methods with the OpenAIRE ID of the entity.

```python
import asyncio
from aireloom import AireloomSession, NoAuth
from aireloom.exceptions import AireloomError

async def get_entities():
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        try:
            # Get Research Product by OpenAIRE ID
            product_id = "doi_________::001857a5236493680133d59f11040d0f"
            print(f"\nFetching Product ID: {product_id}")
            product = await session.get_research_product(product_id)
            print(f"-> Product '{product.mainTitle}' fetched.")

            # Get Organization by OpenAIRE ID
            org_id = "openorgs____::5eab9d1a3b6f48762a0c0081" # Example: CERN
            print(f"\nFetching Organization ID: {org_id}")
            org = await session.get_organization(org_id)
            print(f"-> Organization '{org.legalName}' fetched.")

            # Get Project by OpenAIRE ID
            project_id = "corda_______::ec48e31594a6f1cad6678d1cad11e00a" # Example H2020 project
            print(f"\nFetching Project ID: {project_id}")
            project = await session.get_project(project_id)
            print(f"-> Project '{project.title}' fetched.")

            # Get Data Source by OpenAIRE ID
            source_id = "openaire____::0abf5ad011718363c13b04c10188f110" # Example: Zenodo
            print(f"\nFetching Data Source ID: {source_id}")
            source = await session.get_data_source(source_id)
            print(f"-> Data Source '{source.officialName}' fetched.")

        except AireloomError as e:
            # Specific handling for not found or other API errors
            print(f"Error fetching entity: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status Code: {e.response.status_code}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(get_entities())
```

## Searching Entities

Use the `search_<entity_type>` methods. These support pagination, sorting, and filtering.

```python
import asyncio
from aireloom import AireloomSession, NoAuth
from aireloom.exceptions import AireloomError, ValidationError

async def search_entities():
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        try:
            # Search Research Products (publications) with filters and sorting
            print("\nSearching Research Products...")
            search_response = await session.search_research_products(
                page=1,
                page_size=5,
                sort_by="publicationDate desc", # Sort by publication date, newest first
                type="publication",             # Filter by type
                countryCode="NL",               # Filter by country code
                isPeerReviewed="true"           # Filter boolean (accepts string/bool)
                # Example: search="climate change" # Add a full-text search term
            )

            print(f"Found {search_response.header.total} products matching criteria.")
            print(f"Showing page {search_response.header.page} of results (up to {search_response.header.pageSize}):")
            if search_response.results:
                for product in search_response.results:
                    print(f"- {product.mainTitle} ({product.publicationDate}) - DOI: {product.get_pid_value('doi')}")
            else:
                print("No products found for this page/filter combination.")

            # Search Projects
            print("\nSearching Projects...")
            project_response = await session.search_projects(
                page=1,
                page_size=3,
                keywords="artificial intelligence" # Filter by keyword(s)
                # Example: sort_by="endDate desc"
            )
            print(f"Found {project_response.header.total} projects.")
            if project_response.results:
                for project in project_response.results:
                    print(f"- {project.title} (Acronym: {project.acronym}, ID: {project.id})")
            else:
                print("No projects found.")

        except ValidationError as e:
            print(f"Invalid search parameters: {e}")
        except AireloomError as e:
            print(f"API Error during search: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during search: {e}")

if __name__ == "__main__":
    asyncio.run(search_entities())
```

**Filtering:** Pass filter criteria as keyword arguments to the `search_` methods. Valid filter keys depend on the entity type (see `aireloom/endpoints.py` or OpenAIRE documentation). The library attempts basic type conversion (e.g., string `"true"` to boolean `True`). If an invalid filter key is used, a `ValidationError` is raised.

**Sorting:** Use the `sort_by` parameter with the format `"field_name asc"` or `"field_name desc"`. Valid sort fields depend on the entity type. An invalid sort field raises a `ValidationError`.

**Pagination:** Use the `page` (1-indexed) and `page_size` parameters. The response object (`<EntityType>Response`) contains a `header` attribute with pagination information (`page`, `pageSize`, `total` results, `nextCursor`, etc.).

## Iterating Through All Results

For retrieving all results matching criteria without manual pagination, use the `iterate_<entity_type>` methods. These use efficient cursor-based pagination provided by the API.

```python
import asyncio
from aireloom import AireloomSession, NoAuth
from aireloom.exceptions import AireloomError, ValidationError

async def iterate_all_results():
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        print("\nIterating through recent Peer Reviewed publications from NL...")
        count = 0
        max_results_to_fetch = 15 # Limit for example purposes
        try:
            # Iterate through publications from the Netherlands, newest first
            async for product in session.iterate_research_products(
                page_size=5, # How many to fetch per underlying API call (adjust as needed)
                sort_by="publicationDate desc", # Get newest first
                countryCode="NL",
                type="publication",
                isPeerReviewed=True
            ):
                count += 1
                print(f"#{count}: {product.mainTitle} ({product.publicationDate})")
                if count >= max_results_to_fetch:
                    print(f"\nStopping iteration early after fetching {max_results_to_fetch} results.")
                    break
            print(f"\nFinished iterating. Total fetched in this run: {count}")

        except ValidationError as e:
            print(f"Invalid parameters for iteration: {e}")
        except AireloomError as e:
            print(f"API Error during iteration: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during iteration: {e}")

if __name__ == "__main__":
    asyncio.run(iterate_all_results())
```

**Note:** Iteration fetches results in batches (`page_size`) using the API's cursor mechanism until all matching entities are retrieved or the iteration is explicitly broken (as shown in the example).

## Working with Scholexplorer (Scholix Links)

Use `search_scholix_links` to find relationships (links) between research products (e.g., publications citing datasets, software citing publications).

**Important:** You *must* provide either `sourcePid` or `targetPid` for Scholix searches. PIDs should typically be DOIs or other persistent identifiers recognized by Scholexplorer.

```python
import asyncio
from aireloom import AireloomSession, NoAuth
from aireloom.exceptions import AireloomError, ValidationError

async def search_scholix():
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        print("\nSearching Scholix links...")
        try:
            # Find links where a specific DOI is the source
            # Using a known DOI that likely has citations/relations
            source_doi = "10.1038/s41586-021-03964-9" # Example Nature paper DOI
            print(f"Searching for links originating from PID: {source_doi}")

            scholix_response = await session.search_scholix_links(
                sourcePid=source_doi,
                page=0, # Scholexplorer uses 0-based pagination
                page_size=10 # Corresponds to 'rows' parameter in Scholexplorer
                # Example filters:
                # targetType="dataset",
                # relation="references"
            )

            print(f"Found {scholix_response.totalHits} links originating from {source_doi} (showing page {scholix_response.pageNumber}).")
            if scholix_response.results:
                for link in scholix_response.results:
                    target_id = link.target.identifier[0].id if link.target.identifier else 'N/A'
                    print(f"- Relation: {link.relationshipType.name} -> Target: {target_id} ({link.target.type.name})")
            else:
                print("No links found for this source PID on this page.")

            # Example: Find links targeting a specific PID
            target_doi = "10.5281/zenodo.3937230" # Example Zenodo dataset DOI
            print(f"\nSearching for links targeting PID: {target_doi}")
            scholix_target_response = await session.search_scholix_links(
                targetPid=target_doi,
                page_size=5
            )
            print(f"Found {scholix_target_response.totalHits} links targeting {target_doi}.")
            if scholix_target_response.results:
                 for link in scholix_target_response.results:
                    source_id = link.source.identifier[0].id if link.source.identifier else 'N/A'
                    print(f"- Source: {source_id} ({link.source.type.name}) -> Relation: {link.relationshipType.name}")
            else:
                print("No links found targeting this PID.")


        except ValueError as ve:
             print(f"Validation Error: {ve}") # e.g., missing sourcePid/targetPid
        except ValidationError as ve:
             print(f"Invalid Scholix filter parameter: {ve}")
        except AireloomError as e:
            print(f"API Error searching Scholix: {e}")
        except Exception as e:
            print(f"An unexpected error occurred searching Scholix: {e}")

if __name__ == "__main__":
    asyncio.run(search_scholix())
```

## Error Handling

AIREloom raises specific exceptions found in `aireloom.exceptions`:

*   `AireloomError`: Base exception for the library.
*   `APIError`: For non-success HTTP status codes (4xx, 5xx) from the API after retries. Contains the `response` and `request` objects.
*   `RateLimitError`: Subclass of `APIError` specifically for 429 status codes.
*   `TimeoutError`: For request timeouts after retries. Contains the `request` object.
*   `NetworkError`: For connection errors after retries. Contains the `request` object.
*   `AuthError`: For authentication failures (e.g., invalid credentials, token fetch failure).
*   `ConfigurationError`: For missing required configuration (e.g., missing token for `StaticTokenAuth`).
*   `ValidationError`: For invalid filter/sort parameters provided by the user.

Wrap API calls in `try...except` blocks to handle potential issues gracefully.

```python
import asyncio
from aireloom import AireloomSession, NoAuth
from aireloom.exceptions import (
    AireloomError, APIError, RateLimitError, TimeoutError, NetworkError, AuthError, ValidationError
)

async def error_handling_example():
    async with AireloomSession(auth_strategy=NoAuth()) as session:
        try:
            # Intentionally use an invalid filter key
            print("\nAttempting search with invalid filter...")
            await session.search_research_products(invalid_filter_key="some_value")
        except ValidationError as e:
            print(f"Caught expected validation error: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}")

        try:
            # Intentionally use a non-existent ID
            print("\nAttempting to fetch non-existent ID...")
            await session.get_research_product("nonexistent_id_________::12345")
        except APIError as e:
            print(f"Caught expected API error: Status {e.response.status_code if e.response else 'N/A'}")
            # Check for 404 Not Found specifically if needed
            if e.response and e.response.status_code == 404:
                print("  Resource not found (404).")
        except AireloomError as e:
            print(f"Caught other Aireloom error: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(error_handling_example())
```

## Advanced Usage

*   **Custom `httpx.AsyncClient`:** While `AireloomSession` manages its own internal `AireloomClient` (which in turn manages an `httpx.AsyncClient`), you can instantiate `AireloomClient` directly if you need to pass a pre-configured `httpx.AsyncClient` for fine-grained control over transport, proxies, event hooks, etc. However, you would then typically use this `AireloomClient` instance directly, bypassing the `AireloomSession` convenience layer.
*   **Override Settings:** You can configure client behavior (timeout, retries) via environment variables (see Authentication section) or by passing an `ApiSettings` instance when creating an `AireloomClient`.
*   **Direct Client Use:** You can use `AireloomClient` directly for making requests. This gives you the raw `httpx.Response` object. You would be responsible for parsing the JSON response and potentially validating it against Pydantic models yourself.

```python
import asyncio
import httpx
from aireloom.client import AireloomClient
from aireloom.auth import NoAuth
from aireloom.config import ApiSettings

# Example: Using a custom httpx client via AireloomClient
async def use_direct_client_with_custom_httpx():
    # Configure custom httpx settings
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    custom_http_client = httpx.AsyncClient(limits=limits, timeout=45.0)

    # Create AireloomClient, passing the custom httpx client
    # Note: AireloomClient will use this client instead of creating its own.
    # It will also *not* close this client automatically unless it created it.
    custom_settings = ApiSettings(request_timeout=45.0) # Match timeout if desired
    async with AireloomClient(
        auth_strategy=NoAuth(),
        http_client=custom_http_client,
        settings=custom_settings
    ) as client:
        try:
            print("\nMaking request with direct client and custom httpx client...")
            response = await client.request("GET", "researchProducts", params={"pageSize": 1})
            print(f"Direct client response status: {response.status_code}")
            # Manual parsing needed
            if response.status_code == 200:
                data = response.json()
                print(f"Successfully fetched {len(data.get('results', []))} product(s).")
            else:
                print(f"Request failed: {response.text}")
        except Exception as e:
            print(f"Error using direct client: {e}")
    # Remember to close the client you created manually
    await custom_http_client.aclose()
    print("Manually closed custom httpx client.")

if __name__ == "__main__":
    asyncio.run(use_direct_client_with_custom_httpx())

```
## Dev

This project uses `uv` for environment and dependency management.

```bash
> git clone github.com/utsmok/aireloom.git
> cd aireloom
> uv init
> uv sync --all-extras
```

run tests with `uv pytest`, format / lint with `uvx ruff format .` and `uvx ruff check --fix .`.


Contributions are welcome! Please follow standard practices like creating issues for bugs or feature requests, submitting pull requests with relevant tests, and adhering to the coding style enforced by Ruff (use `uvx ruff format .` and `uvx ruff check --fix .`).

## License

This project is licensed under the MIT License.
