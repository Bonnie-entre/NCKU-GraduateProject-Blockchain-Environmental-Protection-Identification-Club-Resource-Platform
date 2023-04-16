from fastapi import APIRouter, FastAPI, Response, status, Depends
# from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter()    

@router.get("/users")
def getUser(_club_id: int, db: Session = Depends(get_db)):
    #Club -> (Booked -> Resource)
    usrs = db.query(models.Club).all()
    return usrs

@router.get("/users/{_club_id}")
def getUser(_club_id: int, db: Session = Depends(get_db)):
    #Club -> (Booked -> Resource)
    usr = db.query(models.Club).filter(models.Club.club_id==_club_id).first
    return usr


@router.post("/createUser")
def createUser(db: Session = Depends(get_db)):
    #CLub
    return