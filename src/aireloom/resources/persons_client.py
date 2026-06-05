# aireloom/resources/persons_client.py
"""Client for interacting with the OpenAIRE Persons API endpoint."""

from ..endpoints import PERSONS
from ..models import Person, PersonResponse
from ._standard import StandardResourceClient


class PersonsClient(StandardResourceClient):
    """Client for the OpenAIRE Persons API endpoint.

    Attributes:
        _entity_path (str): The API path for persons.
        _entity_model (type[Person]): Pydantic model for a single person.
        _search_response_model (type[PersonResponse]): Pydantic model for the
                                                        search response envelope.
    """

    _entity_path: str = PERSONS
    _entity_model: type[Person] = Person
    _search_response_model: type[PersonResponse] = PersonResponse
