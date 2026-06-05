# aireloom/resources/projects_client.py
"""Client for interacting with the OpenAIRE Projects API endpoint."""

from ..endpoints import PROJECTS
from ..models import Project, ProjectResponse
from ._standard import StandardResourceClient


class ProjectsClient(StandardResourceClient):
    """Client for the OpenAIRE Projects API endpoint.

    Attributes:
        _entity_path (str): The API path for projects.
        _entity_model (type[Project]): Pydantic model for a single project.
        _search_response_model (type[ProjectResponse]): Pydantic model for the
                                                        search response envelope.
    """

    _entity_path: str = PROJECTS
    _entity_model: type[Project] = Project
    _search_response_model: type[ProjectResponse] = ProjectResponse
