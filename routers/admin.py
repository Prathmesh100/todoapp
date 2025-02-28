from fastapi import APIRouter,Depends,HTTPException,Path
from models import Todos
from database import engine,sessionLocal
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .auth import get_current_user

router=APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get('/todo')
async def read_all(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    res= db.query(Todos).all()
    # print(res)
    return res