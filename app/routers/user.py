from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.models import *
from app.schemas import *

from app.database import get_db
from sqlalchemy.orm import Session

from eth_utils import is_checksum_address
from blockchain.src.EFT_functions import CreateClub
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

router_user = APIRouter(
                    prefix="/users",
                    tags=["User"]
        )


@router_user.get("")
def getUser(db: Session = Depends(get_db)):
    usrs = db.query(Club).all()
    return usrs


@router_user.get("/user")
def getUser(club_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    return db_user


@router_user.post("/login")
def userLogin(login: ClubLogin, db: Session = Depends(get_db)):
    db_user = db.query(Club).filter(Club.id==login.id).first()
    if db_user is None:
        return Response(status_code=404, content="User not found")
    
    if login.password == db_user.password:
        return signJWT(login.id)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED, content='Invalid login details!')


@router_user.patch("/update", dependencies=[Depends(jwtBearer())]) #, response_model=ClubModify)
def updateUser(club_id: int, club: ClubModify, db: Session = Depends(get_db)):
    if not is_checksum_address(club.address):
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f'Invalid Address')
    
    db_user = db.query(Club).filter(Club.id==club_id).first()
    if db_user is None:
        raise Response(status_code=404, content="User not found")
    
    if club.name is None or club.password is None or club.address is None:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f'Invalid parameters')

    db_user.name = _name = club.name
    db_user.password = club.password
    db_user.address = _addr = club.address

    # blockchain
    hash = CreateClub(club_id, _name, _addr)

    db.commit()
    db.refresh(db_user)
    
    return db_user


@router_user.post("/register")#, response_model=ClubsToken)
def createUser(club: ClubModify, db: Session = Depends(get_db)):
    if not is_checksum_address(club.address):
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f'Invalid Address')

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