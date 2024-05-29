from enum import Enum
from typing import Optional, Literal, Annotated
from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship
from pydantic.functional_validators import AfterValidator
from pydantic import BaseModel

from api.StringDatetime import StringDatetime


class SelectionCouponLink(SQLModel, table=True):
    selection_id: int | None = Field(
        default=None, foreign_key="selection.id", primary_key=True
    )
    coupon_id: int | None = Field(
        default=None, foreign_key="coupon.id", primary_key=True
    )


class Selection(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_id: int = Field(default=None, foreign_key="event.id")
    odds: float

    coupons: list["Coupon"] = Relationship(
        back_populates="selections", link_model=SelectionCouponLink
    )


class CouponBase(SQLModel):
    user_id: int = Field(default=None, foreign_key="user.id")
    stake: float
    timestamp: StringDatetime


class Coupon(CouponBase, table=True):
    id: int = Field(default=None, primary_key=True)

    selections: list["Selection"] = Relationship(
        back_populates="coupons", link_model=SelectionCouponLink
    )


class CouponWithSelections(BaseModel):
    id: int
    user_id: int
    stake: float
    timestamp: StringDatetime
    selections: list
