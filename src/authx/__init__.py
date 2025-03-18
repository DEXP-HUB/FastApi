from authx import AuthX, AuthXConfig, RequestToken

from psycopg2.extras import RealDictCursor

from ..database import ConnectionDb, SelectUser
from ..schemas.users import UserJwtSchema


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]


security = AuthX(config=config, model=UserJwtSchema)


@security.set_subject_getter
def get_user_from_uid(uid: str) -> UserJwtSchema:
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    profile = dict(SelectUser.by_login(db, uid))
    return UserJwtSchema(**profile)
