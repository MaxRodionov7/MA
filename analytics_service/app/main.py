from fastapi import FastAPI
from app.routers.analytics import router as analytics_router

app = FastAPI()

app.include_router(analytics_router)
