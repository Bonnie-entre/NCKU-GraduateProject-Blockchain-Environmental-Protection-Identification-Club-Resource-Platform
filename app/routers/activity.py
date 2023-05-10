from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session


router_activity = APIRouter(
                    prefix="/activities"
        )


@router_activity.get("/{activity_id}") #, response_model=List[Activities])
def getActivities(activity_id: int, db: Session = Depends(get_db)):
    db_activities = db.query(Activity).filter(Activity.id==activity_id).all()
    if db_activities is None or len(db_activities)==0: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'there is no activities for activity ID {activity_id}')
    return db_activities
