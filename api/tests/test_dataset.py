import pytest
from fastapi.testclient import TestClient

from api.models import user, event, coupon, recommendations

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.main import app
from api.dependencies.database import get_session

SQLITE_TEST_DB_URL = "test.db"

# IMPORTANT: Import these fixtures to other tests to use the test database


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        f"sqlite:///{SQLITE_TEST_DB_URL}",
        connect_args={"check_same_thread": False},
        # poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        test_user = user.User(
            birth_year=2002,
            country="GR",
            currency="EUR",
            gender="M",
            registration_date="2024-04-01 20:48:20.438063",
            id=0,
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        test_participants = event.Participants(id=0, a="Panathinaikos", b="Real Madrid")
        session.add(test_participants)
        session.commit()
        session.refresh(test_participants)

        test_event = event.Event(
            begin_timestamp="2024-05-29 13:18:00.060583",
            end_timestamp="2024-05-29 13:18:17.512332",
            country="US",
            league="EuroLeague",
            sport="Basketball",
            id=0,
            participants_id=test_participants.id,
        )
        session.add(test_event)
        session.commit()
        session.refresh(test_event)

        test_selection_1 = coupon.Selection(id=0, event_id=0, odds=2.3)
        test_selection_2 = coupon.Selection(id=1, event_id=0, odds=5.9)
        test_selection_3 = coupon.Selection(id=2, event_id=0, odds=0.5)

        session.add(test_selection_1)
        session.add(test_selection_2)
        session.add(test_selection_3)

        session.commit()

        session.refresh(test_selection_1)
        session.refresh(test_selection_2)
        session.refresh(test_selection_3)

        test_coupon_1 = coupon.Coupon(
            id=0,
            selections=[test_selection_1, test_selection_3],
            stake=10.2,
            timestamp="2024-05-29 18:13:20.852628",
            user_id=0,
        )

        session.add(test_coupon_1)

        session.commit()
        session.refresh(test_coupon_1)

        test_recommendation_1 = recommendations.Recommendation(
            id=0, user_id=0, events=[test_event]
        )

        session.add(test_recommendation_1)
        session.commit()
        session.refresh(test_recommendation_1)

        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    # APIRouter object is a "under" the app/FastAPI object. There is no option
    # of adjusting the dependencies of an APIRouter object, the whole FastAPI
    # object has to change the dependency.
    # https://stackoverflow.com/questions/77544046/how-to-override-dependency-apirouter-level-in-pytest
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    import os

    os.remove(SQLITE_TEST_DB_URL)
    app.dependency_overrides.clear()


def test_create_tables(client: TestClient):
    # This is specific for each database.
    import sqlite3

    con = sqlite3.connect(SQLITE_TEST_DB_URL)
    sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    cur = con.cursor()
    created_tables = cur.execute(sql_query).fetchall()
    # The arraysize should be equal to all models (or all created tables)
    assert len(created_tables) == 8
