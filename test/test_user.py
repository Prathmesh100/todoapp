from .utils import *
from routers.user import get_current_user,get_db

main.app.dependency_overrides[get_db]=override_get_db
main.app.dependency_overrides[get_current_user]=override_get_current_user


def test_return_user(test_user):
    response=client.get('/user')
    # print(response.json())
    assert response.status_code==200
    # assert response.json()=={'last_name': 'test', 'email': 'user@test.in', 'username': 'usertest', 'isActive': True, 'phone_number': '9999999999', 'id': 1, 'first_name': 'user', 'hashed_password': '$2b$12$rDcHsFK4k8FBnLbu3c.dXea5vLUVEqV0xDTMd949J8uo92CeR833W', 'role': 'admin'}
    response_data = response.json()

    assert response.json()['last_name'] == 'test'
    assert response.json()['email'] == 'user@test.in'
    assert response.json()['username'] == 'usertest'
    assert response.json()['isActive'] is True
    assert response.json()['phone_number'] == '9999999999'
    assert response.json()['id'] == 1
    assert response.json()['first_name'] == 'user'
    assert response.json()['role'] == 'admin'