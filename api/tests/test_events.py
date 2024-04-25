import pytest

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from pydantic import ValidationError

from ..schemas import Event
from ..routers import events

client = TestClient(events.router)


def test_get_random_event():
    response = client.get("/event/random")

    assert response.status_code == 200
    assert Event(**response.json())


def test_get_event():
    response = client.get("/event/0")

    assert response.status_code == 200
    assert Event(**response.json())


def test_read_event_not_found():
    with pytest.raises(HTTPException) as err:
        client.get("/event/-1")

    assert err.value.status_code == 404


def test_create_event():
    event = {
        "begin_timestamp": "2021-01-01T00:00:00",
        "end_timestamp": "2021-01-01T01:00:00",
        "country": "US",
        "event_id": "32",
        "league": "NBA",
        "participants": ["Lakers", "Warriors"],
        "sport": "Basketball",
    }

    # FIXME: Why do I have to do this this way? In Coupons testing I don't need
    # to wrap the response in a pytest.raises() block
    with pytest.raises(HTTPException) as err:
        client.post("/event/", json=event)

    assert err.value.status_code == 501
