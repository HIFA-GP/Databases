from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column('id',Integer,primary_key=True , autoincrement=True)
    username = Column('username',String , unique=True)
    password = Column('password' , String)		
    email = Column('email' , String , unique=True)
    location = Column('location' , String)
    googleassist = Column('googleassist' , String)		
    alexa = Column('alexa',String)
    account = relationship("Account",			## Cascade to delete associated account
    	back_populates='user',			## if that user was deleted.
        cascade='all, delete-orphan')

class Room(Base):
    __tablename__ = "room"
    id = Column('id' , Integer , primary_key=True)
    name = Column('name' , String , unique=True)
##    for one-to many relation with room table
    user_id = Column(Integer , ForeignKey('user.id'))
##    for one-to many relation with device table    
    device = relationship("Device",			
    	back_populates='room',				
        cascade='all, delete-orphan')


class Device(Base):
    __tablename__ = "device"
    id = Column('id' , Integer , primary_key=True)
    name = Column('name' , String)
    status = Column('status', Boolean)
    room_id = Column(Integer , ForeignKey('room.id'))
##    to specify the device table as a parent in the inheritence
    type = Column(String)

    __mapper_args__ = {'polymorphic_identity':'device', 'polymorphic_on': type
        }

class Hub(Device):
    __tablename__ = "hub"
    id = Column(ForeignKey('device.id'), primary_key=True)		
    ##    inherit from the parent table device
    

    __mapper_args__ = {'polymorphic_identity':'hub'
        }

class Controller(Device):
    __tablename__ = "controller"
    id = Column(ForeignKey('device.id'), primary_key=True)		
    ##    inherit from the parent table device
    

    __mapper_args__ = {'polymorphic_identity':'controller'
        }





engine = create_engine('sqlite:///withhub.db')
Base.metadata.create_all(engine)
