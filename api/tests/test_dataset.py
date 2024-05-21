import pytest
from fastapi.testclient import TestClient

from api.models import user

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.main import app
from api.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
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
    # app.dependency_overrides.clear()


def test_create_tables(client: TestClient):
    response = client.post(
        "/user/",
        json={
            "birth_year": 2002,
            "country": "US",
            "currency": "USD",
            "gender": "F",
        },
    )
    assert response.status_code == 200
    assert user.UserBase(**response.json())
