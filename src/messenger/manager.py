from datetime import datetime
from typing import List

from sqlalchemy import insert
from starlette.websockets import WebSocket

from database import async_session_maker
from messenger.models import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(Message).values(
                date=datetime.utcnow(),
                content=message,
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()