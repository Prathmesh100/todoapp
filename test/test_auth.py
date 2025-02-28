from .utils import *
from routers.auth import authenticate_user,get_db,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from jose import jwt,JWTError
import pytest
from fastapi import HTTPException
main.app.dependency_overrides[get_db]=override_get_db
# main.app.dependency_overrides[get_current_user]=override_get_current_user


def test_authenticate_user(test_user):
    db=TestingSessionLocal()
    authenticated_user=authenticate_user(test_user.username,'user123',db)
    assert authenticated_user is not None
    assert authenticated_user.username==test_user.username

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode={'sub':'usertest','id':1,'role':'admin'}
    token=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {'username':'usertest','id':1,'user_role':'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode={"role":"user"}
    token= jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code==401
    assert excinfo.value.detail == 'Could not validate user.'