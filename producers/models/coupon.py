from pydantic import BaseModel


class SelectionCreate(BaseModel):
    event_id: int
    odds: float


class CouponCreate(BaseModel):
    user_id: int
    stake: float
    selections: list[SelectionCreate]
