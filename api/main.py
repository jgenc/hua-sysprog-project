from typing import Union
from datetime import datetime
import random
import logging

from fastapi import FastAPI, HTTPException
import pandas as pd

from .routers import users
from .data.betting import BettingData
from .schemas import Coupon, Event, User, Selection, Recommendations, NewUser
from .recommendations import most_bet_sport_recommenedation

logger = logging.getLogger("api")
# logger.disabled = True

app = FastAPI()
app.include_router(users.router, prefix="/user")

df = BettingData("./api/data/dummy.json")


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


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
    try:
        coupon = df.coupons[df.coupons["coupon_id"] == coupon_id].to_dict(
            orient="records"
        )[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Coupon not found")

    return Coupon(**coupon)


@app.get("/coupons/{user_id}", response_model=list[Coupon])
def get_coupon_userid(user_id: int) -> list[Coupon]:
    user_id_exists = df.users["user_id"].isin([user_id]).any()
    if not user_id_exists:
        raise HTTPException(status_code=404, detail="User not found")

    return [
        Coupon(**x)
        for x in df.coupons[df.coupons["user_id"] == user_id].to_dict(orient="records")
    ]


@app.get("/recommendation/{user_id}", response_model=Recommendations)
def get_recommendation(user_id: int) -> Recommendations:
    recommended_events = most_bet_sport_recommenedation(user_id)
    return Recommendations(events=recommended_events)


if __name__ == "__main__":
    import uvicorn
    from .log_conf import LOGGING_CONFIG

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8098,
        log_config=LOGGING_CONFIG,
        reload=True,
    )
