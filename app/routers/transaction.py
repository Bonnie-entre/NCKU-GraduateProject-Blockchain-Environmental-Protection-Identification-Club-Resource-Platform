


from fastapi import APIRouter, Response, status, Depends
from typing import  List
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session


router_transaction = APIRouter(
                    prefix="/transactions"
        )


@router_transaction.get("/", response_model=List[Transactions])
def getTransactions(club: ClubBase, db: Session = Depends(get_db)):
    db_transactions = db.query(Transaction).filter(Transaction.club_id == club.id).all()
    if db_transactions is None:
        return Response(content = f'there is no activities for club {club.id}', status_code=status.HTTP_404_NOT_FOUND)   
    return db_transactions