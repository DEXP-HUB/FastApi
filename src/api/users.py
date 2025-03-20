from typing import Annotated
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from psycopg2.extras import RealDictCursor

from .dependencies import auntification
from ..schemas.users import UserRegSchema
from ..database import ConnectionDb, SelectUser, InsertUser
from ..authx import *


router = APIRouter(prefix='/user', tags=['User router'])


@router.get(
    path='/profile',
    description='Returns information about the logged in user.',
)
def user_profile(uid: str = Depends(security.get_current_subject)):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    profile = dict(SelectUser.by_id(db, uid))
    json = jsonable_encoder(profile)
    response = JSONResponse(json, 200)
    return response    


@router.post(
    path='/login',
    description='Authentication user',
)
def login(user_data: dict = Depends(auntification)):
    uid, role, login = user_data
    token = security.create_access_token(uid=uid, data={'role': role, 'login': login})
    response = JSONResponse(
        content={'token': token, 'status': 200, 'result': 'Password True'}, 
        status_code=200
    )
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return response


@router.post(
    path='/registration', 
    description='Create new profile to db'
)
def registration(user: UserRegSchema):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, dict(user))
    return JSONResponse(
        status_code=200, 
        content={'info': 'Create new profile to db', 'status': 200}
    )


@router.get('/token')
def get_token(token: TokenPayload = Depends(access_token_required)):
    return token