##creating a database by sqlalchemy - sqlite 
from sqlalchemy import create_engine , Column , Integer , String , ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

##create classes that include
##directives to describe the actual database table they will be mapped to.
Base = declarative_base()

##user table
class User(Base):
    __tablename__ = "user"
    id = Column('id',Integer,primary_key=True , autoincrement=True)
    username = Column('username',String , unique=True)
    password = Column('password' , String)		##[Asmer] password doesn't have to be unique
    email = Column('email' , String , unique=True)
    googleassist = Column('googleassist' , String)	##[Asmer] user_id include alphabetic characters	
    alexa = Column('alexa',String) ##[Asmer] user_id include alphabetic characters	
##    for one-to many relation with room table
    room = relationship("Room",			##[Asmer] Cascade to delete associated rooms
    	back_populates='user',			## if that user was deleted.
        cascade='all, delete-orphan')


class Room(Base):
    __tablename__ = "room"
    id = Column('id' , Integer , primary_key=True)
    name = Column('name' , String , unique=True)
##    for one-to many relation with room table
    user_id = Column(Integer , ForeignKey('user.id'))
##    for one-to many relation with device table    
    device = relationship("Device",			##[Asmer] Cascade to delete associated devices
    	back_populates='room',				## if that room was deleted.
        cascade='all, delete-orphan')

class Device(Base):
    __tablename__ = "device"
    id = Column('id' , Integer , primary_key=True)
    name = Column('name' , String)
    room_id = Column(Integer , ForeignKey('room.id'))
##    to specify the device table as a parent in the inheritence
    type = Column(String)

    __mapper_args__ = {'polymorphic_identity':'device', 'polymorphic_on': type
        }

class Hub(Device):
    __tablename__ = "hub"
    id = Column(ForeignKey('device.id'), primary_key=True)		##[Asmer] The FK and The PK are the same here
    ##    inherit from the parent table device
    
    # device_id = Column(Integer , ForeignKey('device.id'))

    __mapper_args__ = {'polymorphic_identity':'hub'
        }

class Controller(Device):
    __tablename__ = "controller"
    id = Column(ForeignKey('device.id'), primary_key=True)		##[Asmer] The FK and The PK are the same here
    # id = Column('id' , Integer , primary_key=True)
    ##    inherit from the parent table device
    
    # device_id = Column(Integer , ForeignKey('device.id'))

    __mapper_args__ = {'polymorphic_identity':'controller'
        }

    
    
    

engine = create_engine('sqlite:///hifa.db')
Base.metadata.create_all(engine)
