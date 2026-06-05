# Links

The Links endpoint provides access to relation links between research products
via the OpenAIRE Graph API (`/researchProducts/links`).

Unlike other endpoints, there is no standalone `LinksClient`. Link operations are
accessed through the **ResearchProductsClient**:

- `search_links()` — search for relation links between research products
- `iterate_links()` — iterate through all matching relation links
- `get_relations_info()` — retrieve available relation types

## LinksFilters

::: aireloom.endpoints.LinksFilters
    options:
      members: true
      show_docstring_description: true

## Access via ResearchProductsClient

::: aireloom.resources.research_products_client.ResearchProductsClient
    options:
      members:
        - search_links
        - iterate_links
        - get_relations_info
