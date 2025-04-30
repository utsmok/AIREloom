"""Defines API endpoint paths and validation details."""

# Base URLs
GRAPH_API_BASE_URL = "https://api.graph.openaire.eu/v1/"
SCHOLIX_API_BASE_URL = (
    "https://api-beta.scholexplorer.openaire.eu/v3/"  # Scholexplorer v3 (beta)
)

# --- Graph API Endpoint Paths ---
RESEARCH_PRODUCTS = "researchProducts"
ORGANIZATIONS = "organizations"
DATA_SOURCES = "dataSources" # Corrected casing
PROJECTS = "projects"
SCHOLIX = "Links"  # Renamed for Scholexplorer

# Basic definition structure: {path: {'filters': dict(), 'sort': dict()}}
ENDPOINT_DEFINITIONS = {
    RESEARCH_PRODUCTS: {
        "filters": { # Map filter name to its definition (type, etc.)
            "search": {"type": "str"},
            "mainTitle": {"type": "str"},
            "description": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "originalId": {"type": "str"},
            "type": {"type": "str"}, # Could be Literal/Enum later
            "fromPublicationDate": {"type": "date"},
            "toPublicationDate": {"type": "date"},
            "subjects": {"type": "str"}, # Potentially list?
            "countryCode": {"type": "str"},
            "authorFullName": {"type": "str"},
            "authorOrcid": {"type": "str"},
            "publisher": {"type": "str"},
            "bestOpenAccessRightLabel": {"type": "str"},
            "influenceClass": {"type": "str"},
            "impulseClass": {"type": "str"},
            "popularityClass": {"type": "str"},
            "citationCountClass": {"type": "str"},
            "instanceType": {"type": "str"},
            "sdg": {"type": "str"}, # Potentially list?
            "fos": {"type": "str"}, # Potentially list?
            "isPeerReviewed": {"type": "bool"},
            "isInDiamondJournal": {"type": "bool"},
            "isPubliclyFunded": {"type": "bool"},
            "isGreen": {"type": "bool"},
            "openAccessColor": {"type": "str"},
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relProjectId": {"type": "str"},
            "relProjectCode": {"type": "str"},
            "hasProjectRel": {"type": "bool"},
            "relProjectFundingShortName": {"type": "str"},
            "relProjectFundingStreamId": {"type": "str"},
            "relHostingDataSourceId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": { # Map sort field to its definition (currently empty)
            "relevance": {},
            "publicationDate": {},
            "dateOfCollection": {},
            "influence": {},
            "popularity": {},
            "citationCount": {},
            "impulse": {},
        },
    },
    ORGANIZATIONS: {
        "filters": {
            "search": {"type": "str"},
            "legalName": {"type": "str"},
            "legalShortName": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "countryCode": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}},
    },
    DATA_SOURCES: {
        "filters": {
            "search": {"type": "str"},
            "officialName": {"type": "str"},
            "englishName": {"type": "str"},
            "legalShortName": {"type": "str"},
            "id": {"type": "str"},
            "pid": {"type": "str"},
            "subjects": {"type": "str"}, # Potentially list?
            "dataSourceTypeName": {"type": "str"},
            "contentTypes": {"type": "str"}, # Potentially list?
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}},
    },
    PROJECTS: {
        "filters": {
            "search": {"type": "str"},
            "title": {"type": "str"},
            "keywords": {"type": "str"}, # Potentially list?
            "id": {"type": "str"},
            "code": {"type": "str"},
            "acronym": {"type": "str"},
            "callIdentifier": {"type": "str"},
            "fundingShortName": {"type": "str"},
            "fundingStreamId": {"type": "str"},
            "fromStartDate": {"type": "date"},
            "toStartDate": {"type": "date"},
            "fromEndDate": {"type": "date"},
            "toEndDate": {"type": "date"},
            "relOrganizationName": {"type": "str"},
            "relOrganizationId": {"type": "str"},
            "relCommunityId": {"type": "str"},
            "relOrganizationCountryCode": {"type": "str"},
            "relCollectedFromDatasourceId": {"type": "str"},
        },
        "sort": {"relevance": {}, "startDate": {}, "endDate": {}},
    },
    SCHOLIX: {  # Updated for Scholexplorer v3 /Links endpoint
        "filters": { # Types based on Scholix v3 documentation
            "sourcePid": {"type": "str"}, # Required (one of source/target Pid/Publisher/Type)
            "targetPid": {"type": "str"},
            "sourcePublisher": {"type": "str"},
            "targetPublisher": {"type": "str"},
            "sourceType": {"type": "str"}, # Enum: Publication, Dataset, Software, Other
            "targetType": {"type": "str"}, # Enum: Publication, Dataset, Software, Other
            "relation": {"type": "str"},
            "from": {"type": "date"},
            "to": {"type": "date"},
        },
        "sort": {},  # Sorting not specified for /Links endpoint
    },
}


def get_valid_filters(endpoint_path: str) -> set[str]:
    """Returns the set of valid filter keys for a given endpoint path."""
    definitions = ENDPOINT_DEFINITIONS.get(endpoint_path, {})
    filter_definitions = definitions.get("filters", {})
    return set(filter_definitions.keys())


def get_valid_sort_fields(endpoint_path: str) -> set[str]:
    """Returns the set of valid sort fields for a given endpoint path."""
    definitions = ENDPOINT_DEFINITIONS.get(endpoint_path, {})
    sort_definitions = definitions.get("sort", {})
    return set(sort_definitions.keys())
