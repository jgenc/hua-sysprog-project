from sqlmodel import select, col

from ..data.dataframe import BettingDataDataframe
from api.models.coupon import Coupon
from api.models.event import Event
from api.dependencies.database import get_session, Session

data = BettingDataDataframe("./api/data/dummy.json")


def get_all_events_df():
    return data._events


def get_all_events():
    session: Session = next(get_session())

    events = session.exec(select(Event)).all()

    session.close()
    return events


def get_user_events_df(user_id: int) -> list[dict]:
    pass
    user_coupons = data._coupons[data._coupons["user_id"] == user_id]
    user_coupon_selections = user_coupons["selections"].to_list()
    user_coupon_selections = [
        selection for selections in user_coupon_selections for selection in selections
    ]
    user_event_ids = [selection["event_id"] for selection in user_coupon_selections]
    user_events = data._events[data._events["event_id"].isin(user_event_ids)]
    return user_events


def get_user_events(user_id: int):
    session: Session = next(get_session())

    user_coupons = session.exec(select(Coupon).where(Coupon.user_id == user_id)).all()

    user_coupons_selections = []
    for coupon in user_coupons:
        for selection in coupon.selections:
            user_coupons_selections.append(selection)

    user_event_ids = [
        user_coupons_selection.event_id
        for user_coupons_selection in user_coupons_selections
    ]

    user_events = session.exec(
        select(Event).where(col(Event.id).in_(user_event_ids))
    ).all()

    session.close()
    return user_events
