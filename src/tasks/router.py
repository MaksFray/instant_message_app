from fastapi import APIRouter, Depends

from auth.base_config import current_user
from tasks.tasks import send_unread_message_report

router = APIRouter(
    prefix="/report",
    tags=['tasks'],
)

@router.get("/report")
def get_unread_messages(user=Depends(current_user)):
    send_unread_message_report.delay(user.username)
    return {
        "status": 200,
        "data": "Message were sent",
        "details": None,
    }