# aireloom/resources/persons_client.py
"""Client for interacting with the OpenAIRE Persons API endpoint.

This module provides the `PersonsClient`, which facilitates access to
OpenAIRE's person data. It leverages generic mixins from `bibliofabric.resources`
for common API operations like retrieving individual entities, searching, and
iterating through result sets.
"""

from typing import TYPE_CHECKING

from bibliofabric.log_config import logger
from bibliofabric.resources import (
    BaseResourceClient,
    CursorIterableMixin,
    GettableMixin,
    SearchableMixin,
)

if TYPE_CHECKING:
    from ..client import AireloomClient
from ..endpoints import PERSONS
from ..models import Person, PersonResponse


class PersonsClient(
    GettableMixin, SearchableMixin, CursorIterableMixin, BaseResourceClient
):
    """Client for the OpenAIRE Persons API endpoint.

    This client provides standardized methods (`get`, `search`, `iterate`) for
    accessing person data, by inheriting from `bibliofabric` mixins.
    It is configured with the specific API path and Pydantic models relevant
    to OpenAIRE persons.

    Attributes:
        _entity_path (str): The API path for persons.
        _entity_model (type[Person]): Pydantic model for a single person.
        _search_response_model (type[PersonResponse]): Pydantic model for the
                                                        search response envelope.
    """

    _entity_path: str = PERSONS
    _entity_model: type[Person] = Person
    _search_response_model: type[PersonResponse] = PersonResponse

    def __init__(self, api_client: "AireloomClient"):
        """Initializes the PersonsClient.

        Args:
            api_client: An instance of AireloomClient.
        """
        super().__init__(api_client)
        logger.debug(f"PersonsClient initialized for path: {self._entity_path}")

    # All get, search, and iterate methods are now provided by the mixins
