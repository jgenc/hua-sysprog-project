from typing import Annotated

from pydantic import BaseModel


class Event(BaseModel):
    begin_timestamp: str
    end_timestamp: str
    country: str
    event_id: str
    league: str
    participants: list[str]
    sport: str
