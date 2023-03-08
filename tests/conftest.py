import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dependencies import get_db
from main import api
from app import models


@pytest.fixture(scope="session")
def db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    os.remove("./test.db")


@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.rollback()

    api.dependency_overrides[get_db] = override_get_db
    client = TestClient(api)
    return client
