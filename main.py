from config import api
import uvicorn
from starlette.staticfiles import StaticFiles


from routers import user, item, home, video_upload, chat


def configure():
    configure_routing()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(user.router)
    api.include_router(item.router)
    api.include_router(video_upload.router)
    api.include_router(chat.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(api, host='0.0.0.0', port=8000, reload=True)
else:
    configure()
