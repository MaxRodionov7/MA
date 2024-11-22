from fastapi import APIRouter
from pydantic import BaseModel
from app.repositories.analytics_repository import AnalyticsRepository

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["analytics"]
)

repo = AnalyticsRepository()

class AnalyticsNotification(BaseModel):
    calendar_id: int
    action: str
    details: str

@router.post("/notify")
def notify_analytics(notification: AnalyticsNotification):
    repo.process_notification(notification.dict())
    return {"message": "Notification received", "data": notification}


@router.get("/logs")
def get_logs():
    return repo.get_notifications()


@router.delete("/logs")
def clear_logs():
    repo.clear_notifications()
    return {"message": "All logs cleared"}
