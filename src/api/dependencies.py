from fastapi import HTTPException

from psycopg2.extras import RealDictCursor

from src.database import ConnectionDb, SelectUser

from src.schemas.users import UserLoginSchema



def auntification(login: str = UserLoginSchema, password: str = UserLoginSchema):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = SelectUser.by_login(db, login)

    if user_data == None or user_data['password'] != password:
        raise HTTPException(401, {'auntification': 'Incorrect password or login', 'status': 401})

    return login