from .StringDatetime import StringDatetime

from pydantic import BaseModel


class Event(BaseModel):
    begin_timestamp: StringDatetime
    end_timestamp: StringDatetime
    country: str
    event_id: str
    league: str
    participants: list[str]
    sport: str
