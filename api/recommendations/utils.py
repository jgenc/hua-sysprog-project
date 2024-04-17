import json

data = json.loads(open("./api/tools/dummy.json").read())


def get_all_events():
    return data["events"]


def get_user_events(user_id: int):
    user_coupons = [
        coupon for coupon in data["coupons"] if coupon["user_id"] == user_id
    ]
    user_coupon_selections = [coupon["selections"] for coupon in user_coupons]
    user_event_ids = [
        selection["event_id"]
        for selections in user_coupon_selections
        for selection in selections
    ]
    user_events = [
        event for event in data["events"] if event["event_id"] in user_event_ids
    ]
    return user_events
