from fastapi import HTTPException
from fastapi.testclient import TestClient

import pytest

from ..schemas import Coupon

from ..routers import coupons

client = TestClient(coupons.router)


def test_get_coupon_random_api():
    response = client.get("/coupon/random")

    assert response.status_code == 200
    assert Coupon(**response.json())


def test_get_coupon_userid_api():
    # Added user has no coupons, response should be an empty list
    response = client.get("/coupon/user/0")

    assert response.status_code == 200
    assert response.json() == []


def test_get_coupon_userid_api_flawed():
    # Non-existant user
    with pytest.raises(HTTPException) as err:
        client.get("/coupon/user/-10")

    assert err.value.status_code == 404


def test_get_coupon_id_api():
    result = client.get("/coupon/0")

    assert result.status_code == 200
    assert Coupon(**result.json())


def test_get_coupon_id_api_flawed():
    with pytest.raises(HTTPException) as err:
        client.get("/coupon/-1")

    assert err.value.status_code == 404
