from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..schemas import User

from ..main import app


client = TestClient(app)


def test_user_random():
    response = client.get("/user/random")

    assert response.status_code == 200
    assert User(**response.json())


def test_user():
    response = client.get("/user/12197")

    assert response.status_code == 200
    assert User(**response.json())
