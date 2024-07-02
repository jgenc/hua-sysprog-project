from sqlmodel import SQLModel, create_engine, Session
from api.models import user
import os

# Local development will use the relative path
if os.getenv("ENV") == "dev":
    sqlite_file_name = "user_data_dev.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
else:
    sqlite_file_name = "user_data.db"
    # sqlite db will live in /user_data.db in the container
    sqlite_url = f"sqlite:////api/data/{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
