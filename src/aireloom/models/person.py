# aireloom/models/person.py
"""Pydantic models for representing OpenAIRE Person entities.

This module defines the Pydantic model for an OpenAIRE Person,
based on the OpenAIRE Graph API v1 persons endpoint.
Reference: https://api.openaire.eu/graph/v1/persons
"""

from pydantic import ConfigDict

# Import base classes
from .base import ApiResponse, BaseEntity


class Person(BaseEntity):
    """Model representing an OpenAIRE Person entity.

    Captures details about a person in the OpenAIRE Graph, including
    names, biography, subjects, indicators, and co-authors.
    Inherits the `id` field from `BaseEntity`.

    Attributes:
        givenName: The person's given (first) name.
        familyName: The person's family (last) name.
        biography: Biography or description text.
        subject: List of subjects associated with the person.
        indicator: Citation/impact indicators (structure varies).
        context: Context information (structure varies).
        consent: Consent status of the person's data.
        coAuthors: List of co-author information.
    """

    # id is inherited from BaseEntity
    givenName: str | None = None
    familyName: str | None = None
    biography: str | None = None
    subject: list | None = None
    indicator: dict | None = None
    context: dict | None = None
    consent: str | None = None
    coAuthors: list | None = None

    model_config = ConfigDict(extra="allow")


# Define the specific response type for persons
PersonResponse = ApiResponse[Person]
"""Type alias for an API response containing a list of `Person` entities."""
