from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session


router_picture = APIRouter(
                    prefix="/pictures"
        )


@router_picture.get("/{activity_id}", response_model=List[Pictures])
def getPictures(activity_id: int, db: Session = Depends(get_db)):
    db_pics = db.query(Picture).filter(Picture.activity_id == activity_id).all()
    if db_pics is None or len(db_pics)==0: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'there is no pics for activity {acticity_id}')
    return db_pics

@router_picture.post("/upload", response_model=PictureUpload)
def uploadPicture(picture: PictureCreate, db: Session = Depends(get_db)):
    #TODO Blockchain
    hash = '0x0000'

    add_pic = Picture(
        num_friendly = picture.num_friendly,
        activity_id = picture.activity_id,
        hash = hash
    )
    #TODO 圖片存檔

    db.add(add_pic)
    db.commit()
    db.refresh(add_pic)

    return add_pic


@router_picture.post("/reportErr")
def reportErr(picture: PictureErrReport, db: Session = Depends(get_db)):
    #TODO Blockchain
    hash = '0x0000'

    db_pic_old = db.query(Picture).filter(Picture.id==picture.reportErr_picID).first()
    add_pic = Picture(
        num_friendly = picture.num_friendly,
        activity_id = db_pic_old.activity_id,
        hash = hash
    )
    db.add(add_pic)
    db.commit()
    db.refresh(add_pic)

    # upadate reportErr_new_picID for old one
    db_pic_old.reportErr_new_picID = add_pic.id
    db.commit()

    return Response(status_code=status.HTTP_200_OK)