from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.models import *
from app.schemas import *

from app.database import get_db
from sqlalchemy.orm import Session

from blockchain.src.EFT_functions import CreateClub
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

router_user = APIRouter(
                    prefix="/users",
                    tags=["User"]
        )

@router_user.get("")#, response_model=List[Clubs])
def getUser(db: Session = Depends(get_db)):
    usrs = db.query(Club).all()
    return usrs


@router_user.get("/{club_id}", response_model=Clubs)
def getUser(club_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router_user.post("/login")
def userLogin(login: ClubLogin, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==login.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if login.password == db_user.password:
        return signJWT(login.id)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid login details!')


@router_user.patch("/update/{club_id}", dependencies=[Depends(jwtBearer())]) #, response_model=ClubModify)
def updateUser(club_id: int, club: ClubModify, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    _name = ''
    _addr = ''
    if club.name is not None:
        db_user.name = _name = club.name
    if club.password is not None:
        db_user.password = club.password
    if club.address is not None:
        db_user.address = _addr = club.address

    # blockchain
    hash = CreateClub(club_id, _name, _addr)

    db.commit()
    db.refresh(db_user)
    
    return db_user


@router_user.post("/register", response_model=ClubsToken)
def createUser(club: ClubModify, db: Session = Depends(get_db)):
    add_user = Club(
        name = club.name,
        address = club.address,
        password = club.password,
        token = 0
    )
    db.add(add_user)
    db.commit()
    db.refresh(add_user)

    
    # blockchain
    hash = CreateClub(add_user.id, club.name, club.address)

    token = signJWT(add_user.id)

    user_dict = add_user.to_dict()
    return {**user_dict, **token}