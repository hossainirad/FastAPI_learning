from fastapi import FastAPI
from models import Person

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/query-parameter/")
async def say_anathor_hello(username: str = None):
    return {"message": f"Hello query parameter {username}"}


@app.post("/first-post/")
async def say_post(req: Person):
    return req
