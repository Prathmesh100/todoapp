from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(260),unique=True)
    username=Column(String(260),unique=True)
    first_name=Column(String(260))
    last_name=Column(String(260))
    hashed_password=Column(String(260))
    isActive=Column(Boolean,default=True)
    role=Column(String(260))
    phone_number=Column(String(10))

class Todos(Base):
    __tablename__ = 'todos'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(260))
    description=Column(String(260))
    priority=Column(Integer)
    complete=Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey('users.id'))