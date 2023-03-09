import os
import uuid
from typing import List

import aiofiles
from fastapi import UploadFile
from fastapi.websockets import WebSocket, WebSocketDisconnect


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



class ChatManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ChatManager()

async def chat_room(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)