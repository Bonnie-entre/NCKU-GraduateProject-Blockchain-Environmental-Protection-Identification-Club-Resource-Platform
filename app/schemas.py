from pydantic import BaseModel

from typing import List, Union

from datetime import datetime


#picture
class PictureBase(BaseModel):
    pic_id: int

class Pictures(PictureBase):
    num_friendly: int
    reportErr_new_picID: int
    pic_date: datetime
    pic_hash: str

class PictureCreate(PictureBase):
    num_friendly: int
    pic_date: datetime

class PictureUpload(PictureBase):
    pic_hash: str

class PictureWrong(PictureBase):
    reportErr_new_picID: int


#booked
class


#user
class ClubBase(BaseModel):
    club_id: int

class ClubCreate(ClubBase):
    password: str
    club_name: str
    club_address: str
    password: str


class Clubs(ClubCreate):
    club_upload_pics: List[Picture] = []
    club_booked_records: List[]

    class Config:
        orm_mode = True


#
class TransactionBase(BaseModel):
    transaction_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    class Config:
        orm_mode = True


#activity
class ActivityBase(BaseModel):
    activity_id: int
    activity_name: str
    activity_date: str
    pics: List[Picture] = []
    transactID: List[Transaction] = []

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    class Config:
        orm_mode = True

