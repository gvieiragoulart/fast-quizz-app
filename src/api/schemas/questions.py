from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from .options import OptionBase, OptionAnswerResponse


class QuestionBase(BaseModel):
    text: str
    options: List[OptionBase] = Field(..., min_items=2, max_items=6)
    correct_answer: int


class QuestionCreate(QuestionBase):
    quiz_id: UUID


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    options: Optional[List[OptionBase]] = Field(None, min_items=2, max_items=6)
    correct_answer: Optional[str] = None
    quiz_id: Optional[UUID] = None


class QuestionResponse(BaseModel):
    id: UUID
    text: str
    quiz_id: UUID
    options: List[OptionAnswerResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuestionResponseWithAnswer(QuestionResponse):
    correct_answer: str


# Answer Checking
class AnswerCheck(BaseModel):
    answer: str


class AnswerResult(BaseModel):
    is_correct: bool
    correct_answer: Optional[str] = None


__all__ = [
    "QuestionBase",
    "QuestionCreate",
    "QuestionUpdate",
    "QuestionResponse",
    "QuestionResponseWithAnswer",
    "AnswerCheck",
    "AnswerResult",
]
