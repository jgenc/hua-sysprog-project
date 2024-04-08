from typing import Annotated

from pydantic import BaseModel


class Selection(BaseModel):
    event_id: str
    odds: float


class Coupon(BaseModel):
    coupon_id: int
    selections: list[Selection]
    stake: float
    timestamp: str
    user_id: int
