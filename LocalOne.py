from sqlalchemy import Table, create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectin_polymorphic


Base = declarative_base()


##for many to many relation between user and place
association = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('place_id', Integer, ForeignKey('place.id'))
)

class User(Base):
    __tablename__ = "user"
    id = Column('id',Integer,primary_key=True , autoincrement=True)
    first_name = ('firstname',String)
    last_name = ('lastname' , String)
    username = Column('username',String , unique=True)
    admin = Column('admin',Boolean , unique=True)
    password = Column('password' , String)		
    email = Column('email' , String , unique=True)
    googleassist = Column('googleassist' , String)
    
##bidirectional relation between user and place 
    place = relationship("Place",secondary=association , back_populates="user")
    
    account = relationship("Account",			## Cascade to delete associated account
    	back_populates='user',			## if that user was deleted.
        cascade='all, delete-orphan')


    
class Room(Base):
    __tablename__ = "room"
    id = Column('id' , Integer , primary_key=True)
    name = Column('name' , String , unique=True)

    place_id = Column(Integer , ForeignKey('place.id'))
    
##    for one-to many relation with room table
    user_id = Column(Integer , ForeignKey('user.id'))
    
##    for one-to many relation with device table    
    device = relationship("Device",			
    	back_populates='room',				
        cascade='all, delete-orphan')


    
class Schedule(Base):
    __tablename__="schedule"
    id = Column('id' , Integer , primary_key=True)
    start_time = Column('starttime' , DateTime )
    end_time = Column('endtime' , DateTime )
    
    user_id = Column(Integer , ForeignKey('user.id'))

    room_id = Column(Integer , ForeignKey('room.id'))


    
class Activity(Base):
    __tablename__="activity"
    id = Column('id' , Integer , primary_key=True)
    changed_status = Column('changedstatus', String)

    device_id = Column(Integer , ForeignKey('device.id'))


    
class HomeNetwork(Base):
    __tablename__="homenetwork"
    id = Column('id',Integer , primary_key=True)
    ss_id = Column('ssid',Integer)
    password = Column('password', String)
    
    place_id = Column(Integer,ForeignKey('place.id'))



class Place(Base):
    __tablename__="place"
    id = Column('id',Integer,primary_key=True)
    location = Column('location' , String)

    hub_id = Column(Integer , ForeignKey('hub.id'))
##bidirectional relation between user and place
    user = relationship("User",secondary = association , back_populates="place")


    
class Device(Base):
    __tablename__ = "device"
    id = Column( Integer , primary_key=True)
    name = Column('name' , String)
    manufacturer = Column('manufacturer',String)
    power_consumption = Column('powerconsumption',Integer)
    
    room_id = Column(Integer , ForeignKey('room.id'))
    
##    to specify the device table as a parent in the inheritence
    type = Column( String)

    __mapper_args__ = {'polymorphic_identity':'device', 'polymorphic_on': type
        }


    
class Hub(Device):
    __tablename__ = "hub"
    id = Column(Integer , ForeignKey('device.id'), primary_key=True)		
    ##    inherit from the parent table device
    

    __mapper_args__ = {'polymorphic_identity':'hub' 
        }


    
class Controller(Device):
    __tablename__ = "controller"
    id = Column( Integer , ForeignKey('device.id'), primary_key=True)
    status = Column('status', Boolean)
    ##    inherit from the parent table device
    

    __mapper_args__ = {'polymorphic_identity':'controller'
        }





engine = create_engine('sqlite:///withhub.db')
Base.metadata.create_all(engine)
