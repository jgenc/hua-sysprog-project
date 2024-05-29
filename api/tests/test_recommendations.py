from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import app
from api.routers import users

from api.tests.test_dataset import session_fixture, client_fixture
from api.models.recommendations import Recommendation, RecommendationWithEvents

client = TestClient(app)
client_user = TestClient(users.router)


def test_recommendation_static(client):
    response = client.get("/recommendation/0")

    assert response.status_code == 200
    for recommendation in response.json():
        assert RecommendationWithEvents(**recommendation)
