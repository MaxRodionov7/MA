from fastapi import APIRouter, HTTPException, Depends
from app.repositories.calendar_repository import CalendarRepository
from app.models.calendar import CalendarCreateRequest, CalendarResponse
from typing import List
import requests

router = APIRouter(
    prefix="/api/v1/calendar",
    tags=["Calendar Management"]
)


def get_repo():
    from app.main import repo
    return repo


@router.post("/", response_model=CalendarResponse, summary="Create Calendar")
def create_calendar(data: CalendarCreateRequest, repo: CalendarRepository = Depends(get_repo)):
    try:
        calendar_id = repo.create_calendar(data.name, data.owner)

        # Вызов аналитического сервиса
        analytics_url = "http://analytics_service:8002/api/v1/analytics/notify"
        payload = {
            "calendar_id": calendar_id,
            "action": "create",
            "details": f"Calendar '{data.name}' created by {data.owner}",
            "owner": data.owner,
            "name": data.name
        }
        requests.post(analytics_url, json=payload)

        return CalendarResponse(id=calendar_id, name=data.name, owner=data.owner)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[CalendarResponse], summary="Get All Calendars")
def get_all_calendars(repo: CalendarRepository = Depends(get_repo)):
    return repo.get_all_calendars()


@router.delete("/{calendar_id}", summary="Delete Calendar")
def delete_calendar(calendar_id: int, repo: CalendarRepository = Depends(get_repo)):
    try:
        repo.delete_calendar(calendar_id)
        return {"message": f"Calendar with ID {calendar_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
