"""AIREloom: A Python client for the OpenAIRE Graph API."""

__version__ = "0.1.0" # Placeholder

from .session import AireloomSession
from .exceptions import (
    AireloomError,
    AuthenticationError,
    ApiError,
    RateLimitError,
    ValidationError,
)
from .models.research_product import ResearchProduct
from .models.organization import Organization
from .models.data_source import DataSource
from .models.project import Project

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