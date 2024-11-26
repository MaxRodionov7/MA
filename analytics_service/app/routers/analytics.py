from fastapi import APIRouter, Depends
from app.models.report import NotificationRequest, NotificationResponse
from app.repositories.analytics_repository import AnalyticsRepository
from typing import List

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics Management"]
)

def get_repo():
    from app.main import repo
    return repo


@router.post("/notify", summary="Send Notification")
def notify_analytics(data: NotificationRequest, repo: AnalyticsRepository = Depends(get_repo)):
    repo.save_notification(data.dict())
    return {"message": "Notification saved successfully"}


@router.get("/logs", response_model=List[NotificationResponse], summary="Get Notification Logs")
def get_logs(repo: AnalyticsRepository = Depends(get_repo)):
    return repo.get_notifications()
