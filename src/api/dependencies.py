from fastapi import Depends, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from ..database.postgre import ConnectionDb, SelectUser
from ..authx import security, access_token_required


def create_tokens(uid: str, role: str, login: str) -> dict:
    refresh_token = security.create_refresh_token(uid=uid, data={'role': role, 'login': login})
    access_token = security.create_access_token(uid=uid, data={'role': role, 'login': login})
    
    return {'access_token': access_token, 'refresh_token': refresh_token}

        
def auntification(login: str = Query(max_length=20), password: str = Query(max_length=20)) -> dict:
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = dict(SelectUser.by_login(db, login))
    
    if user_data == None or user_data['password'] != password:
        raise HTTPException(401, {'auntification': 'Incorrect password or login', 'status': 401})
    
    tokens = create_tokens(str(user_data['id']), user_data['status'], user_data['login'])
    return tokens


def is_admin(payload: TokenPayload = Depends(access_token_required)):
    if payload.role == 'admin':
        return True
    
    else:
        raise HTTPException(status_code=403, detail='Access Denied: Admin privileges required')