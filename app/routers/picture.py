from fastapi import APIRouter, Response, status, Depends
from typing import List
from app.models import *
from app.schemas import *
from app.database import get_db
from sqlalchemy.orm import Session

from blockchain.src.EFT_functions import uploadPic, ModifyPicnum_Add, ModifyPicnum_Retake
from app.auth.jwt_bearer import jwtBearer

router_picture = APIRouter(
                    prefix="/pictures",
                    tags=["Activity"]
        )


@router_picture.get("")
def getPictures(activity_id: int, db: Session = Depends(get_db)):
    db_pics = db.query(Picture).filter(Picture.activity_id == activity_id).all()
    if db_pics is None or len(db_pics)==0: 
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f'there is no pics for activity {activity_id}')
    return db_pics


@router_picture.post("/upload", dependencies=[Depends(jwtBearer())]) #, response_model=Pictures)
def uploadPicture(picture: PictureCreate, db: Session = Depends(get_db)):
    
    db_activity = db.query(Activity).filter(Activity.id==picture.activity_id).first()
    if db_activity is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f'acrivity ID {picture.activity_id} doesn\'t exit')
    
    # Upload state
    if (datetime.now()-db_activity.date).days>3 or db_activity.state==False:
        db_activity.state = False
        db.add(db_activity)
        db.commit()
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f'Exceed 3 days, uploading not allow!')

    if db_activity.state:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f'Cannot upload again!')

    db_activity.state = True

    #Blockchain
    db_last_ID = db.query(Picture).order_by(Picture.id.desc()).first().id
    hash = uploadPic(
                        db_activity.club_id,
                        picture.activity_id,
                        db_activity.name,
                        str(picture.date),
                        db_last_ID,
                        picture.num_friendly*(10**18),
                        picture.base64
    )


    # add Picture
    add_pic = Picture(
        num_friendly = picture.num_friendly,
        activity_id = picture.activity_id,
        base64 = picture.base64,
        hash = hash
    )


    #add Transaction
    db_last_transact = db.query(Transaction).filter(Transaction.club_id==db_activity.club_id).order_by(Transaction.id.desc()).first()
    add_transact = Transaction(
        amount = picture.num_friendly,  #1:1
        token_left = db_last_transact.token_left + picture.num_friendly,
        hash = hash,
        club_id = db_activity.club_id,
    ) 
    db.add(add_transact)
    db.add(add_pic)
    db.add(db_activity)
    db.commit()
    db.refresh(add_transact)
    db.refresh(add_pic)

    return add_pic


@router_picture.post("/reportErr", dependencies=[Depends(jwtBearer())])
def reportErr(picture: PictureErrReport, db: Session = Depends(get_db)):
    # Blockchain, only make sure modify would upload to blackchain. So, here doon't need to

    # add picture
    db_pic_old = db.query(Picture).filter(Picture.id==picture.reportErr_picID).first()
    add_pic = Picture(
        num_friendly = picture.num_friendly,
        activity_id = db_pic_old.activity_id,
    )
    db.add(add_pic)
    db.commit()
    db.refresh(add_pic)

    # upadate reportErr_new_picID for old one
    db_pic_old.reportErr_new_picID = add_pic.id
    db.commit()

    return Response(status_code=status.HTTP_200_OK)


# Only For Backend Check
@router_picture.post("/backend/checkErr")
def checkErr_Add(picture: PictureWrong, db: Session = Depends(get_db)):
    # Assign table Picture's Err_accept of reportErr_picID 
    db_pic_err = db.query(Picture).filter(Picture.id==picture.reportErr_picID).first()
    
    # reject the ErrReport
    if not picture.Err_accept:
        db_pic_err.Err_accept = False
        db.add(db_pic_err)
        db.commit()
        db.refresh(db_pic_err)
        return db_pic_err
    

    # accept the ErrReport
    db_pic_err.Err_accept = True
    db_pic_old = db.query(Picture).filter(Picture.reportErr_new_picID==picture.reportErr_picID).first()
    if db_pic_old is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f'picture ID{picture.reportErr_picID} was covered by another errID')
    
    token_old = db_pic_old.num_friendly
    token_new = db_pic_err.num_friendly
    db_pic_old.num_friendly = db_pic_err.num_friendly


    # TODO 有賒帳機制嗎，當已經先花掉了
    # blockchain - call contract modify function
    db_activity = db.query(Activity).filter(Activity.id==db_pic_old.activity_id).first()
    print(F'token_old: {token_old}')
    print(F'token_new: {token_new}')
    if token_old > token_new:
        hash = ModifyPicnum_Retake(
                                    db_activity.club_id,
                                    db_activity.id,
                                    db_activity.name,
                                    token_old,
                                    db_pic_old.id,
                                    token_new,
                                    (token_old-token_new)*(10**18)
                                )
    else:
        hash = ModifyPicnum_Add(
                                    db_activity.club_id,
                                    db_activity.id,
                                    db_activity.name,
                                    token_old,
                                    db_pic_old.id,
                                    token_new,
                                    (token_new-token_old)*(10**18)
                                )
    
     
    # add Transaction, renew token_left
    amount = token_new-token_old
    db_last_transact = db.query(Transaction).filter(Transaction.club_id==db_activity.club_id).order_by(Transaction.id.desc()).first()
    add_transact = Transaction(
        amount = amount,  #1:1
        token_left = db_last_transact.token_left + amount,
        hash = hash,
        club_id = db_activity.club_id,
    ) 

    db.add(add_transact)    
    db.add(db_pic_err)
    db.add(db_pic_old)
    db.commit()
    db.refresh(db_pic_old)

    return db_pic_old

