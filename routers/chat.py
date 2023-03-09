from fastapi.templating import Jinja2Templates
import fastapi
from fastapi.websockets import WebSocket, WebSocketDisconnect
from starlette.requests import Request

from app.chat_managers import ChatManager, GroupManager

templates = Jinja2Templates(directory="templates")


router = fastapi.APIRouter()
chat_manager = ChatManager()
group_manager = GroupManager()


@router.get('/socket.io.js')
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/socket.io.js')


@router.get("/chat/all")
async def chat_bot(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket('/ws/chat')
async def chat_room(websocket: WebSocket):
    await chat_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)


@router.get("/chat/group")
async def group_chat_bot(request: Request):
    return templates.TemplateResponse("group-chat.html", {"request": request})


@router.websocket('/ws/group')
async def group_room(websocket: WebSocket):
    await group_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            parts = data.split(' ')
            command = parts[0]
            if command == 'join':
                await group_manager.join_room(websocket, parts[1])
            elif command == 'leave':
                await group_manager.leave_room(websocket, parts[1])
            else:
                await group_manager.broadcast("default", f"{data}")
    except WebSocketDisconnect:
        await group_manager.disconnect(websocket)

