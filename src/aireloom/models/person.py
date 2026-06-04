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

    Reference: https://graph.openaire.eu/docs/api/entities/person

    Attributes:
        originalId: Original identifiers from various sources (e.g. ORCID).
        givenName: The person's given (first) name.
        familyName: The person's family (last) name.
        alternativeNames: Alternative names and aliases.
        biography: Biography or description text.
        subject: Research subjects or areas of expertise.
        indicator: Metrics (hIndex, citationCount, publicationCount).
        context: Affiliation context (affiliation, department, country).
        consent: Whether the person has consented to data processing.
        coAuthors: List of co-author names.
    """

    # id is inherited from BaseEntity
    originalId: list[str] | None = None
    givenName: str | None = None
    familyName: str | None = None
    alternativeNames: list[str] | None = None
    biography: str | None = None
    subject: list[str] | None = None
    indicator: dict | None = None
    context: dict | None = None
    consent: bool | None = None
    coAuthors: list[str] | None = None

    model_config = ConfigDict(extra="allow")


# Define the specific response type for persons
PersonResponse = ApiResponse[Person]
"""Type alias for an API response containing a list of `Person` entities."""
