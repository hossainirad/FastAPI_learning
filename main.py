import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles


from routers import user, item, home

if __name__ == '__main__':
    uvicorn.run('config:app', host='0.0.0.0', port=8000, reload=True)

api = fastapi.FastAPI()


def configure():
    configure_routing()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(user.router)
    api.include_router(item.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(api)
else:
    configure()
