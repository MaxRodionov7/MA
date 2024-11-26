import os
from fastapi import FastAPI
from app.routers.calendar import router as calendar_router
from app.repositories.calendar_repository import CalendarRepository

# URL базы данных календарей
calendar_db_url = os.getenv("CALENDAR_DATABASE_URL")
if not calendar_db_url:
    raise ValueError("CALENDAR_DATABASE_URL environment variable is not set")

# URL аналитической базы данных
analytics_db_url = os.getenv("ANALYTICS_DATABASE_URL")
if not analytics_db_url:
    raise ValueError("ANALYTICS_DATABASE_URL environment variable is not set")

# Создание репозитория с двумя базами данных
repo = CalendarRepository(calendar_db_url, analytics_db_url)

# Создание приложения FastAPI
app = FastAPI()
app.include_router(calendar_router)
