from typing import List

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from database import get_async_session
from messenger.manager import ConnectionManager

from messenger.models import Message
from messenger.schemas import MessageCreate

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

templates = Jinja2Templates(directory="templates")
@router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.get("/")
async def get_messages(session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(Message))
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
    stmt = insert(Message).values(**new_message.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
):
    query = select(message).order_by(message.id.desc()).limit(5)
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/chat/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} connect the chat", add_to_db=False)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
