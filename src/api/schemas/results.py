from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class ResultCreate(BaseModel):
    user_id: Optional[UUID] = None
    respondent_name: str = Field(..., min_length=1, max_length=200)
    quiz_id: UUID
    score: int = Field(..., ge=0, le=100)
    total_questions: int = Field(..., gt=0)


class ResultResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    respondent_name: str
    quiz_id: UUID
    score: int
    total_questions: int
    taken_at: datetime

    class ConfigDict:
        from_attributes = True


class ResultsListResponse(BaseModel):
    items: List[ResultResponse]
    total: int


__all__ = [
    "ResultCreate",
    "ResultResponse",
    "ResultsListResponse",
]
