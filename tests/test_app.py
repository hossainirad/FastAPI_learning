import os
from httpx import AsyncClient
from starlette.testclient import TestClient
from main import api

client = TestClient(api)


async def test_upload_file():
    # create a temporary file to use for testing
    filename = "test.mp4"
    with open(filename, "wb") as f:
        f.write(b"test")

    # send a POST request to the file upload endpoint
    # with AsyncClient(app=api, base_url="http://localhost") as client:
    #     response = await client.post("/upload/video-upload/", files={"file": (filename, open(filename, "rb"))})


    async with AsyncClient(app=api, base_url="http://localhost") as client:
        with open(filename, "rb") as file:
            response = await client.post("/upload/video-upload/", files={"video": (filename, file)})



    # check that the response is successful
    assert response.status_code == 200

    # check that the returned file information is correct
    response_data = response.json()
    assert response_data["filename"] == filename
    assert os.path.exists(response_data["filepath"])
    assert response_data["filesize"] == os.path.getsize(response_data["filepath"])

    # delete the temporary file
    os.remove(filename)

