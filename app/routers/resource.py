from fastapi import APIRouter, FastAPI, Response, status, Depends
# from fastapi.responses import HTMLResponse
from typing import Optional, List
# from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter(
                    prefix="/resources"
        )


@router.get("/")
def getResources(db: Session = Depends(get_db), userid: str | Optional[str]=None):
    #Reaouce -> Booked 
    return


@router.post("/Book")
def createBook(db: Session = Depends(get_db)):
    # check available (token)
    return