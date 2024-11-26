import os
from fastapi import FastAPI
from app.repositories.analytics_repository import AnalyticsRepository
from app.routers.analytics import router as analytics_router

database_url = os.getenv("DATABASE_URL")  # Uppercase for consistency
print(f"Main.py: DATABASE_URL is {database_url}", flush=True)
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

repo = AnalyticsRepository(database_url)

app = FastAPI()
app.include_router(analytics_router)
