from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    String,
    Column,
    Integer,
    ARRAY,
    DateTime,
    Boolean,
    ForeignKey
)

from app.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    password = Column(String, default='0000')

    booked = relationship("Booked", back_populates="club")
    transact = relationship("Transaction", back_populates="club")
    activity = relationship("Activity", back_populates="club")


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True)      #pic_name = pic_id.jpg
    num_friendly = Column(Integer, nullable=False)  #-1: mark as uncheck recheck case
    reportErr_new_picID = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)         #TODO init??, when append a row
    hash = Column(String, nullable=True)
    Err_accept = Column(Boolean, nullable=True)
    base64 = Column(String, nullable=True)
    
    activity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activity", back_populates="picture")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)

    booked = relationship("Booked", back_populates="resource")


class Booked(Base):
    __tablename__ = "booked"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)         #record
    day = Column(String, nullable=True)     #book
    hr = Column(Integer, nullable=False)    #unit = an hour, number present the start hour: 0~23
    
    resource_id = Column(Integer, ForeignKey("resources.id"))
    resource = relationship("Resource", back_populates="booked")
    club_id = Column(Integer, ForeignKey("clubs.id"))
    club = relationship("Club", back_populates="booked")
    transact_id = Column(Integer, ForeignKey("transactions.id"))
    transact = relationship("Transaction", back_populates="booked")
    available_id = Column(String, ForeignKey("availables.resourceId_bookedDay"))
    available_day = relationship("Available", back_populates="occupy_bookedID")


class Available(Base):
    __tablename__ = "availables"

    resourceId_bookedDay = Column(String, primary_key=True)     #ex.'2_20240505'
    occupy_hr = Column(ARRAY(Integer))
    occupy_bookedID = relationship("Booked", back_populates="available_day")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    token_left = Column(Integer, nullable=False)
    hash = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    club_id = Column(Integer, ForeignKey("clubs.id"))
    club = relationship("Club", back_populates="transact")
    acticity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activity", back_populates="transaction")
    booked = relationship("Booked", back_populates="transact")
    

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    club_id = Column(Integer, ForeignKey("clubs.id"))
    club = relationship("Club", back_populates="activity")
    picture = relationship("Picture", back_populates="activity")
    transaction = relationship("Transaction", back_populates="activity")
