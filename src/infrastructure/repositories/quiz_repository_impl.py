from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.quiz import Quiz
from ...domain.repositories.quiz_repository import QuizRepository
from ..database.models import QuizModel


class QuizRepositoryImpl(QuizRepository):
    """SQLAlchemy implementation of QuizRepository."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: QuizModel) -> Quiz:
        """Convert database model to domain entity."""
        return Quiz(
            id=model.id,
            title=model.title,
            description=model.description,
            journey_id=model.journey_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Quiz) -> QuizModel:
        """Convert domain entity to database model."""
        return QuizModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            journey_id=entity.journey_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, quiz: Quiz) -> Quiz:
        """Create a new quiz."""
        db_quiz = self._to_model(quiz)
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        return self._to_entity(db_quiz)

    async def get_by_id(self, quiz_id: UUID) -> Optional[Quiz]:
        """Get a quiz by ID."""
        db_quiz = self.db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
        return self._to_entity(db_quiz) if db_quiz else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes with pagination."""
        db_quizzes = self.db.query(QuizModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_quiz) for db_quiz in db_quizzes]

    async def get_by_journey_id(self, journey_id: UUID, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes for a specific journey."""
        db_quizzes = (
            self.db.query(QuizModel)
            .filter(QuizModel.journey_id == journey_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(db_quiz) for db_quiz in db_quizzes]

    async def update(self, quiz: Quiz) -> Quiz:
        """Update a quiz."""
        db_quiz = self.db.query(QuizModel).filter(QuizModel.id == quiz.id).first()
        if db_quiz:
            db_quiz.title = quiz.title
            db_quiz.description = quiz.description
            db_quiz.journey_id = quiz.journey_id
            db_quiz.updated_at = quiz.updated_at
            self.db.commit()
            self.db.refresh(db_quiz)
            return self._to_entity(db_quiz)
        raise ValueError(f"Quiz with ID '{quiz.id}' not found")

    async def delete(self, quiz_id: UUID) -> bool:
        """Delete a quiz."""
        db_quiz = self.db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
        if db_quiz:
            self.db.delete(db_quiz)
            self.db.commit()
            return True
        return False
