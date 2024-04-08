from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..schemas import User

from ..main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/user/1")

    assert response.status_code == 200
    assert response.json() == {
        "birth_year": 1990,
        "country": "US",
        "currency": "USD",
        "gender": "Male",
        "registration_date": "2021-01-01T12:08:54",
        "user_id": 1,
    }
