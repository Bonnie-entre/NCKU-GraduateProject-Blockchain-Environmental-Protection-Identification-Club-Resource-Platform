from fastapi import APIRouter, FastAPI, Response, status, Depends
# from fastapi.responses import HTMLResponse
from typing import Optional, List
# from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter()    #prefix="/files"


@router.get("/users")
def getUser(db: Session = Depends(get_db), userid: str | Optional[str]=None):
    return


@router.post("/createUser")
def createUser(db: Session = Depends(get_db)):
    return