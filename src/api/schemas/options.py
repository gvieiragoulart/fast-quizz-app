from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class OptionBase(BaseModel):
    reference_id: int
    text: str
    order: int = 0
    is_correct: bool = False
    image_url: Optional[str] = None
    metadata: Optional[dict] = {}


class OptionAnswerResponse(BaseModel):
    id: UUID
    reference_id: int
    text: str
    order: int
    is_correct: bool

    class Config:
        from_attributes = True


__all__ = [
    "OptionBase",
    "OptionAnswerResponse",
]
