import os
from fastapi import FastAPI
from app.repositories.calendar_repository import CalendarRepository
from app.routers.calendar import router as calendar_router

database_url = os.getenv("DATABASE_URL")  # Uppercase for consistency
print(f"Main.py: DATABASE_URL is {database_url}", flush=True)
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

repo = CalendarRepository(database_url)

app = FastAPI()
app.include_router(calendar_router)
