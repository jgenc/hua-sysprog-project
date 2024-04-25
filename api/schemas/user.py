from typing import Annotated, Literal
from datetime import datetime
from .StringDatetime import StringDatetime

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

# TODO: Add all standard validation values into Documentation


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


BirthYear = Annotated[int, AfterValidator(check_birth_year)]
Country = Annotated[str, AfterValidator(check_country)]
Currency = Annotated[str, AfterValidator(check_currency)]
Gender = Literal["M", "F"]


# TODO: Use a standard for currency codes
class NewUser(BaseModel):
    birth_year: BirthYear
    country: Country
    currency: Currency
    gender: Gender


class User(BaseModel):
    birth_year: BirthYear
    country: Country
    currency: Currency
    gender: Gender
    registration_date: StringDatetime
    # TODO: Make this UUID
    user_id: int
