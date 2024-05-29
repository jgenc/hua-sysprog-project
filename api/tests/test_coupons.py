from fastapi import HTTPException
from fastapi.testclient import TestClient

import pytest

from api.models import coupon
from api.routers import coupons
from api.tests.test_dataset import session_fixture, client_fixture

client = TestClient(coupons.router)


def test_get_coupon_userid_api(client):
    # Added user has no coupons, response should be an empty list
    response = client.get("/coupon/user/0")

    assert response.status_code == 200
    assert len(response.json()[0]["selections"]) == 2


def test_get_coupon_userid_api_flawed(client):
    response = client.get("/coupon/user/-10")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_coupon_id_api(client):
    result = client.get("/coupon/0")

    assert result.status_code == 200
    assert coupon.Coupon(**result.json())


def test_get_coupon_id_api_flawed(client):
    result = client.get("/coupon/-1")

    assert result.status_code == 404


def test_post_coupon(client):
    response = client.post(
        "/coupon",
        json={"user_id": 0, "stake": 42.2, "selections": [{"event_id": 0, "odds": 30}]},
    )

    print(f"[\x1b[1;31mDEBUG\x1b[0m] {response.json()}")

    assert response.status_code == 200
