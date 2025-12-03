from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.question import Question
from ...domain.repositories.question_repository import QuestionRepository
from ..database.models import QuestionModel


class QuestionRepositoryImpl(QuestionRepository):
    """SQLAlchemy implementation of QuestionRepository."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: QuestionModel) -> Question:
        """Convert database model to domain entity."""
        return Question(
            id=model.id,
            text=model.text,
            quiz_id=model.quiz_id,
            options=model.options,
            correct_answer=model.correct_answer,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Question) -> QuestionModel:
        """Convert domain entity to database model."""
        return QuestionModel(
            id=entity.id,
            text=entity.text,
            quiz_id=entity.quiz_id,
            options=entity.options,
            correct_answer=entity.correct_answer,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, question: Question) -> Question:
        """Create a new question."""
        db_question = self._to_model(question)
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return self._to_entity(db_question)

    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        """Get a question by ID."""
        db_question = self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        return self._to_entity(db_question) if db_question else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions with pagination."""
        db_questions = self.db.query(QuestionModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_question) for db_question in db_questions]

    async def get_by_quiz_id(self, quiz_id: UUID, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions for a specific quiz."""
        db_questions = (
            self.db.query(QuestionModel)
            .filter(QuestionModel.quiz_id == quiz_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(db_question) for db_question in db_questions]

    async def update(self, question: Question) -> Question:
        """Update a question."""
        db_question = self.db.query(QuestionModel).filter(QuestionModel.id == question.id).first()
        if db_question:
            db_question.text = question.text
            db_question.quiz_id = question.quiz_id
            db_question.options = question.options
            db_question.correct_answer = question.correct_answer
            db_question.updated_at = question.updated_at
            self.db.commit()
            self.db.refresh(db_question)
            return self._to_entity(db_question)
        raise ValueError(f"Question with ID '{question.id}' not found")

    async def delete(self, question_id: UUID) -> bool:
        """Delete a question."""
        db_question = self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        if db_question:
            self.db.delete(db_question)
            self.db.commit()
            return True
        return False
