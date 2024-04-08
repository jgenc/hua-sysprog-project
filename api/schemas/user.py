from typing import Annotated

from pydantic import BaseModel


class User(BaseModel):
    birth_year: int
    country: str
    currency: str
    gender: str
    registration_date: str
    user_id: int
