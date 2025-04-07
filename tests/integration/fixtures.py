import os
import pytest
import tempfile
from sqlmodel import SQLModel, create_engine, Session, select


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    session = Session(engine)
    yield session


@pytest.fixture
def db_uri():
    file = tempfile.NamedTemporaryFile(delete=False)
    file.close()
    uri = f"sqlite:///{file.name}"
    engine = create_engine(uri)
    SQLModel.metadata.create_all(engine)
    engine.dispose()

    yield uri
    os.remove(file.name)
