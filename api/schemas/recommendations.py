from typing import Annotated

from pydantic import BaseModel

from .coupon import Coupon, Selection
from .event import Event
from .user import User


class Recommendations(BaseModel):
    events: list[Event]
