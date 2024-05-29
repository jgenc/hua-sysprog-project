# from enum import Enum
# from typing import Optional, Literal, Annotated
# from datetime import datetime

from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from pydantic import conlist

# from pydantic.functional_validators import AfterValidator

from api.StringDatetime import StringDatetime
from api.models.recommendations import RecommendationEventLink

if TYPE_CHECKING:
    from api.models.recommendations import Recommendation

# TODO: Add validations for country, league, sport and participants?


class ParticipantsBase(SQLModel):
    a: str
    b: str


class Participants(ParticipantsBase, table=True):
    id: int = Field(default=None, primary_key=True)


class EventBase(SQLModel):
    begin_timestamp: StringDatetime
    end_timestamp: StringDatetime
    country: str
    league: str
    sport: str


class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)
    participants_id: int = Field(default=None, foreign_key="participants.id")

    recommendations: list["Recommendation"] = Relationship(
        back_populates="events", link_model=RecommendationEventLink
    )


class EventCreate(EventBase):
    # TODO: Limit this to just take in two items
    participants: List[str]
