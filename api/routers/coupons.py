import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.dependencies.database import get_session, Session
from api.models.coupon import Coupon, CouponWithSelections
from api.models.user import User
from api.dependencies.get_betting_data_df import get_df

router = APIRouter(
    prefix="/coupon", tags=["coupons"], dependencies=[Depends(get_session)]
)

logger = logging.getLogger("api")


def get_populated_coupons(coupons):
    results_populated = []
    for res in coupons:
        results_populated.append(
            CouponWithSelections(
                id=res.id,
                user_id=res.user_id,
                stake=res.stake,
                timestamp=res.timestamp,
                selections=[selection.model_dump() for selection in res.selections],
            )
        )
    return results_populated


@router.get("/{coupon_id}", response_model=Coupon)
def read_coupon(
    coupon_id: int, session: Session = Depends(get_session)
) -> CouponWithSelections | None:
    results = session.get(Coupon, coupon_id)
    if not results:
        raise HTTPException(status_code=404, detail="Coupons not found")
    return get_populated_coupons([results])[0]


@router.get("/user/{user_id}")
def read_coupon_userid(
    user_id: int, session: Session = Depends(get_session)
) -> CouponWithSelections | list[CouponWithSelections] | None:
    user_results = session.exec(select(User).where(User.id == user_id)).all()
    if not user_results:
        raise HTTPException(status_code=404, detail="User not found")

    results = session.exec(select(Coupon).where(Coupon.user_id == user_id)).all()
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Coupons not found")
    return get_populated_coupons(results)
