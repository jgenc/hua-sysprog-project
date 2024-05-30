import httpx
import json

with open("./api/data/dummy.json", "r") as f:
    js = json.load(f)

users = js["users"]
events = js["events"]
coupons = js["coupons"]

for user in users:
    r = httpx.post(
        "http://0.0.0.0:8098/user",
        json={
            "birth_year": user["birth_year"],
            "country": user["country"],
            "currency": user["currency"],
            "gender": user["gender"],
        },
    )
    if r.status_code != 200:
        print(f"Error with {user["id"]}")

for event in events:
    r = httpx.post(
        "http://0.0.0.0:8098/event",
        json={
            "begin_timestamp": event["begin_timestamp"],
            "end_timestamp": event["end_timestamp"],
            "country": event["country"],
            "league": event["league"],
            "sport": event["sport"],
            "participants": [
                event["participants"][0],
                event["participants"][1]
            ]
        },
    )
    if r.status_code != 200:
        print(f"Error with {event["id"]}")


for coupon in coupons:
    r = httpx.post(
        "http://0.0.0.0:8098/coupon",
        json={
            "user_id": coupon["user_id"],
            "stake": coupon["stake"],
            "selections": [selection for selection in coupon["selections"]]
        },
    )
    if r.status_code != 200:
        print(f"Error with {user["id"]}")
