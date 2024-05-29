from typing import Union, List
from datetime import datetime
import random
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.data.dataframe import BettingDataDataframe

from api.dependencies.get_betting_data_df import get_df

from api.models.user import User, UserCreate, UserCreateWeb, UserPublic
from api.database import get_session

router = APIRouter(
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(get_session)],
)

logger = logging.getLogger("api")


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    results = session.get(User, user_id)
    if not results:
        raise HTTPException(status_code=404, detail="User not found")
    return results


@router.post("", response_model=User)
def create_user(
    new_user: UserCreateWeb, session: Session = Depends(get_session)
) -> User:
    current_date = str(datetime.now())

    new_user = UserCreate(**new_user.model_dump(), registration_date=current_date)
    new_user = User(**new_user.model_dump())

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
