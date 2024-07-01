from pydantic import BaseModel

class UserCreate(BaseModel):
    birth_year: int
    country: str
    currency: str
    gender: str
