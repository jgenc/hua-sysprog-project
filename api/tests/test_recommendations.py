from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..main import app
from ..routers import users
from ..schemas import Recommendations


client = TestClient(app)
client_user = TestClient(users.router)


def test_recommendation_static():
    response = client.get("/recommendation/44798")

    assert response.status_code == 200
    assert Recommendations(**response.json())


def test_random_user_recommendation():
    user_id = client_user.get("/user/random").json()["user_id"]
    response = client.get(f"/recommendation/{user_id}")

    assert response.status_code == 200
    assert Recommendations(**response.json()) and len(response.json()["events"]) == 3
