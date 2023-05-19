from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import *
from app.database import engine
from app.routers.user import *
from app.routers.resource import *
from app.routers.activity import *
from app.routers.transaction import *
from app.routers.picture import *

from js.d3 import d3
d3.need()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_user)
app.include_router(router_resource)
app.include_router(router_activity)
app.include_router(router_transaction)
app.include_router(router_picture)


@app.get("/")
async def root():
    return {"message": "easy start"}