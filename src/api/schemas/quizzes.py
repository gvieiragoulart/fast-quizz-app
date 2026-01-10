from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from .questions import QuestionBase, QuestionResponse


class QuizzQuestionCreate(QuestionBase):
    question_id: Optional[UUID] = None


class QuizBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    questions: Optional[List[QuestionBase]] = []


class QuizCreate(QuizBase):
    journey_id: Optional[UUID] = Field(
        None, description="ID of the journey this quiz belongs to"
    )


class QuizUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    journey_id: Optional[UUID] = None


class QuizResponse(QuizBase):
    id: UUID
    journey_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    questions: Optional[List[QuestionResponse]] = []

    class ConfigDict:
        from_attributes = True


# List response for latest quizzes with pagination metadata
class QuizzesListResponse(BaseModel):
    items: List[QuizResponse]
    total_items: int
    total_pages: int

    class ConfigDict:
        from_attributes = True


__all__ = [
    "QuizzQuestionCreate",
    "QuizBase",
    "QuizCreate",
    "QuizUpdate",
    "QuizResponse",
    "QuizzesListResponse",
]
