# API Reference

This section provides a basic API reference generated from the docstrings in the AIREloom library using `mkdocstrings`.

## `AireloomSession`

The main session class for interacting with AIREloom.

::: aireloom.session.AireloomSession
    options:
      members: true

## Resource Clients

Clients for specific OpenAIRE API endpoints.

### ResearchProductsClient

For accessing research products (publications, datasets, software, etc.) and
relation links.

::: aireloom.resources.research_products_client.ResearchProductsClient
    options:
      members:
        - search
        - iterate
        - get
        - collect
        - count
        - first
        - search_links
        - iterate_links
        - get_relations_info

### OrganizationsClient

For accessing organization data.

::: aireloom.resources.organizations_client.OrganizationsClient
    options:
      members:
        - search
        - iterate
        - get
        - collect
        - count
        - first

### ProjectsClient

For accessing research project data.

::: aireloom.resources.projects_client.ProjectsClient
    options:
      members:
        - search
        - iterate
        - get
        - collect
        - count
        - first

### DataSourcesClient

For accessing data source information.

::: aireloom.resources.data_sources_client.DataSourcesClient
    options:
      members:
        - search
        - iterate
        - get
        - collect
        - count
        - first

### PersonsClient

For accessing person data.

::: aireloom.resources.persons_client.PersonsClient
    options:
      members:
        - search
        - iterate
        - get
        - collect
        - count
        - first

### ScholixClient

For accessing Scholix link data via the Scholexplorer API.

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
