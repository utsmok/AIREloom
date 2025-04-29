"""AIREloom: A Python client for the OpenAIRE Graph API."""

__version__ = "0.1.0"  # Placeholder

from .exceptions import (
    AireloomError,
    ApiError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from .models.data_source import DataSource
from .models.organization import Organization
from .models.project import Project
from .models.research_product import ResearchProduct
from .session import AireloomSession

__all__ = [
    "AireloomSession",
    "ResearchProduct",
    "Organization",
    "DataSource",
    "Project",
    "AireloomError",
    "AuthenticationError",
    "ApiError",
    "RateLimitError",
    "ValidationError",
]
