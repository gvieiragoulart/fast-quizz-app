from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from ...domain.entities.question import Question
from ...domain.entities.option import Option
from ...domain.repositories.question_repository import QuestionRepository
from ..database.models import QuestionModel, QuestionOptionModel


class QuestionRepositoryImpl(QuestionRepository):
    """SQLAlchemy implementation of QuestionRepository."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: QuestionModel) -> Question:
        """Convert database model to domain entity."""
        options = [
            Option(
                id=opt.id,
                text=opt.text,
                order=opt.order,
                is_correct=opt.is_correct,
                image_url=opt.image_url,
                metadata=opt.metadata_json,
                created_at=opt.created_at,
                updated_at=opt.updated_at,
            )
            for opt in getattr(model, "options", []) or []
        ]
        return Question(
            id=model.id,
            text=model.text,
            quiz_id=model.quiz_id,
            options=options,
            correct_answer=model.correct_answer,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Question) -> QuestionModel:
        """Convert domain entity to database model."""
        q_model = QuestionModel(
            id=entity.id,
            text=entity.text,
            quiz_id=entity.quiz_id,
            correct_answer=entity.correct_answer,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        # build option models and attach to question model (cascade will persist them)
        opt_models = []
        for opt in entity.options or []:
            opt_models.append(
                QuestionOptionModel(
                    id=opt.id,
                    question_id=entity.id,
                    text=opt.text,
                    order=opt.order,
                    is_correct=opt.is_correct,
                    image_url=opt.image_url,
                    metadata_json=opt.metadata,
                    created_at=opt.created_at,
                    updated_at=opt.updated_at,
                )
            )
        q_model.options = opt_models
        return q_model

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
        """Update a question and its options (replace options)."""
        db_question = self.db.query(QuestionModel).filter(QuestionModel.id == question.id).first()
        if db_question:
            db_question.text = question.text
            db_question.quiz_id = question.quiz_id
            db_question.correct_answer = question.correct_answer
            db_question.updated_at = question.updated_at

            # replace options: remove existing and add new ones
            # (simpler than diffing; acceptable for typical quiz workflows)
            # delete existing option rows
            for ex in list(db_question.options):
                self.db.delete(ex)
            self.db.flush()

            new_opt_models = []
            for opt in question.options or []:
                new_opt_models.append(
                    QuestionOptionModel(
                        id=opt.id,
                        question_id=question.id,
                        text=opt.text,
                        order=opt.order,
                        is_correct=opt.is_correct,
                        image_url=opt.image_url,
                        metadata_json=opt.metadata,
                        created_at=opt.created_at,
                        updated_at=opt.updated_at,
                    )
                )
            db_question.options = new_opt_models

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
