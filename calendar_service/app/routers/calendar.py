from fastapi import APIRouter, HTTPException
import requests
from app.repositories.calendar_repository import CalendarRepository

router = APIRouter(
    prefix="/api/v1/calendar",
    tags=["calendar"]
)

repo = CalendarRepository()

@router.post("/")
def create_calendar(name: str, owner: str):
    try:
        calendar_id = repo.create_calendar(name, owner)
        action = "create"
        details = f"Calendar '{name}' created by {owner}"

        # Уведомление аналитического сервиса
        url = "http://analytics_service:8000/api/v1/analytics/notify"
        response = requests.post(url, json={"calendar_id": calendar_id, "action": action, "details": details})
        response.raise_for_status()

        return {"calendar_id": calendar_id, "message": "Calendar created and analytics notified successfully"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to notify analytics service: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/")
def get_calendars():
    try:
        return repo.get_all_calendars()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.delete("/{calendar_id}")
def delete_calendar(calendar_id: int):
    try:
        repo.delete_calendar(calendar_id)
        return {"message": f"Calendar with id {calendar_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
