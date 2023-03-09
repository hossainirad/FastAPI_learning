from fastapi.templating import Jinja2Templates
import fastapi
from fastapi.websockets import WebSocket, WebSocketDisconnect
from starlette.requests import Request

templates = Jinja2Templates(directory="templates")


router = fastapi.APIRouter()


@router.get("/chat/")
async def chat_bot(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})