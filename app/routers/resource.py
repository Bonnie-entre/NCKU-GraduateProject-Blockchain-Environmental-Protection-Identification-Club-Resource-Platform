from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas import *
from app.models import *
from app.database import get_db
from sqlalchemy.orm import Session

from blockchain.src.EFT_functions import BookResource_backend
from app.auth.jwt_bearer import jwtBearer


router_resource = APIRouter(
                    prefix="/resources",
                    tags=['Resource']
        )


@router_resource.get("", response_model=List[Resources])
def getResources(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources


@router_resource.get("/free")
def getOccupy(resource_id: str, booked_day: str, db: Session = Depends(get_db)):
    query_id = resource_id + '_' + booked_day
    db_resource_booked = db.query(Available).filter(Available.resourceId_bookedDay==query_id).first()
    
    if db_resource_booked is None:
        return HTTPException(detail=f'Resource {resource_id} on {booked_day} is available', status_code=status.HTTP_200_OK)
    db_free = db_resource_booked.to_dict()
    free = []
    x = 9
    for i in range(len(db_free["occupy_hr"])):
        if x==db_free["occupy_hr"][i]:
            i+=1
        else:
            free.append(x)
        x+=1
    
    while(x<=21):
        free.append(x)
        x+=1
    del db_free["occupy_hr"]
    db_free["free_hour"] = free

    return {**db_free}


@router_resource.post("/book", dependencies=[Depends(jwtBearer())])
def createBook(book:BookCreate, db: Session = Depends(get_db)):
    # check token enough
    db_resource = db.query(Resource).filter(Resource.id==book.resource_id).first()
    db_last_transact = db.query(Transaction).filter(Transaction.club_id==book.club_id).order_by(Transaction.id.desc()).first()
    after_transact_token = db_last_transact.token_left - (db_resource.cost * len(book.hr))
    if after_transact_token<0:
        return HTTPException(detail=f'club {book.club_id}\'s token={db_last_transact.token_left} < resource\'cost={db_resource.cost}*hrs', status_code=status.HTTP_400_BAD_REQUEST)
    
    # blockchain
    hash = BookResource_backend(
                        book.club_id,
                        book.resource_id,
                        str(book.booked_day)
    )


    # TODO check available - frontend


    # add transact
    add_transact = Transaction(
        amount = db_resource.cost* len(book.hr),
        token_left = after_transact_token,
        hash = hash,
        club_id = book.club_id,
    ) 
    
    # add available
    query_id = f'{book.resource_id}_{book.booked_day}'
    query_available = db.query(Available).filter(Available.resourceId_bookedDay==query_id).first()
    if query_available is None:        
        add_available = Available(
            resourceId_bookedDay = query_id,
            occupy_hr = book.hr
        )
        db.add(add_available)
    else:
        query_available.occupy_hr = sorted(list(set(query_available.occupy_hr+book.hr)))
    

    # TODO 把 db 的 Booked.hr 改成 array~ for 減少資料數目, but why booked?
    # add booked
    for i in book.hr:
        add_booked = Booked(
            day = book.booked_day,
            hr = i,
            resource_id = book.resource_id,
            club_id = book.club_id,
            transact_id = add_transact.id,
            available_id = query_id
        )
        db.add(add_booked)
        db.add(add_transact)
        db.commit()
        db.refresh(add_transact)

    return add_transact