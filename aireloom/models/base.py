"""Base Pydantic models for API entities and responses."""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, HttpUrl, field_validator

# Generic type for the entity contained within the response results
EntityType = TypeVar("EntityType", bound="BaseEntity")


class Header(BaseModel):
    """Model for the standard API response header."""

    status: str | None = None
    # Note: "code" seems unused/always null in examples, but kept for potential future use
    code: str | None = None
    message: str | None = None
    # total and count are often strings in the API response, needs validation/coercion
    total: int | None = None
    count: int | None = None
    # next/prev can be full URLs or just the cursor string
    next: str | HttpUrl | None = None
    prev: str | HttpUrl | None = None
    processing_time_millis: int | None = Field(None, alias="processingTimeMillis")
    timestamp: datetime | None = None

    @field_validator("total", "count", mode="before")
    @classmethod
    def coerce_str_to_int(cls, v: Any) -> int | None:
        """Coerce string representations of numbers to integers."""
        if isinstance(v, str):
            try:
                return int(v)
            except (ValueError, TypeError):
                return None  # Or raise a validation error if preferred
        return v


class BaseEntity(BaseModel):
    """Base model for all OpenAIRE entities (like publication, project, etc.)."""

    # Common identifier across most entities
    id: str

    class Config:
        # Allow extra fields, as API responses can vary
        extra = "allow"


class ApiResponse(BaseModel, Generic[EntityType]):
    """Generic base model for standard API list responses."""

    header: Header
    # Results can sometimes be null/absent, sometimes an empty list
    results: list[EntityType] | None = None

    @field_validator("results", mode="before")
    @classmethod
    def handle_null_results(cls, v: Any) -> list[EntityType] | None:
        """Ensure 'results' is a list or None, handling potential null values from API."""
        if v is None:
            return None  # Explicitly return None if API sends null
        if isinstance(v, dict) and "result" in v:
            # API often wraps single result in {"result": {...}} or {"result": [{...}]}
            single_result = v["result"]
            if isinstance(single_result, list):
                return single_result
            if isinstance(single_result, dict):
                return [single_result]  # Wrap single dict in a list
        if isinstance(v, list):
            return v  # Already a list
        # If it's neither None, nor the expected dict wrapper, nor a list, handle appropriately
        # Option: Return empty list, None, or raise ValueError depending on strictness desired
        return []  # Default to empty list for unexpected formats


# Example of a specific response type (for illustration)
# class ResearchProductResponse(ApiResponse[ResearchProduct]):
#     pass
