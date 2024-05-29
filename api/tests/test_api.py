from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import app
from api.tests.test_dataset import client_fixture, session_fixture


client = TestClient(app)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
