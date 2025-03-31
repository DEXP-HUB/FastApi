from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from psycopg2.extras import RealDictCursor

from ..authx import *
from ..database.postgre import ConnectionDb, SelectUser, DeleteUser, UpdateUser
from ..schemas.users import UserRegSchema
from ..api.dependencies import is_admin


router = APIRouter()


@router.get(
    path='/users', 
    description='Get all users',
)
def get_users(json: list = Depends(is_admin)):
    return JSONResponse(content={ind: el for ind, el in enumerate(json)})


@router.get(
    path='/user/{id}',
    description='Get user by id',
)
async def get_user(id):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user = SelectUser.by_id(db, id)
    json = jsonable_encoder(user)
    return JSONResponse(content=json)


@router.delete(
    path='/delete/{id}', 
    description='Delete user from database',
)
def delete_user(id: int):
    db = ConnectionDb().connect()
    DeleteUser.by_id(db, id)
    return JSONResponse(content={'status': 200})


@router.api_route(
    path='/update', 
    methods=['put', 'path'], 
    description='Update user to database',
)
def update_user(user: UserRegSchema):
    db = ConnectionDb().connect()
    UpdateUser.by_id(db, dict(user))
    return JSONResponse(content=jsonable_encoder(user))