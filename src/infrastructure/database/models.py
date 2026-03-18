from sqlalchemy import JSON, Column, Integer, SmallInteger, String, Boolean, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from .connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    type = Column(String(50), default="adventure", nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    journeys = relationship("JourneyModel", back_populates="user", cascade="all, delete-orphan")


class JourneyModel(Base):
    __tablename__ = "journeys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    user = relationship("UserModel", back_populates="journeys")
    quizzes = relationship("QuizModel", back_populates="journey", cascade="all, delete-orphan")


class QuizModel(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    journey_id = Column(UUID(as_uuid=True), ForeignKey("journeys.id"), nullable=True)
    estimated_time = Column(SmallInteger, nullable=True)
    feedback_mode = Column(String(20), nullable=False, default="final")
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    journey = relationship("JourneyModel", back_populates="quizzes")
    questions = relationship("QuestionModel", back_populates="quiz", cascade="all, delete-orphan")


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    correct_answer = Column(SmallInteger, nullable=False) # referencia o reference_id of the correct option
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)


    options = relationship(
        "QuestionOptionModel",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="QuestionOptionModel.order",
    )
    quiz = relationship("QuizModel", back_populates="questions")

class QuestionOptionModel(Base):
    __tablename__ = "question_options"

    id = Column(UUID(as_uuid=True), primary_key=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    reference_id = Column(SmallInteger, nullable=True)
    text = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)
    is_correct = Column(Boolean, nullable=False, default=False)
    image_url = Column(String(1000), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    question = relationship("QuestionModel", back_populates="options")

class ResultsModel(Base):
    __tablename__ = "results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Allow null for anonymous users
    respondent_name = Column(String(200), nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    taken_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user = relationship("UserModel")
    quiz = relationship("QuizModel")

class AnswerResultModel(Base):
    __tablename__ = "answer_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    result_id = Column(UUID(as_uuid=True), ForeignKey("results.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(UUID(as_uuid=True), ForeignKey("question_options.id"), nullable=True)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    result = relationship("ResultsModel")
    question = relationship("QuestionModel")
    selected_option = relationship("QuestionOptionModel")