from typing import Annotated

from pydantic import BaseModel


class Event(BaseModel):
    begin_timestamp: str
    country: str
    event_id: int
    league: str
    participants: list[str]
    sport: str
