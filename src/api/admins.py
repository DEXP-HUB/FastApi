from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from authx import TokenPayload

from psycopg2.extras import RealDictCursor

from ..authx import *
from ..database.postgre import ConnectionDb, SelectUser, DeleteUser, UpdateUser
from ..schemas.users import UserUpdateSchema
from ..api.dependencies import is_admin, set_param_put


router = APIRouter(tags=['Admins API'])


@router.get(
    path='/users', 
    description='Get all users',
    dependencies=[Depends(is_admin)],
)
def get_users():
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
    users = SelectUser().all_users(db)
    json = jsonable_encoder(users)
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
    path='/delete', 
    description='Delete user from database',
    dependencies=[Depends(is_admin)],
)
def delete_user(id: int, token: TokenPayload = Depends(access_token_required)):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    uid = dict(SelectUser().by_id(db, id))
    
    if int(token.sub) == uid['id']:
        raise HTTPException(status_code=403, detail="You can't delete yourself")

    db = ConnectionDb().connect()
    DeleteUser.by_id(db, id)
    return Response(status_code=204)


@router.patch(
    path='/update-user', 
    description='Update user to database',
    dependencies=[Depends(is_admin)],
)
def update_user(user: UserUpdateSchema):
    db = ConnectionDb().connect()
    UpdateUser.by_id(db, dict(user))
    return JSONResponse(status_code=201, content=jsonable_encoder(user))


@router.put(
    path='/new-param',
    description='Set new param for user to database',
    dependencies=[Depends(is_admin)],
)
def new_param(data: dict = Depends(set_param_put)):
    db = ConnectionDb().connect()
    UpdateUser.by_id(db, data)
    return JSONResponse(
        status_code=201, 
        content={'status': 201, 'message': 'Updated user'}
        )