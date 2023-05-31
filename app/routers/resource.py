from fastapi import APIRouter, Response, status, Depends
from typing import List

from app.schemas import *
from app.models import *
from app.database import get_db
from sqlalchemy.orm import Session

from blockchain.src.EFT_functions import BookResource_backend, CreateResource
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
    
    # all available 
    if db_resource_booked is None:
        free = {'resourceId_bookedDay': query_id, 
                'free_hour':[9,10,11,12,13,14,15,16,17,18,19,20,21]
                }
        return {**free}
    
    # some available
    db_free = db_resource_booked.to_dict()
    free = []
    x = 9
    i = 0
    list_occupy = sorted(db_free["occupy_hr"])
    while(x<=21):
        if i<len(db_free["occupy_hr"]) and x==list_occupy[i]:
                print(i, list_occupy[i])
                i+=1
        else:
            free.append(x)
        x+=1
    
    del db_free["occupy_hr"]
    db_free["free_hour"] = free

    return {**db_free}


@router_resource.post("/book", dependencies=[Depends(jwtBearer())])
def createBook_Noblockchain(book:BookCreate_Noblockchain, db: Session = Depends(get_db)):
    
    # club - token
    db_user = db.query(Club).filter(Club.id==book.club_id).first()
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f'Club ID {book.club_id} doesn\'t exist.')
    
    db_resource = db.query(Resource).filter(Resource.id==book.resource_id).first()
    
    # check token enough
    token_left = db_user.token
    after_transact_token = token_left - (db_resource.cost * len(book.hr))
    if after_transact_token<0:
        return Response(content=f'club {book.club_id}\'s token={token_left} < resource\'cost={db_resource.cost}*hrs', status_code=status.HTTP_400_BAD_REQUEST)

    db_user.token = after_transact_token
    db.add(db_user)
    db.commit()
   

    # TODO check available - frontend


    # add transact
    add_transact = Transaction(
        amount = db_resource.cost* len(book.hr),
        token_left = after_transact_token,
        hash = book.hash,
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
        db.commit()
    else:
        query_available.occupy_hr = sorted(list(set(query_available.occupy_hr+book.hr)))
        db.add(query_available)
        db.commit()
    

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


@router_resource.post("/book/blockchain", dependencies=[Depends(jwtBearer())])
def createBook_blockchain(book:BookCreate, db: Session = Depends(get_db)):
    # check token enough
    db_resource = db.query(Resource).filter(Resource.id==book.resource_id).first()
    db_last_transact = db.query(Transaction).filter(Transaction.club_id==book.club_id).order_by(Transaction.id.desc()).first()
    _cost = db_resource.cost * len(book.hr)
    after_transact_token = db_last_transact.token_left - _cost
    if after_transact_token<0:
        return Response(content=f'club {book.club_id}\'s token={db_last_transact.token_left} < resource\'cost={db_resource.cost}*hrs', status_code=status.HTTP_400_BAD_REQUEST)
    
    # blockchain
    hash = BookResource_backend(
                        book.club_id,
                        book.resource_id,
                        str(book.booked_day),
                        _cost*(10**18)
    )


    # TODO check available - frontend


    # add transact
    add_transact = Transaction(
        amount = db_resource.cost* len(book.hr),
        token_left = after_transact_token,
        hash = hash,
        club_id = book.club_id,
    ) 


    # club - token
    db_user = db.query(Club).filter(Club.id==book.club_id).first()
    db_user.token = after_transact_token
    db.add(db_user)
    db.commit()

    # add available
    query_id = f'{book.resource_id}_{book.booked_day}'
    query_available = db.query(Available).filter(Available.resourceId_bookedDay==query_id).first()
    if query_available is None:        
        add_available = Available(
            resourceId_bookedDay = query_id,
            occupy_hr = book.hr
        )
        db.add(add_available)
        db.commit()
        print("no")
    else:
        print("y", query_available.resourceId_bookedDay)
        query_available.occupy_hr = sorted(list(set(query_available.occupy_hr+book.hr)))       
        db.add(query_available)
        db.commit()
    

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


@router_resource.post("/create")
def createResource(name: str, cost: int, db: Session = Depends(get_db)):
    add_resource = Resource(
            name = name,
            cost = cost
        )
    db.add(add_resource)
    db.commit()
    db.refresh(add_resource)
    
    hash = CreateResource(
                        add_resource.id,
                        name,
                        cost
    )

    return add_resource
