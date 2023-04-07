from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    String,
    Column,
    Integer,
    DateTime,
)

from .database import Base


# class User(Base):
#     __tablename__ = "users"

#     student_id = Column(String, primary_key=True)
#     username = Column(String, nullable=False)
#     password = Column(String, nullable=False)   #init default = student_id

#     user_clubs_mem = relationship("ClubMember", back_populates="userID")
#     user_clubs_mini = relationship("ClubMinister", back_populates="userID")
#     user_upload_pics = relationship("Picture", back_populates="userID")

class Club(Base):
    __tablename__ = "clubs"

    club_id = Column(Integer, primary_key=True)
    club_name = Column(String, nullable=False)
    club_address = Column(String, nullable=True)      #how to practice blockchain purse??
    club_code = Column(String, default='0000')

    # club_mems = relationship("ClubMember", back_populates="clubID")
    # club_minis = relationship("ClubMinister", back_populates="clubID")
    club_upload_pics = relationship("Picture", back_populates="clubID")
    club_booked_records = relationship("Booked", back_populates="clubID")
    club_transact_records = relationship("Transaction", back_populates="clubID")


# class ClubMember(Base):    
#     __tablename__ = "club_members"

#     clubmember_id = Column(Integer, primary_key=True)

#     userID = relationship("User", back_populates="user_clubs_mem")
#     clubID = relationship("Club", back_populates="club_mems")


# class ClubMinister(Base):    
#     __tablename__ = "club_ministers"

#     clubminister_id = Column(Integer, primary_key=True)

#     userID = relationship("User", back_populates="user_clubs_mini")
#     clubID = relationship("Club", back_populates="club_minis")


class Picture(Base):
    __tablename__ = "pictures"

    pic_id = Column(Integer, primary_key=True)      #pic_name = pic_id.jpg
    num_friendly = Column(Integer, nullable=False)  #-1: mark as uncheck recheck case
    reportErr_new_picID = Column(Integer, nullable=True)
    pic_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)         #TODO init??, when append a row
    pic_hash = Column(String, nullable=True)
    
    userID = relationship("User", back_populates="user_upload_pics")
    clubID = relationship("Club", back_populates="club_upload_pics")
    activityID = relationship("Activity", back_populates="pics")
    transactID = relationship("Transaction", back_populates="picID")


class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String, nullable=False)
    resource_cost = Column(Integer, nullable=False)

    booked_records = relationship("Booked", back_populates="resourceID")


class Booked(Base):
    __tablename__ = "booked"

    booked_id = Column(Integer, primary_key=True)
    booked_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)         #TODO init??, when append a row
    booked_seg = Column(Integer, nullable=False)    #unit = an hour, number present the start hour
    
    resourceID = relationship("Resource", back_populates="booked_records")
    clubID = relationship("Club", back_populates="club_booked_records")
    transactID = relationship("Transaction", back_populates="bookedID")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    transact_amount = Column(Integer, nullable=False)
    token_left = Column(Integer, nullable=False)
    transact_hash = Column(String, nullable=True)
    transact_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    clubID = relationship("Club", back_populates="club_transact_records")

    #TODO relation 可為空嗎??
    bookedID = relationship("Booked", back_populates="transactID")
    picID = relationship("Picture", back_populates="transactID")
    activityID = relationship("Activity", back_populates="transactID")


class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True)
    activity_name = Column(String, nullable=False)
    activity_date = Column(DateTime, nullable=False)

    pics = relationship("Picture", back_populates="activityID")
    transactID = relationship("Transaction", back_populates="activityID")
    
