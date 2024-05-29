import pytest

from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ..routers import users
from api.models import user
from .test_dataset import session_fixture, client_fixture

client = TestClient(users.router)


def test_get_user_api(client):
    response = client.get("/user/0")

    assert response.status_code == 200
    assert user.User().model_validate(response.json())


def test_get_user_api_not_found(client):
    res = client.get("/user/9999")

    assert res.status_code == 404


def test_create_user_api():
    response = client.post(
        "/user/",
        json={"birth_year": 2002, "country": "US", "currency": "USD", "gender": "F"},
    )
    assert response.status_code == 200
    assert user.User().model_validate(response.json())


def test_create_user_api_flawed():
    with pytest.raises(RequestValidationError) as excinfo:
        response = client.post(
            "/user/",
            json={
                "birth_year": 1992,
                "country": "US",
                "currency": "KL",
                "gender": "FM",
            },
        )
