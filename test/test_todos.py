from database import Base
import main
from routers.todos import get_current_user,get_db
from fastapi.testclient import TestClient
from fastapi import status
from models import Todos
from .utils import override_get_current_user,override_get_db,client,TestingSessionLocal,test_todo

main.app.dependency_overrides[get_db]=override_get_db
main.app.dependency_overrides[get_current_user]=override_get_current_user

def test_read_all_authenticated(test_todo):
    response=client.get('/todo')
    print(response.json())
    assert response.status_code== status.HTTP_200_OK
    assert response.json()==[{"title":"learn to code",
        "description":'Need to learn everyday',
        "priority":3,
        "complete":False,
        "owner_id":1,
        'id':1}]


def test_read_one_authenticated(test_todo):
    response=client.get('/todo/1')
    print(response.json())
    assert response.status_code== status.HTTP_200_OK
    assert response.json()=={"title":"learn to code",
        "description":'Need to learn everyday',
        "priority":3,
        "complete":False,
        "owner_id":1,
        'id':1}


def test_read_one_authenticated_not_found(test_todo):
    response=client.get('/todo/3')
    print(response.json())
    assert response.status_code== 404
    assert response.json()=={"detail":"Todo not found"}


def test_create_todo(test_todo):
    request_data={
        "title": "string",
        "description": "string",
        "priority": 1,
        "complete": False
        }
    response=client.post('/todo/',json=request_data)
    assert response.status_code==201
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    assert model.priority==request_data.get('priority')
    assert model.complete==request_data.get('complete')


def test_update_todo(test_todo):
    request_data = {
        "title": "updated title",
        "description": "updated description",
        "priority": 2,
        "complete": True
    }
    response = client.put('/todo/1', json=request_data)
    assert response.status_code == 200
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo_not_found():
    request_data = {
        "title": "updated title",
        "description": "updated description",
        "priority": 2,
        "complete": True
    }
    response = client.put('/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete('/todo/999')
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

