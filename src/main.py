from typing import Awaitable, Callable
from authx import AuthX, RequestToken
from .authx import security

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from .api import main_router


app = FastAPI()
app.include_router(main_router)

security.handle_errors(app)

