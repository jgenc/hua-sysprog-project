from datetime import datetime
import random
import logging

from fastapi import APIRouter, Depends, HTTPException
from api.data.dataframe import BettingDataDataframe
from pandas import DataFrame, concat

from api.schemas.user import User, NewUser
from api.dependencies.get_betting_data_df import get_df

router = APIRouter(
    prefix="/user",
    tags=["users"],
)

logger = logging.getLogger("api")


@router.get("/random", response_model=User)
def get_user_random(df: BettingDataDataframe = Depends(get_df)) -> User:
    x = df._users.sample(1).to_dict(orient="records")[0]
    return User(**x)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, df: BettingDataDataframe = Depends(get_df)) -> User:
    try:
        user = User(
            **df._users[df._users["user_id"] == user_id].to_dict(orient="records")[0]
        )
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=User)
def create_user(new_user: NewUser, df: BettingDataDataframe = Depends(get_df)) -> User:
    # TODO: When we have a real database, check if the user already exists and if the id is already in use

    # TODO: Create a standard for timestamps and use this system-wide
    current_date = str(datetime.now())
    # TODO: When we have a real database, we should get the user_id from there
    user_id = random.randint(1000, 9999)

    new_user = User(
        **new_user.model_dump(),
        registration_date=current_date,
        user_id=user_id,
    )

    # FIXME: This is here just for testing purposes
    df._users = concat(
        [df._users, DataFrame([new_user.model_dump()])], ignore_index=True
    )
    logger.debug(f"Newly added DF user:\n{df._users.tail(1)}")
    # logger.debug(f"Series of user:\n{pd.Series(new_user.model_dump())}")

    return new_user
