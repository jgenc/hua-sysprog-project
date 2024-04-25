from pydantic import BaseModel
from .StringDatetime import StringDatetime


class Selection(BaseModel):
    event_id: str
    odds: float


class Coupon(BaseModel):
    coupon_id: int
    selections: list[Selection]
    stake: float
    timestamp: StringDatetime
    user_id: int
