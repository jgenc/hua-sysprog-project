import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import ValidationError

from ..schemas import User, NewUser
from ..routers import users

client = TestClient(users.router)


def test_get_user_random_api():
    response = client.get("/user/random")

    assert response.status_code == 200
    assert User(**response.json())


def test_get_user_api():
    response = client.get("/user/0")

    assert response.status_code == 200
    assert User(**response.json())


def test_create_user_api_flawed():
    # TODO: Is this good practice?
    with pytest.raises(ValidationError) as excinfo:
        assert NewUser(birth_year=2002, country="US", currency="KL", gender="M")


def test_create_user_api():
    response = client.post(
        "/user/",
        json={"birth_year": 2002, "country": "US", "currency": "USD", "gender": "F"},
    )
    assert response.status_code == 200
    assert User(**response.json())
