from sqlmodel import SQLModel, create_engine, Session
from api.models import user

sqlite_file_name = "user_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
