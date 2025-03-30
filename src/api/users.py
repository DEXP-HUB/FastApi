from typing import Annotated

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from .dependencies import create_tokens
from ..schemas.users import UserRegSchema
from ..database import ConnectionDb, SelectUser, InsertUser
from ..authx import config, security, access_token_required


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
def login(tokens: dict = Depends(create_tokens)):
    response = JSONResponse(
        content={
            'access_token': tokens['access_token'], 'refresh_token': tokens['refresh_token'], 
            'status': 200, 'result': 'Password True'
            }, 
        status_code=200
    )
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, tokens['access_token'])
    response.set_cookie(config.JWT_REFRESH_COOKIE_NAME, tokens['refresh_token'])
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


@router.get('/access_token')
def get_token(access_token: TokenPayload = Depends(access_token_required)):
    return access_token