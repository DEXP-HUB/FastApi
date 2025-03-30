from fastapi import Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from ..database import ConnectionDb, SelectUser
from ..authx import config, security, access_token_required


def auntification(login: str = Query(max_length=20), password: str = Query(max_length=20)) -> dict:
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = dict(SelectUser.by_login(db, login))
    
    if user_data == None or user_data['password'] != password:
        raise HTTPException(401, {'auntification': 'Incorrect password or login', 'status': 401})

    return {'uid': str(user_data['id']), 'role': user_data['status'], 'login': user_data['login']}


def create_tokens(user_data: dict = Depends(auntification)) -> dict:
    uid, role, login = user_data.values()

    refresh_token = security.create_refresh_token(uid=uid, data={'role': role, 'login': login})
    access_token = security.create_access_token(uid=uid, data={'role': role, 'login': login})

    return {'access_token': access_token, 'refresh_token': refresh_token}


def is_admin(payload: TokenPayload = Depends(access_token_required)):
    if payload.role == 'admin':
        db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
        users = SelectUser().all_users(db)
        json = jsonable_encoder(users)
        return json
    
    raise HTTPException(status_code=403, detail='Access Denied: Admin privileges required')