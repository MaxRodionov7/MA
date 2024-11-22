
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Report(BaseModel):
    id: UUID
    event_name: str
    created_at: datetime
    metrics: dict
    survey_results: dict
    generated_by: str
