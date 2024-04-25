import logging

from fastapi import APIRouter, Depends, HTTPException
from api.data.dataframe import BettingDataDataframe

from api.schemas.coupon import Coupon
from api.dependencies.get_betting_data_df import get_df

router = APIRouter(
    prefix="/coupon",
    tags=["coupons"],
)

logger = logging.getLogger("api")


@router.get("/random", response_model=Coupon)
def get_coupon_random(df: BettingDataDataframe = Depends(get_df)) -> Coupon:
    return Coupon(**df._coupons.sample(1).to_dict(orient="records")[0])


@router.get("/{coupon_id}", response_model=Coupon)
def read_coupon(coupon_id: int, df: BettingDataDataframe = Depends(get_df)) -> Coupon:
    try:
        coupon = df._coupons[df._coupons["coupon_id"] == coupon_id].to_dict(
            orient="records"
        )[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Coupon not found")

    return Coupon(**coupon)


# TODO: Is this a good idea?
@router.get("/user/{user_id}", response_model=list[Coupon])
def read_coupon_userid(
    user_id: int, df: BettingDataDataframe = Depends(get_df)
) -> list[Coupon]:
    user_id_exists = df._users["user_id"].isin([user_id]).any()
    if not user_id_exists:
        raise HTTPException(status_code=404, detail="User not found")

    return [
        Coupon(**x)
        for x in df._coupons[df._coupons["user_id"] == user_id].to_dict(
            orient="records"
        )
    ]
