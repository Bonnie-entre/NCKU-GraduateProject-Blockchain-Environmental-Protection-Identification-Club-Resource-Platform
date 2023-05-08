from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas import *
from app.models import *
from app.database import get_db
from sqlalchemy.orm import Session


router_resource = APIRouter(
                    prefix="/resources"
        )


@router_resource.get("", response_model=List[Resources])
def getResources(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources


@router_resource.get("/occupy/{resource_id}/{booked_day}")
def getOccupy(resource_id: int, booked_day: int, db: Session = Depends(get_db)):
    query_id = resource_id + '_' + booked_day
    db_resource_booked = db.query(Available).filter(Available.resourceId_bookedDay==query_id).first()
    
    if db_resource_booked is None:
        return HTTPException(detail=f'Resource {resource_id} on {booked_day} is available', status_code=status.HTTP_200_OK)
    return db_resource_booked


@router_resource.post("/book")
def createBook(book:BookCreate, db: Session = Depends(get_db)):
    # check token enough
    db_resource = db.query(Resource).filter(Resource.id==book.resource_id).first()
    db_last_transact = db.query(Transaction).filter(Transaction.club_id==book.club_id).order_by(Transaction.id.desc()).first()
    after_transact_token = db_last_transact.token_left - (db_resource.cost * len(book.hr))
    if after_transact_token<0:
        return HTTPException(detail=f'club {book.club_id}''s token={db_last_transact.token_left} < resource''cost={db_resource.cost}*hrs', status_code=status.HTTP_400_BAD_REQUEST)
    
    # TODO 連動 blockchain 進行交易
    hash='0x000'

    # TODO check available - frontend

    # add transact
    add_transact = Transaction(
        amount = db_resource.cost,
        token_left = after_transact_token,
        hash = hash,
        club_id = book.club_id,
    ) 
    db.add(add_transact)
    db.commit()
    db.refresh(add_transact)
    
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
        add_available.id = query_available.id
        query_available.occupy_hr = sorted(list(set(query_available.occupy_hr+book.hr)))
    db.commit()

    # TODO 把 db 的 Booked.hr 改成 array~
    # add booked
    for i in book.hr:
        add_booked = Booked(
            day = book.booked_day,
            hr = i,
            resource_id = book.resource_id,
            club_id = book.club_id,
            tansact_id = add_transact.id,
            available_id = add_available.resourceId_bookedDay
        )
        db.add(add_booked)
        db.commit()

    return add_transact