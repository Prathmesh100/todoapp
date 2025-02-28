from fastapi import APIRouter,Depends,HTTPException,Path,Request
from pydantic import Field,BaseModel
from typing import Optional,Annotated
from models import Users
from passlib.context import CryptContext
from database import sessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,datetime,timezone
from fastapi.templating import Jinja2Templates
# {
#   "email": "user@test.in",
#   "username": "usertest",
#   "first_name": "user",
#   "last_name": "test",
#   "password": "user123",
#   "role": "user"
# }

# {
#   "email": "user1@test.in",
#   "username": "usertest1",
#   "first_name": "user",
#   "last_name": "test",
#   "password": "user1231",
#   "role": "admin"
# }

# {
#   "email": "user2@test.in",
#   "username": "usertest12",
#   "first_name": "user",
#   "last_name": "test",
#   "password": "user12312",
#   "role": "admin"
# }

# {email: "example@gmail.com", username: "prathmesh100", first_name: "prathmesh", last_name: "chaurasia",…}
# email
# : 
# "example@gmail.com"
# first_name
# : 
# "prathmesh"
# last_name
# : 
# "chaurasia"
# password
# : 
# "om123456"
# phone_number
# : 
# "6232072365"
# role
# : 
# "admin"
# username
# : 
# "prathmesh100"

SECRET_KEY='c03518af4d417e3cfcd7a1e0497c205612f9723e28e8b08cdb88b9478b8c3cce'
ALGORITHM='HS256'

router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
templates=Jinja2Templates(directory='templates')

### Pages ###
@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html',{"request":request})

@router.get('/register-page')
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html',{"request":request})


### Endpoints ###

def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user


def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    encode={'sub':username,'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        user_role:str=payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=401,detail='could not validate user.')
        
        return {'username':username,'id':user_id,'user_role':user_role}
    except:
        raise HTTPException(status_code=401,detail='could not validate user.')


class CreateUserRequest(BaseModel):
    # id:Optional[int]=Field(gt=0)
    email:str=Field(min_length=3)
    username:str=Field(min_length=3)
    first_name:str=Field(min_length=3)
    last_name:str=Field(min_length=3)
    password:str=Field(min_length=3)
    role:str=Field(min_length=3)
    phone_number:str=Field(min_length=10, max_length=11)

class LoginRequest(BaseModel):
    email:str=Field(min_length=3)
    password:str=Field(min_length=3)


class Token(BaseModel):
    access_token:str
    token_type:str


@router.post('/')
async def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        isActive=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()
    return create_user_model


@router.post('/token',response_model=Token)
# async def get_token(db:db_dependency,user_data:LoginRequest):
#     user_model=db.query(Users).filter(Users.email==user_data.email).first()
#     if user_model is None:
#         return {'message':'User not found'},404
#     if bcrypt_context:
#         pass
#     pass



async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                db:db_dependency):
    
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401,detail='could not validate user.')
    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=20))

    return {'access_token':token ,'token_type':'bearer'}




