# https://graph.openaire.eu/docs/data-model/entities/community

from typing import Literal
from pydantic import BaseModel, Field

CommunityType = Literal["Research Community", "Research infrastructure"]

class Community(BaseModel):
    id: str | None = None
    acronym: str | None = None
    description: str | None = None
    name: str | None = None
    subjects: list[str] = Field(default_factory=list)
    type: CommunityType | None = None
    zenodoCommunity: str | None = None

    class Config:
        frozen = True

# Response wrapper classes
class Header(BaseModel):
    nextCursor: str | None = None

    class Config:
        frozen = True

class Message(BaseModel):
    header: Header
    results: list[Community]

    class Config:
        frozen = True