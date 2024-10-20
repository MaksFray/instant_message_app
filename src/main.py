from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from pydantic import BaseModel

from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_users import FastAPIUsers, fastapi_users

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate

from messenger.router import router as router_messenger
from tasks.router import router as router_tasks

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


app.include_router(router_messenger)
app.include_router(router_tasks)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"