from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.models import *
from app.schemas import *

from app.database import get_db
from sqlalchemy.orm import Session


router_user = APIRouter(
                    prefix="/users")

@router_user.get("", response_model=List[Clubs])
def getUser(db: Session = Depends(get_db)):
    usrs = db.query(Club).all()
    return usrs


@router_user.get("/{club_id}", response_model=Clubs)
def getUser(club_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router_user.patch("/update/{club_id}") #, response_model=ClubModify)
def updateUser(club_id: int, club: ClubModify, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if club.name is not None:
        db_user.name = club.name
    if club.password is not None:
        db_user.password = club.password
    if club.address is not None:
        db_user.address = club.address
    db.commit()
    db.refresh(db_user)
    
    return db_user
