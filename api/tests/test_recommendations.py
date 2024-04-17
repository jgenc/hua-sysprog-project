from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..main import app
from ..schemas import Recommendations


client = TestClient(app)


def test_recommendation_static():
    response = client.get("/recommendation/44798")

    assert response.status_code == 200
    assert Recommendations(**response.json())
