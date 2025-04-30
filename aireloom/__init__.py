"""AIREloom: A Python client for the OpenAIRE Graph API."""

__version__ = "0.1.0"  # Placeholder

# Import Exceptions
from .exceptions import (
    AireloomError,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

# Re-export key models from the models subpackage
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

# Import main session class
from .session import AireloomSession

__all__ = [
    "AireloomSession",
    "AireloomError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ApiResponse",
    "BaseEntity",
    "Community",
    "DataSource",
    "Header",
    "Organization",
    "Project",
    "Relationship",
    "ResearchProduct",
    "ScholixRelationship",
]
