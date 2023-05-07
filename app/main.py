from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.models import *
from app.database import engine
from app.routers.user import *
from app.routers.resource import *
from app.routers.activity import *
from app.routers.transaction import *

from js.d3 import d3
d3.need()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router_user)
app.include_router(router_resource)
app.include_router(router_activity)
app.include_router(router_transaction)


@app.get("/")
async def root():
    return {"message": "easy start"}