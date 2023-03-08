import os
import uuid

import aiofiles
from fastapi import UploadFile


# function to save the uploaded file to disk
async def save_upload_file(upload_file: UploadFile) -> str:
    extension = os.path.splitext(upload_file.filename)[-1]
    filename = f"{uuid.uuid4()}{extension}"
    file_path = f"uploads/{filename}"

    # Create the uploads directory if it doesn't already exist
    os.makedirs("uploads", exist_ok=True)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await upload_file.read()
        await out_file.write(content)
    return file_path