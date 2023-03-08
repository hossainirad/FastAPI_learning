import os

from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import crud, models
from main import api

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def test_create_user(client, db: Session):
    user_data = {"email": "example@test.com", "password": "secret_password"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    # Check that user was actually saved to database
    db_user = crud.get_user_by_email(db, email=user_data["email"])
    assert db_user is not None
    assert db_user.email == user_data["email"]
    db.close()


def test_create_duplicate_user(client):
    user_data = {"email": "example@test.com", "password": "secret_password"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_upload_file(client):
    # create a temporary file to use for testing
    filename = "test.mp4"
    with open(filename, "wb") as f:
        f.write(b"test")

    with open(filename, "rb") as file:
        response = client.post("/upload/video-upload/", files={"video": (filename, file)})

    # check that the response is successful
    assert response.status_code == 200

    # check that the returned file information is correct
    response_data = response.json()
    assert response_data["filename"] == filename
    assert os.path.exists(response_data["filepath"])
    assert response_data["filesize"] == os.path.getsize(response_data["filepath"])

    # delete the temporary file
    os.remove(filename)
    os.remove(response_data["filepath"])
