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
    activity_id: int
    hr: List[int]

class Books(BookCreate):
    pass

    class Config:
        orm_mode = True


#user
class ClubBase(BaseModel):
    id: int

class ClubModify(BaseModel):
    password: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None

class Clubs(ClubBase):
    password: str
    name: str
    address: Optional[str] = None
    upload_pics: List[Pictures] = []
    booked_records: List[Books] = []

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


