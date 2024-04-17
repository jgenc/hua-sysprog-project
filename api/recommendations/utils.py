from ..data.betting import BettingData

data = BettingData("./api/data/dummy.json")


def get_all_events():
    return data.events


def get_user_events(user_id: int) -> list[dict]:
    user_coupons = data.coupons[data.coupons["user_id"] == user_id]
    user_coupon_selections = user_coupons["selections"].to_list()
    user_coupon_selections = [
        selection for selections in user_coupon_selections for selection in selections
    ]
    user_event_ids = [selection["event_id"] for selection in user_coupon_selections]
    user_events = data.events[data.events["event_id"].isin(user_event_ids)]
    return user_events
