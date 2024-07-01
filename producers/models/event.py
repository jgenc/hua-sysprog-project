from pydantic import BaseModel


class EventCreate(BaseModel):
    begin_timestamp: str
    end_timestamp: str
    country: str
    league: str
    sport: str
    participants: list[str]
