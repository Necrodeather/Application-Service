from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .base import BaseEntity


class ApplicationCreate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)


class ApplicationRead(BaseEntity, ApplicationCreate):
    pass
