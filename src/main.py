from fastapi import FastAPI

from .authx import security
from .api import main_router


app = FastAPI()
app.include_router(main_router)

security.handle_errors(app)

