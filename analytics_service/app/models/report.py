from pydantic import BaseModel


class NotificationRequest(BaseModel):
    calendar_id: int
    action: str
    details: str
    owner: str
    name: str


class NotificationResponse(BaseModel):
    id: int
    calendar_id: int
    action: str
    details: str
    owner: str
    name: str
