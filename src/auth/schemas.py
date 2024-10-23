from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    #username: str
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int = 1
