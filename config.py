import fastapi
from fastapi.middleware.cors import CORSMiddleware
api = fastapi.FastAPI(
    websocket_authenticate=False,
)


# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)