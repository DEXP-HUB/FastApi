from authx import AuthX

from psycopg2.extras import RealDictCursor

from .config import config_authx


security = AuthX(config=config_authx)


get_access_from_request = security.get_token_from_request(
    type = "access",
    optional = False
)


access_token_required = security.token_required(
    type = "access",
    verify_type = True,
    verify_fresh = False,
    verify_csrf = True
)


@security.set_subject_getter
def get_user_from_uid(uid: str) -> str:
    return uid
