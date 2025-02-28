from fastapi import APIRouter,Depends,HTTPException,Path,Request
from models import Todos
from database import engine,sessionLocal
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .auth import get_current_user
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

templates=Jinja2Templates(directory='templates')
router=APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    # id:Optional[int]=Field(gt=0)
    title:str = Field(min_length=3)
    description:str=Field(min_length=3,max_length=100)
    priority:int=Field(gt=0)
    complete:bool

def redirect_to_login():
    redirect_response=RedirectResponse(url='/auth/login-page',status_code=302)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

### pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if not user:
            print('User not authenticated — redirecting to login.')
            return redirect_to_login()
        
        print('Fetching todos for user:', user.get('id'))
        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
        print('Todos fetched successfully.')

        return templates.TemplateResponse('todo.html', {
            "request": request,
            "todos": todos,
            "user": user
        })

    except Exception as e:
        print(f'Exception occurred: {e}')
        return redirect_to_login()

@router.get('/add-todo-page')
async def render_todo_page(request:Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if not user:
            print('User not authenticated — redirecting to login.')
            return redirect_to_login()
        

        return templates.TemplateResponse('add-todo.html', {
            "request": request,
            "user": user
        })

    except Exception as e:
        print(f'Exception occurred: {e}')
        return redirect_to_login()

@router.get('/edit-todo-page/{todoid}')
async def render_todo_page(request:Request,db:db_dependency,todoid:int):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if not user:
            print('User not authenticated — redirecting to login.')
            return redirect_to_login()
        
        todo=db.query(Todos).filter(Todos.id==todoid).filter(Todos.owner_id==user.get('id')).first()
        return templates.TemplateResponse('edit-todo.html', {
            "request": request,
            "user": user,
            "todo":todo
        })

    except Exception as e:
        print(f'Exception occurred: {e}')
        return redirect_to_login()

### endpoints ###

@router.get('/')
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    res= db.query(Todos).filter(Todos.owner_id==user.get('id')).all()
    # print(res)
    return res

@router.get("/{todo_id}")
async def read_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model= db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Todo not found")




@router.post("/",status_code=201)
async def add_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    print(user)
    todo_model=Todos(**todo_request.model_dump(),
                    owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    



@router.put("/{todo_id}")
async def update_todo(user:user_dependency,db:db_dependency,todo_id:int,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is  None:
        raise HTTPException(status_code=404,detail="Todo not found")
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/{todo_id}",status_code=204)
async def update_todo(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is  None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()

    