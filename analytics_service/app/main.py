import os
from fastapi import FastAPI
from app.routers.analytics import router as analytics_router
from app.repositories.analytics_repository import AnalyticsRepository

# Получение URL базы данных из переменных окружения
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Создание приложения FastAPI
app = FastAPI()

# Подключение роутера
app.include_router(analytics_router)
