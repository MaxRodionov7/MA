from fastapi import APIRouter, HTTPException
from app.repositories.calendar_repository import CalendarRepository
from app.models.calendar import CalendarCreateRequest, CalendarUpdateRequest, CalendarResponse
from typing import List
import os

router = APIRouter(
    prefix="/api/v1/calendar",
    tags=["Calendar Management"]
)

# URL базы данных календарей
calendar_db_url = os.getenv("CALENDAR_DATABASE_URL")
if not calendar_db_url:
    raise ValueError("CALENDAR_DATABASE_URL environment variable is not set")

# URL аналитической базы данных
analytics_db_url = os.getenv("ANALYTICS_DATABASE_URL")
if not analytics_db_url:
    raise ValueError("ANALYTICS_DATABASE_URL environment variable is not set")

# Создание репозитория
repo = CalendarRepository(calendar_db_url, analytics_db_url)

@router.post("/", response_model=CalendarResponse, summary="Create a new calendar")
def create_calendar(data: CalendarCreateRequest):
    try:
        calendar_id = repo.create_calendar(data.name, data.owner)
        repo.log_event("CREATE", calendar_id, data.name, data.owner)  # Вызов вложенной функции
        return CalendarResponse(id=calendar_id, name=data.name, owner=data.owner)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[CalendarResponse], summary="Get all calendars")
def get_all_calendars():
    return repo.get_all_calendars()


@router.put("/{calendar_id}", summary="Update an existing calendar")
def update_calendar(calendar_id: int, data: CalendarUpdateRequest):
    try:
        repo.update_calendar(calendar_id, data.name, data.owner)
        repo.log_event("UPDATE", calendar_id, data.name, data.owner)  # Вложенная функция
        return {"message": f"Calendar with ID {calendar_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{calendar_id}", summary="Delete a calendar")
def delete_calendar(calendar_id: int):
    try:
        repo.delete_calendar(calendar_id)
        repo.log_event("DELETE", calendar_id, None, None)  # Вложенная функция
        return {"message": f"Calendar with ID {calendar_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
