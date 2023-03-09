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
        print('ative conection ....')
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class GroupManager:
    def __init__(self):
        self.active_rooms = {}
        self.clients = []

    async def connect(self, websocket: WebSocket):
        print('Connection created ...')
        print(self.active_rooms)
        print(self.clients)
        await websocket.accept()
        self.clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)
        for room_id, room in self.active_rooms.items():
            if websocket in room:
                room.remove(websocket)
                await self.broadcast(room_id, f"{websocket} left the room.")
                break

    async def join_room(self, websocket: WebSocket, room_id: str):
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = set()
        room = self.active_rooms[room_id]
        room.add(websocket)
        await self.broadcast(room_id, f"{websocket} joined the room.")

    async def leave_room(self, websocket: WebSocket, room_id: str):
        if room_id not in self.active_rooms:
            return
        room = self.active_rooms[room_id]
        if websocket in room:
            room.remove(websocket)
            await self.broadcast(room_id, f"{websocket} left the room.")

    async def broadcast(self, room_id: str, message: str):
        if room_id not in self.active_rooms:
            return
        room = self.active_rooms[room_id]
        for client in room:
            await client.send_text(message)
