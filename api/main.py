import json
from typing import Union
import random

from fastapi import FastAPI

from .schemas import Coupon, Event, User, Selection, Recommendations
from .recommendations import most_bet_sport_recommenedation

app = FastAPI()

data = json.loads(open("./api/tools/dummy.json").read())


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/user/random", response_model=User)
def get_user_random() -> User:
    x = random.choice(data["users"])
    return x


@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    for user in data["users"]:
        if user["user_id"] == user_id:
            return user


@app.get("/event/random", response_model=Event)
def get_event_random() -> Event:
    return random.choice(data["events"])


@app.get("/event/{event_id}", response_model=Event)
def get_event(event_id: str) -> Event:
    for event in data["events"]:
        if event["event_id"] == event_id:
            return event


@app.get("/coupon/random", response_model=Coupon)
def get_coupon_random() -> Coupon:
    return random.choice(data["coupons"])


@app.get("/coupon/{coupon_id}", response_model=Coupon)
def get_coupon(coupon_id: int) -> Coupon:
    for coupon in data["coupons"]:
        if coupon["coupon_id"] == coupon_id:
            return coupon


@app.get("/coupons/{user_id}", response_model=list[Coupon])
def get_coupons(user_id: int) -> list[Coupon]:
    return [coupon for coupon in data["coupons"] if coupon["user_id"] == user_id]


@app.get("/recommendation/{user_id}", response_model=Recommendations)
def get_recommendation(user_id: int) -> Recommendations:
    recommended_events = most_bet_sport_recommenedation(user_id)
    return Recommendations(events=recommended_events)
