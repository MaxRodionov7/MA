from pydantic import BaseModel


class ReportRequest(BaseModel):
    event_name: str
    owner: str


class ReportResponse(BaseModel):
    id: int
    event_name: str
    owner: str
