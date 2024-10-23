from fastapi import APIRouter

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserUpdate
from fastapi_users import FastAPIUsers


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#/me
#/{id}
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)