import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.dependencies.database import get_session, Session
from api.models.coupon import Coupon, CouponWithSelections, CouponWeb, Selection
from api.models.user import User
from api.models.event import Event
from api.dependencies.get_betting_data_df import get_df
from api.StringDatetime import get_time

router = APIRouter(
    prefix="/coupons", tags=["coupons"], dependencies=[Depends(get_session)]
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


@router.post("")
def create_coupon(new_coupon: CouponWeb, session: Session = Depends(get_session)):
    user_results = session.exec(select(User).where(User.id == new_coupon.user_id)).all()
    if not user_results:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO: Add a check to see if a coupon for the user exists with exact same stake and selections
    event_ids = []
    for selection in new_coupon.selections:
        event_ids.append(selection.event_id)
    event_results = session.exec(select(Event).where(Event.id.in_(event_ids))).all()
    if len(event_results) != len(event_ids):
        raise HTTPException(status_code=422, detail="Check if Events exist")

    new_coupon_db = Coupon(
        user_id=new_coupon.user_id,
        stake=new_coupon.stake,
        timestamp=get_time(),
        selections=[
            Selection(**selection.model_dump()) for selection in new_coupon.selections
        ],
    )

    session.add(new_coupon_db)
    session.commit()
    session.refresh(new_coupon_db)

    return get_populated_coupons([new_coupon_db])
