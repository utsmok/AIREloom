# aireloom/models/organization.py
"""Pydantic models for representing OpenAIRE Organization entities.

This module defines the Pydantic model for an OpenAIRE Organization,
including nested models for country and persistent identifiers (PIDs),
based on the OpenAIRE data model documentation.
Reference: https://graph.openaire.eu/docs/data-model/entities/organization
"""

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, computed_field

# Import base classes
from .base import ApiResponse, BaseEntity
from .safe_types import SafeList, SafeStr


class Country(BaseModel):
    """Represents the country associated with an organization.

    Attributes:
        code: The ISO 3166-1 alpha-2 country code (e.g., "GR", "US").
        label: The human-readable name of the country (e.g., "Greece").
    """

    code: SafeStr = ""
    label: SafeStr = ""

    model_config = ConfigDict(extra="allow")


# Type alias for Country that defaults None to Country()
SafeCountry = Annotated[Country, BeforeValidator(lambda v: Country() if v is None else v)]


class OrganizationPid(BaseModel):
    """Represents a persistent identifier (PID) for an organization.

    Attributes:
        scheme: The scheme of the PID (e.g., "ror", "grid", "isni").
        value: The value of the PID.
    """

    scheme: SafeStr = ""
    value: SafeStr = ""

    model_config = ConfigDict(extra="allow")


class Organization(BaseEntity):
    """Model representing an OpenAIRE Organization entity.

    Captures details about an organization, including its names, website,
    country, and various persistent identifiers. Inherits the `id` field
    from `BaseEntity`.

    Attributes:
        legalShortName: The official short name or acronym of the organization.
        legalName: The full official legal name of the organization.
        alternativeNames: A list of other known names for the organization.
        websiteUrl: The URL of the organization's official website.
        country: A `Country` object representing the organization's country.
        pids: A list of `OrganizationPid` objects representing various PIDs
              associated with the organization.
    """

    # id is inherited from BaseEntity
    legalShortName: SafeStr = ""
    legalName: SafeStr = ""
    alternativeNames: SafeList[str] = Field(default_factory=list)
    websiteUrl: str | None = None
    country: SafeCountry = Field(default_factory=Country)
    pids: SafeList[OrganizationPid] = Field(default_factory=list)

    @computed_field
    @property
    def ror_id(self) -> str | None:
        for pid in self.pids:
            if pid.scheme and pid.scheme.lower() == "ror" and pid.value:
                return pid.value
        return None

    @computed_field
    @property
    def country_code(self) -> str | None:
        return self.country.code if self.country.code and self.country.code != "UNKNOWN" else None

    model_config = ConfigDict(extra="allow")


# Define the specific response type for organizations
OrganizationResponse = ApiResponse[Organization]
"""Type alias for an API response containing a list of `Organization` entities."""
