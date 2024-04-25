from ..data.dataframe import BettingDataDataframe
from ..schemas import Event, User, Coupon
import pytest


@pytest.fixture
def bd():
    bd = BettingDataDataframe("./api/data/dummy.json")
    return bd


def test_betting_data(bd):
    assert bd.tables() is not None, "Tables not set correctly"
    assert bd._users is not None
    assert bd._events is not None
    assert bd._coupons is not None


def test_get_data_users(bd):
    user_sample = bd.get_data("users", "user_id", 0)
    assert User(**user_sample.to_dict(orient="records")[0]) is not None


def test_get_data_events(bd):
    event_sample = bd.get_data("events", "event_id", "0")
    assert Event(**event_sample.to_dict(orient="records")[0]) is not None


def test_get_data_coupons(bd):
    coupon_sample = bd.get_data("coupons", "coupon_id", 0)
    assert Coupon(**coupon_sample.to_dict(orient="records")[0]) is not None


def test_events_df(bd):
    assert Event(**bd._events.sample(20).to_dict(orient="records")[0]) is not None


def test_coupons_df(bd):
    assert Coupon(**bd._coupons.sample(20).to_dict(orient="records")[0]) is not None


def test_nonexistant_table(bd):
    with pytest.raises(ValueError):
        bd.get_data("nonexistant", "user_id", "0")
    with pytest.raises(ValueError):
        bd.set_data("nonexistant", "0", "0")
    with pytest.raises(ValueError):
        bd.delete_data("nonexistant", "user_id", "0")
