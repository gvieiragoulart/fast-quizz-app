from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Journey Schemas
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

    class Config:
        from_attributes = True




# Question Schemas
class QuestionBase(BaseModel):
    text: str
    options: List[str] = Field(..., min_items=2, max_items=6)
    correct_answer: str


class QuestionCreate(QuestionBase):
    quiz_id: UUID


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    options: Optional[List[str]] = Field(None, min_items=2, max_items=6)
    correct_answer: Optional[str] = None
    quiz_id: Optional[UUID] = None


class QuestionResponse(BaseModel):
    id: UUID
    text: str
    quiz_id: UUID
    options: List[str]
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


# Quiz Schemas

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

    class Config:
        from_attributes = True