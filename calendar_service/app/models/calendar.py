from pydantic import BaseModel


class CalendarCreateRequest(BaseModel):
    name: str
    owner: str


class CalendarResponse(BaseModel):
    id: int
    name: str
    owner: str
