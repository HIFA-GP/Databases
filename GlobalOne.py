from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
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


class Account(Base):
    __tablename__ = "account"
    id = Column('id', Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer , ForeignKey('user.id'))
    last_login = Column(DateTime() )
    last_logout = Column(DateTime())
    

engine = create_engine('sqlite:///withServer.db')
Base.metadata.create_all(engine)
    
