from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    id: int
    date: datetime
    content: str