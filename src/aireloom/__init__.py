"""AIREloom: A Python client for the OpenAIRE Graph API."""

from bibliofabric.exceptions import (
    APIError,
    AuthError,
    BibliofabricError,
    ConfigurationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)

from .client import AireloomClient
from .constants import __version__
from .models import (
    ApiResponse,
    BaseEntity,
    DataSource,
    Header,
    Organization,
    Project,
    ResearchProduct,
    ScholixRelationship,
)
from .session import AireloomSession

__all__ = [
    # Core Client/Session
    "AireloomClient",
    "AireloomSession",
    # Core Exceptions
    "BibliofabricError",
    "APIError",
    "AuthError",
    "ConfigurationError",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    "TimeoutError",
    "ValidationError",
    # Key Models (consider reducing if needed)
    "ApiResponse",
    "BaseEntity",
    "DataSource",
    "Header",
    "Organization",
    "Project",
    "ResearchProduct",
    "ScholixRelationship",
]
