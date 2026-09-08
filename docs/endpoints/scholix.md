# Scholix

`ScholixClient` supports the current v3 API as well as the legacy v1 and v2
endpoints. Use `search_links()` and `iterate_links()` for v3 links; the
versioned helpers expose link-provider, publisher, data-source, KPI, and
legacy-link operations when compatibility with older Scholexplorer deployments
is required.

## ScholixFilters

::: aireloom.endpoints.ScholixFilters
    options:
      members: true
      show_docstring_description: true

## ScholixClient

::: aireloom.resources.scholix_client.ScholixClient
    options:
      members:
        - search
        - search_links
        - iterate_links
        - iterate
        - collect
        - count
        - first
