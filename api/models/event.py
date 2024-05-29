# from enum import Enum
# from typing import Optional, Literal, Annotated
# from datetime import datetime

from typing import List
from sqlmodel import Field, SQLModel
from pydantic import conlist

# from pydantic.functional_validators import AfterValidator

from api.StringDatetime import StringDatetime

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


class EventCreate(EventBase):
    # TODO: Limit this to just take in two items
    participants: List[str]
