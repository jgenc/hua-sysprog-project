from typing import Optional

from sqlmodel import Field, SQLModel

# The API has schemas for all the previous stuff (api/schemas/)
# so the final type should be used here, as validation is done
# at that level. Validation here is avoided

# For the Python instance of a generated user to have an ID it
# should first be saved in the database. The ID is generated
# by the database, not from us.

# TODO: Add validations from schema


class UserBase(SQLModel):
    birth_year: int
    country: str
    currency: str
    gender: str


class User(UserBase, table=True):
    # TODO: At some point this will change to UUID
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    registration_date: str
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
