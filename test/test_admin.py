from .utils import *
from routers.admin import get_current_user,get_db

main.app.dependency_overrides[get_db]=override_get_db
main.app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response=client.get('/admin/todo')
    assert response.status_code==200
    assert response.json()==[{"title":"learn to code",
        "description":'Need to learn everyday',
        "priority":3,
        "complete":False,
        "owner_id":1,
        'id':1}]
