from typing import Annotated

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, Response

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from ..services.mail import send_message
from .dependencies import auntification
from ..schemas.users import UserRegSchema
from ..database.postgre import ConnectionDb, SelectUser, InsertUser
from ..authx import config_authx, security, access_token_required, get_access_from_request


router = APIRouter(prefix='/user', tags=['User API'])


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


@router.get('/access-token')
def get_token(access_token: TokenPayload = Depends(access_token_required)):
    return access_token


@router.post(
    path='/login',
    description='Authentication user',
)
def login(user_data: dict = Depends(auntification)):
    response = JSONResponse(
            content={
                'access_token': user_data['access_token'], 
                'refresh_token': user_data['refresh_token'], 
                'status': 200, 'result': 'Password True',
                }, 
            status_code=200
        )

    response.set_cookie(config_authx.JWT_ACCESS_COOKIE_NAME, user_data['access_token'])
    response.set_cookie(config_authx.JWT_REFRESH_COOKIE_NAME, user_data['refresh_token'])

    return response
    

@router.post(
    path='/registration', 
    description='Create new profile to db',
)
def registration(user: UserRegSchema, bg_task: BackgroundTasks):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, dict(user))

    return JSONResponse(
        status_code=201, 
        content={'info': 'Create new profile to db', 'status': 201},
        background=bg_task.add_task(send_message, user.email),
    )


@router.post(
    path='/logout',
    description='Out from profile',
    dependencies=[Depends(get_access_from_request)],   
)
def logout():
    response = Response(status_code=204)
    response.delete_cookie(key=config_authx.JWT_ACCESS_COOKIE_NAME)
    response.delete_cookie(key=config_authx.JWT_REFRESH_COOKIE_NAME)

    return response




