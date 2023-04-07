from pydantic import BaseModel

from typing import List, Union

#club member
class ClubMemberBase(BaseModel):
    clubmember_id: int
    # userID: 
    # clubID: 

class ClubMemberCreate(ClubMemberBase):
    pass

class ClubMember(ClubMemberBase):
    class Config:
        orm_mode = True


#club minister
class ClubMinisterBase(BaseModel):
    clubminister_id: int

class ClubMinisterCreate(ClubMinisterBase):
    pass

class ClubMinister(ClubMinisterBase):
    class Config:
        orm_mode = True

#picture
class PictureBase(BaseModel):
    pic_id: int
class PictureCreate(PictureBase):
    pass
class


#user
class UserBase(BaseModel):
    student_id: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_clubs_mem: List[ClubMember] = []
    user_clubs_mini: List[ClubMinister] = []
    user_upload_pics: List[Picture] = []
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

