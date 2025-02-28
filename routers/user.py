from fastapi import APIRouter,Depends,HTTPException,Path
from models import Todos,Users
from database import engine,sessionLocal
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext
router=APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)

class UserPhone(BaseModel):
    phone_number:str=Field(min_length=10,max_length=10)
@router.get('/')
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()


@router.put('/password')
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.__get('id')).first()
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='Error on password change')
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phone')
async def update_phone(user:user_dependency,db:db_dependency,user_request:UserPhone):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number=user_request.phone_number
    db.add(user_model)
    db.commit()