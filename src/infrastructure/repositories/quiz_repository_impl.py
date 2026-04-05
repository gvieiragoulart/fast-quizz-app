from typing import Optional, List, Annotated
from fastapi import Depends
from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from src.infrastructure.database.connection import get_db

from ...domain.entities.quiz import Quiz, FeedbackMode, Difficulty
from ...domain.repositories.quiz_repository import QuizRepository
from ..database.models import QuizModel


class QuizRepositoryImpl(QuizRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: QuizModel, include_questions: bool = False) -> Quiz:
        quizz = Quiz(
            id=model.id,
            title=model.title,
            description=model.description,
            journey_id=model.journey_id,
            user_id=model.user_id,
            estimated_time=model.estimated_time,
            feedback_mode=FeedbackMode(model.feedback_mode) if model.feedback_mode else FeedbackMode.FINAL,
            difficulty=Difficulty(model.difficulty) if model.difficulty else None,
            image_url=model.image_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        if include_questions:
            from .question_repository_impl import QuestionRepositoryImpl

            question_repo = QuestionRepositoryImpl(self.db)
            questions = [
                question_repo._to_entity(q_model) for q_model in model.questions
            ]
            quizz.questions = questions  # type: ignore
        return quizz

    def _to_model(self, entity: Quiz) -> QuizModel:
        return QuizModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            journey_id=entity.journey_id,
            user_id=entity.user_id,
            estimated_time=entity.estimated_time,
            feedback_mode=entity.feedback_mode.value if entity.feedback_mode else "final",
            difficulty=entity.difficulty.value if entity.difficulty else None,
            image_url=entity.image_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, quiz: Quiz) -> Quiz:
        db_quiz = self._to_model(quiz)
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        return self._to_entity(db_quiz)

    async def get_by_id(self, quiz_id: UUID, include_questions: bool = False) -> Optional[Quiz]:
        query = self.db.query(QuizModel).filter(QuizModel.id == quiz_id)
        if include_questions:
            query = query.options(joinedload(QuizModel.questions))
        db_quiz = query.first()
        return self._to_entity(db_quiz, include_questions=include_questions) if db_quiz else None


    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        db_quizzes = self.db.query(QuizModel).offset(skip).limit(limit).all()
        
        return [self._to_entity(db_quiz) for db_quiz in db_quizzes]

    async def get_by_journey_id(self, journey_id: UUID, skip: int = 0, limit: int = 100) -> List[Quiz]:
        db_quizzes = (
            self.db.query(QuizModel)
            .filter(QuizModel.journey_id == journey_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(db_quiz) for db_quiz in db_quizzes]

    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Quiz]:
        db_quizzes = (
            self.db.query(QuizModel)
            .filter(QuizModel.user_id == user_id)
            .order_by(QuizModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(db_quiz) for db_quiz in db_quizzes]

    async def update(self, quiz: Quiz) -> Quiz:
        db_quiz = self.db.query(QuizModel).filter(QuizModel.id == quiz.id).first()
        if db_quiz:
            db_quiz.title = quiz.title
            db_quiz.description = quiz.description
            db_quiz.journey_id = quiz.journey_id
            db_quiz.user_id = quiz.user_id
            db_quiz.estimated_time = quiz.estimated_time
            db_quiz.feedback_mode = quiz.feedback_mode.value if quiz.feedback_mode else "final"
            db_quiz.difficulty = quiz.difficulty.value if quiz.difficulty else None
            db_quiz.image_url = quiz.image_url
            db_quiz.updated_at = quiz.updated_at
            self.db.commit()
            self.db.refresh(db_quiz)
            return self._to_entity(db_quiz)
        raise ValueError(f"Quiz with ID '{quiz.id}' not found")

    async def delete(self, quiz_id: UUID) -> bool:
        db_quiz = self.db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
        if db_quiz:
            self.db.delete(db_quiz)
            self.db.commit()
            return True
        return False

def get_quiz_repository(db: Annotated[Session, Depends(get_db)]) -> QuizRepository:
    return QuizRepositoryImpl(db)