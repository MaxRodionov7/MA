
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class Calendar(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    shared: bool = False
    owner: str  # Owner's user ID
