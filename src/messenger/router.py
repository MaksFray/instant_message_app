from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from messenger.models import message
from messenger.schemas import MessageCreate

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.get("/")
async def get_messages(session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(message))
    results = query.all()
    if results:
        messages = []
        for r in results:
            messages.append({
                "date": r.date,
                "id": r.id,
                "content": r.content,
            }
            )
        return {"data": messages, "status_code": 200}


@router.post("/")
async def add_message(new_message: MessageCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(message).values(**new_message.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}