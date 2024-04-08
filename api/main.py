from typing import Union

from fastapi import FastAPI

from .schemas import Coupon, Event, User, Selection

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    return User(
        birth_year=1990,
        country="US",
        currency="USD",
        gender="Male",
        registration_date="2021-01-01T12:08:54",
        user_id=user_id,
    )


@app.get("/event/{event_id}", response_model=Event)
def get_event(event_id: int) -> Event:
    return Event(
        begin_timestamp="2021-01-01T12:08:54",
        country="US",
        event_id=event_id,
        league="NFL",
        participants=["New England Patriots", "Tampa Bay Buccaneers"],
        sport="Football",
    )


@app.get("/coupon/{user_id}/{coupon_id}", response_model=Coupon)
def get_coupon(user_id: int, coupon_id: int) -> Coupon:
    return Coupon(
        coupon_id=coupon_id,
        selections=[
            Selection(event_id="1", odds=1.5),
            Selection(event_id="2", odds=2.5),
        ],
        stake=100,
        timestamp="2021-01-01T12:08:54",
        user_id=user_id,
    )
