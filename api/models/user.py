from enum import Enum
from typing import Optional, Literal, Annotated
from datetime import datetime

from sqlmodel import Field, SQLModel
from pydantic.functional_validators import AfterValidator

from api.StringDatetime import StringDatetime

# The API has schemas for all the previous stuff (api/schemas/)
# so the final type should be used here, as validation is done
# at that level. Validation here is avoided

# For the Python instance of a generated user to have an ID it
# should first be saved in the database. The ID is generated
# by the database, not from us.


def check_birth_year(year: int) -> int:
    if year < 1920 or year > datetime.now().year - 22:
        raise ValueError("Invalid birth year")
    return year


def check_country(country: str) -> str:
    # TODO: Use a standard for country codes
    if country not in ["US", "UK", "DE", "FR", "GR", "AL", "IT", "ES", "JPN"]:
        raise ValueError("Invalid country")
    return country


def check_currency(currency: str) -> str:
    if currency not in ["USD", "EUR", "JPY", "GBP"]:
        raise ValueError("Invalid currency")
    return currency


class GenderEnum(str, Enum):
    M = "M"
    F = "F"


BirthYear = Annotated[int, AfterValidator(check_birth_year)]
Country = Annotated[str, AfterValidator(check_country)]
Currency = Annotated[str, AfterValidator(check_currency)]


class UserBase(SQLModel):
    birth_year: BirthYear
    country: Country
    currency: Currency
    gender: GenderEnum


class User(UserBase, table=True):
    # TODO: At some point this will change to UUID
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    registration_date: StringDatetime
    pass


class UserCreateWeb(UserBase):
    # Essentially what data a user would give.
    # Personally, I think that the JS code should also send in the
    # registration date.
    pass


class UserPublic(UserBase):
    pass


class UserUpdate(SQLModel):
    pass
