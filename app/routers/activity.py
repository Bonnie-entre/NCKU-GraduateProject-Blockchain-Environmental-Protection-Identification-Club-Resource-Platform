from fastapi import APIRouter, FastAPI, Response, status, Depends
# from fastapi.responses import HTMLResponse
from typing import Optional, List
# from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter(
                    prefix="/activities"
        )


@router.get("/")
def getActivities(db: Session = Depends(get_db), userid: str | Optional[str]=None):
    #Activity -> (Picture + Transaction)
    return


# @router.post("/createActivity")
# def createActivity(db: Session = Depends(get_db)):
#     #
#     return