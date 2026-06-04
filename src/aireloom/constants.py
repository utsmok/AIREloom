"""Constants used throughout the Aireloom library.

This module defines constants for API base URLs, default client settings,
and various literals or enumerations used for API parameters.
"""

from importlib.metadata import PackageNotFoundError, version as _get_version

OPENAIRE_GRAPH_API_BASE_URL = "https://api.openaire.eu/graph/v2"
OPENAIRE_SCHOLIX_API_BASE_URL = "https://api.scholexplorer.openaire.eu/v3"
REGISTERED_SERVICE_API_TOKEN_URL = "https://aai.openaire.eu/oidc/token"

# Default settings
DEFAULT_TIMEOUT: int = 30  # Default request timeout in seconds
DEFAULT_RETRIES: int = 2  # Default number of retries on transient errors
DEFAULT_PAGE_SIZE: int = 20  # Default number of results per page for standard search
ITERATE_PAGE_SIZE: int = (
    100  # Default number of results per page for iteration (using cursor)
)

try:
    __version__: str = _get_version("aireloom")
except PackageNotFoundError:
    __version__: str = "0.0.0"

DEFAULT_USER_AGENT: str = f"aireloom/{__version__}"
CLIENT_HEADERS: dict[str, str] = {
    "accept": "application/json",
    "User-Agent": DEFAULT_USER_AGENT,
}
