import os
import json
import httpx

from api.tools.timing_functions import timeit

# Default port is 8098 for the docker-compose environment
PORT = os.environ.get("PORT", 8098)

with open("./api/data/dummy.json", "r") as f:
    js = json.load(f)

users = js["users"]
events = js["events"]
coupons = js["coupons"]

@timeit
def create_users():
    for user in users:
        r = httpx.post(
            f"http://localhost:{PORT}/users",
            json={
                "birth_year": user["birth_year"],
                "country": user["country"],
                "currency": user["currency"],
                "gender": user["gender"]
            },
        )
        if r.status_code != 200:
            print(f"Error with {user["id"]=}")

@timeit
def create_events():
    for event in events:
        r = httpx.post(
            f"http://localhost:{PORT}/events",
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
            print(f"Error with {event["id"]=}")

@timeit
def create_coupons():
    for coupon in coupons:
        r = httpx.post(
            f"http://localhost:{PORT}/coupons",
            json={
                "user_id": coupon["user_id"],
                "stake": coupon["stake"],
                "selections": [selection for selection in coupon["selections"]]
            },
        )
        if r.status_code != 200:
            print(f"Error with {coupon["id"]=}")

create_users()
create_events()
create_coupons()