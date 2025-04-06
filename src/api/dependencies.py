from typing import Literal

from pydantic import EmailStr

from fastapi import Depends, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from ..database.postgre import ConnectionDb, SelectUser
from ..authx import security, access_token_required, get_access_from_request


def create_tokens(uid: str, role: str, login: str) -> dict:
    refresh_token = security.create_refresh_token(uid=uid, data={'role': role, 'login': login})
    access_token = security.create_access_token(uid=uid, data={'role': role, 'login': login})
    
    return {'access_token': access_token, 'refresh_token': refresh_token}


def auntification(
        request: Request, 
        login: str = Query(max_length=20), 
        password: str = Query(max_length=20)
    ) -> dict:
    if request.cookies.get('access_token'):
        raise HTTPException(409, 'User is already authenticated')
    
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = dict(SelectUser.by_login(db, login))
    
    if user_data == None or user_data['password'] != password:
        raise HTTPException(401, {'auntification': 'Incorrect password or login', 'status': 401})
    
    tokens = create_tokens(str(user_data['id']), user_data['status'], user_data['login'])

    return tokens


def is_admin(payload: TokenPayload = Depends(access_token_required)):
    if payload.role == 'admin':
        return True
    
    raise HTTPException(status_code=403, detail='Access Denied: Admin privileges required')


def set_param_put(
    user_id: int = Query(ge=0),
    login: str = Query(max_length=20, default=None),
    password: str = Query(max_length=20, default=None),
    first_name: str = Query(max_length=15, default=None),
    last_name: str = Query(max_length=15, default=None),
    city: str = Query(max_length=20, default=None),
    address: str = Query(max_length=50, default=None),
    age: int = Query(ge=0, le=115, default=None),
    floor: int = Query(ge=0, le=163, default=None),
    apartament_number: int = Query(ge=0, default=None),
    data_registratsii: Literal['NOW()'] = Query(default=None),
    status: Literal['user', 'admin'] = Query(default=None),
    email: EmailStr = Query(default=None),
):
    return locals()