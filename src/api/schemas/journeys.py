from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class JourneyBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str


class JourneyCreate(JourneyBase):
    pass


class JourneyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None


class JourneyResponse(JourneyBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


__all__ = [
    "JourneyBase",
    "JourneyCreate",
    "JourneyUpdate",
    "JourneyResponse",
]
