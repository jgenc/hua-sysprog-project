import pytest

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from pydantic import ValidationError

from api.routers import events
from api.models import event

from .test_dataset import session_fixture, client_fixture


client = TestClient(events.router)


def test_get_event(client):
    response = client.get("/events/0")

    assert response.status_code == 200
    assert event.Event().model_validate(response.json())


def test_read_event_not_found(client):
    response = client.get("/events/-1")

    assert response.status_code == 404


def test_create_event(client):
    event = {
        "begin_timestamp": "2021-01-01T00:00:00",
        "end_timestamp": "2021-01-01T01:00:00",
        "country": "US",
        "league": "NBA",
        "participants": ["Lakers", "Warriors"],
        "sport": "Basketball",
    }

    result = client.post("/events/?gen_recommendations=False", json=event)
    assert result.status_code == 200


def test_create_event_same_participants(client):
    event = {
        "begin_timestamp": "2021-01-01T00:00:00",
        "end_timestamp": "2021-01-01T01:00:00",
        "country": "GR",
        "league": "LG",
        "participants": ["Panathinaikos", "AEK"],
        "sport": "Basketball",
    }

    result = client.post("/events/?gen_recommendations=False", json=event)
    assert result.status_code == 200
    result_one_participant_id = result.json()["participants_id"]
    result_one_event_id = result.json()["id"]

    result = client.post("/events/?gen_recommendations=False", json=event)
    assert result.status_code == 200
    result_two_participant_id = result.json()["participants_id"]
    result_two_event_id = result.json()["id"]

    assert (
        result_one_event_id != result_two_event_id
    ) and result_one_participant_id == result_two_participant_id
