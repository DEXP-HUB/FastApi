from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from psycopg2.extras import RealDictCursor

from ..authx import security
from ..database import ConnectionDb, SelectUser, DeleteUser, UpdateUser
from ..schemas.users import UserRegSchema


router = APIRouter()


@router.get(
    path='/users', 
    description='Get all users',
    dependencies=[Depends(security.access_token_required)]
    )
def get_users():
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
    users = SelectUser().all_users(db)
    json = jsonable_encoder(users)
    response = JSONResponse(content={ind: el for ind, el in enumerate(json)})
    return response


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