import pytest
from sqlmodel import SQLModel, create_engine, Session, select

from src.app import database as db


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    session = Session(engine)
    yield session
