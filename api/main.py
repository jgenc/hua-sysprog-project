from typing import Union
import random

from fastapi import FastAPI

from .data.betting import BettingData
from .schemas import Coupon, Event, User, Selection, Recommendations
from .recommendations import most_bet_sport_recommenedation

app = FastAPI()

df = BettingData("./api/data/dummy.json")


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/user/random", response_model=User)
def get_user_random() -> User:
    x = df.users.sample(1).to_dict(orient="records")[0]
    return User(**x)


@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    return User(**df.users[df.users["user_id"] == user_id].to_dict(orient="records")[0])


@app.get("/event/random", response_model=Event)
def get_event_random() -> Event:
    return Event(**df.events.sample(1).to_dict(orient="records")[0])


@app.get("/event/{event_id}", response_model=Event)
def get_event(event_id: str) -> Event:
    return Event(
        **df.events[df.events["event_id"] == event_id].to_dict(orient="records")[0]
    )


@app.get("/coupon/random", response_model=Coupon)
def get_coupon_random() -> Coupon:
    return Coupon(**df.coupons.sample(1).to_dict(orient="records")[0])


@app.get("/coupon/{coupon_id}", response_model=Coupon)
def get_coupon(coupon_id: int) -> Coupon:
    return Coupon(
        **df.coupons[df.coupons["coupon_id"] == coupon_id].to_dict(orient="records")[0]
    )


@app.get("/coupons/{user_id}", response_model=list[Coupon])
def get_coupons(user_id: int) -> list[Coupon]:
    return [
        Coupon(**x)
        for x in df.coupons[df.coupons["user_id"] == user_id].to_dict(orient="records")
    ]


@app.get("/recommendation/{user_id}", response_model=Recommendations)
def get_recommendation(user_id: int) -> Recommendations:
    recommended_events = most_bet_sport_recommenedation(user_id)
    return Recommendations(events=recommended_events)
