from fastapi import APIRouter, HTTPException
from app.repositories.analytics_repository import AnalyticsRepository
import os

# Получение URL базы данных из переменных окружения
database_url = os.getenv("DATABASE_URL")
repo = AnalyticsRepository(database_url)

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)


@router.get("/events/", summary="Get all logged events")
def get_all_events():
    try:
        return repo.get_all_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/count/", summary="Get the count of all events")
def get_event_count():
    try:
        return {"count": repo.get_event_count()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/user/{owner}", summary="Get events by owner")
def get_events_by_owner(owner: str):
    try:
        return repo.get_events_by_owner(owner)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/action/{action}", summary="Get events by action type")
def get_events_by_action(action: str):
    try:
        events = repo.get_events_by_action(action)
        return repo.get_events_by_action(action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
