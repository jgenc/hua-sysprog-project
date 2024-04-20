from ..data.betting import BettingData
from ..schemas import Event, User, Coupon
import pytest


@pytest.fixture
def bd():
    bd = BettingData("./api/data/dummy.json")
    return bd


def test_betting_data(bd):
    assert bd.data is not None, "Data did not load succes"
    assert bd.users is not None
    assert bd.events is not None
    assert bd.coupons is not None


def test_users(bd):
    assert User(**bd.users.sample(20).to_dict(orient="records")[0]) is not None


def test_events(bd):
    assert Event(**bd.events.sample(20).to_dict(orient="records")[0]) is not None


def test_coupons(bd):
    assert Coupon(**bd.coupons.sample(20).to_dict(orient="records")[0]) is not None
