from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from . import models
from .database import engine
from .routers import user

from js.d3 import d3
d3.need()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)


@app.get("/")
async def root():
    # return HTMLResponse(content=html_main(), status_code=200)
    return {"message": "easy start"}