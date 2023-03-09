import os

import fastapi
from fastapi import File, UploadFile

from app.db_config import SessionLocal
from app.models import Video
from app.chat_managers import save_upload_file

router = fastapi.APIRouter()


# route to handle file upload
@router.post("/upload/video-upload/")
async def upload_video_file(video: UploadFile = File(...)):
    # save the file to disk
    file_path = await save_upload_file(video)

    # create a database session
    db = SessionLocal()

    # create a new video object
    new_video = Video(
        filename=video.filename,
        filepath=file_path,
        filesize=os.path.getsize(file_path)
    )

    # add the video object to the database
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    # return the video object as JSON
    return new_video
