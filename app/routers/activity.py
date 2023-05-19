from fastapi import APIRouter, HTTPException, status, Depends
from app.models import *
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import asc


router_activity = APIRouter(
                    prefix="/activities",
                    tags=["Activity"]
        )


@router_activity.get("")
def getActivities(club_id: int, db: Session = Depends(get_db)):
    db_activities = db.query(Activity).filter(Activity.club_id==club_id).order_by(asc(Activity.date)).all()
    if db_activities is None or len(db_activities)==0: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'there is no activities for Club ID {club_id}')
    
    activities = []
    for i in db_activities:
        activities.append(i.to_dict_without_clubid())
    return activities
