from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from .questions import QuestionBase, QuestionResponse
from ...domain.entities.quiz import FeedbackMode, Difficulty


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
    estimated_time: Optional[int] = Field(
        None, ge=1, description="Estimated time in minutes to complete the quiz"
    )
    feedback_mode: FeedbackMode = Field(
        FeedbackMode.FINAL, description="Feedback mode: 'final' or 'imediato'"
    )
    difficulty: Difficulty = Field(
        None, description="Difficulty level: 'facil', 'medio', 'dificil', 'expert'"
    )
    image_url: Optional[str] = None


class QuizUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    journey_id: Optional[UUID] = None
    estimated_time: Optional[int] = Field(None, ge=1)
    feedback_mode: Optional[FeedbackMode] = None
    difficulty: Optional[Difficulty] = None
    image_url: Optional[str] = None


class QuizResponse(QuizBase):
    id: UUID
    journey_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    estimated_time: Optional[int] = None
    feedback_mode: FeedbackMode = FeedbackMode.FINAL
    difficulty: Difficulty = Difficulty.EASY
    image_url: Optional[str] = None
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
