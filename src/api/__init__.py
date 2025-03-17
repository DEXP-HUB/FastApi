from fastapi import APIRouter

from src.api.users import router as users_router
from src.api.admins import router as admins_router


main_router = APIRouter()
main_router.include_router(users_router)
main_router.include_router(admins_router)