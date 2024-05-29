from enum import Enum
from typing import Optional, Literal, Annotated, TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship
from pydantic.functional_validators import AfterValidator


if TYPE_CHECKING:
    from api.models.event import Event


class RecommendationEventLink(SQLModel, table=True):
    recommendation_id: int | None = Field(
        default=None, foreign_key="recommendation.id", primary_key=True
    )
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)


class Recommendation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")

    events: list["Event"] = Relationship(
        back_populates="recommendations", link_model=RecommendationEventLink
    )


class RecommendationWithEvents(BaseModel):
    id: int
    user_id: int
    events: list[dict]
