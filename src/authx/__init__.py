from typing import Awaitable, Callable

from fastapi import Request
from authx import AuthX, AuthXConfig, RequestToken, TokenPayload

from psycopg2.extras import RealDictCursor


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]


security = AuthX(config=config)


# TokenGetter = Callable[[Request], Awaitable[RequestToken]]
# OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]


get_access_from_request = security.get_token_from_request(
    type = "access",
    optional = False
)


access_token_required = security.token_required(
    type = "access",
    verify_type = True,
    verify_fresh = False,
    verify_csrf = None
)


@security.set_subject_getter
def get_user_from_uid(uid: str) -> str:
    return uid
