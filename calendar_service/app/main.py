from fastapi import FastAPI
from app.routers.calendar import router as calendar_router

app = FastAPI()

app.include_router(calendar_router)
