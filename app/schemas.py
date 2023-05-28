from pydantic import BaseModel

from typing import List, Optional

from datetime import datetime


#picture
class PictureBase(BaseModel):
    id: int

class Pictures(PictureBase):
    num_friendly: int
    reportErr_new_picID: Optional[int] = None
    date: datetime
    hash: str
    activity_id: int

class PictureCreate(BaseModel):
    num_friendly: int
    date: datetime
    activity_id: int
    base64: str

class PictureErrReport(BaseModel):
    reportErr_picID: int
    num_friendly: int

class PictureWrong(BaseModel):
    reportErr_picID: int
    Err_accept: bool


#resources
class ResourceBase(BaseModel):
    id: int
    name: str

class Resources(ResourceBase):
    cost: int

    class Config:
        orm_mode = True
    

#booked
class BookBase(BaseModel):
    id: int

class BookCreate(BaseModel):
    resource_id: int
    booked_day: str
    club_id: int
    hr: List[int]

class BookCreate_Noblockchain(BookCreate):
    hash: str

class Books(BookCreate):
    pass

    class Config:
        orm_mode = True


#user
class ClubBase(BaseModel):
    id: int

class ClubModify(BaseModel):
    password: Optional[str] = '0000'
    name: Optional[str] = None
    address: Optional[str] = '0x'

class ClubLogin(ClubBase):
    password: str

class Clubs(ClubBase):
    password: str
    name: str
    address: Optional[str] = None
    token: int
    # upload_pics: List[Pictures] = []
    # booked_records: List[Books] = []

class ClubsToken(Clubs):
    token: str

    class Config:
        orm_mode = True


#transaction
class TransactionBase(BaseModel):
    id: int

class Transactions(TransactionBase):
    amount: int
    token_left: int
    hash: str
    date: datetime

    class Config:
        orm_mode = True


class ActivityBase(BaseModel):
    id: int

class Activities(ActivityBase):
    name: str
    date: datetime
    state: Optional[bool] = None
    
    class Config:
        orm_mode = True