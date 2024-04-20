from typing import Union
from datetime import datetime
import random
import logging

from fastapi import FastAPI
import pandas as pd

from .data.betting import BettingData
from .schemas import Coupon, Event, User, Selection, Recommendations, NewUser
from .recommendations import most_bet_sport_recommenedation

app = FastAPI()
logger = logging.getLogger("api")
# logger.disabled = True

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


@app.post("/user/", response_model=User)
def create_user(new_user: NewUser) -> User:
    # TODO: When we have a real database, check if the user already exists and if the id is already in use

    # TODO: Create a standard for timestamps and use this system-wide
    current_date = datetime.now()
    # TODO: When we have a real database, we should get the user_id from there
    user_id = random.randint(1000, 9999)

    new_user = User(
        **new_user.model_dump(),
        registration_date=current_date,
        user_id=user_id,
    )

    # FIXME: This is here just for testing purposes
    df.users = pd.concat(
        [df.users, pd.DataFrame([new_user.model_dump()])], ignore_index=True
    )
    logger.debug(f"Newly added DF user:\n{df.users.tail(1)}")
    # logger.debug(f"Series of user:\n{pd.Series(new_user.model_dump())}")

    return new_user


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
