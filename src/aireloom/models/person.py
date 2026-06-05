# aireloom/models/person.py
"""Pydantic models for representing OpenAIRE Person entities.

This module defines the Pydantic model for an OpenAIRE Person,
based on the OpenAIRE Graph API v1 persons endpoint.
Reference: https://api.openaire.eu/graph/v1/persons
"""

from pydantic import ConfigDict, Field, computed_field

from .._helpers import extract_orcid

# Import base classes
from .base import ApiResponse, BaseEntity
from .safe_types import SafeList, SafeStr


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
    originalId: SafeList[str] = Field(default_factory=list)
    givenName: SafeStr = ""
    familyName: SafeStr = ""
    alternativeNames: SafeList[str] = Field(default_factory=list)
    biography: SafeStr = ""
    subject: SafeList[str] = Field(default_factory=list)
    indicator: dict | None = None
    context: dict | None = None
    consent: bool | None = None
    coAuthors: SafeList[str] = Field(default_factory=list)

    @computed_field
    @property
    def orcid(self) -> str | None:
        return extract_orcid(self.originalId, self.id)

    @computed_field
    @property
    def full_name(self) -> str:
        parts = [n for n in (self.givenName, self.familyName) if n]
        return " ".join(parts)


    def __str__(self) -> str:
        name = self.full_name
        if name and self.orcid:
            return f"{name} (ORCID:{self.orcid})"
        if name:
            return name
        return f"Person(id={self.id!r})"
    model_config = ConfigDict(extra="allow")


# Define the specific response type for persons
PersonResponse = ApiResponse[Person]
"""Type alias for an API response containing a list of `Person` entities."""
