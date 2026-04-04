from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.results import Result
from ...domain.repositories.result_repository import ResultRepository
from ..database.models import ResultsModel


class ResultRepositoryImpl(ResultRepository):

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: ResultsModel) -> Result:
        return Result(
            id=model.id,
            user_id=model.user_id,
            respondent_name=model.respondent_name,
            quiz_id=model.quiz_id,
            score=model.score,
            total_questions=model.total_questions,
            taken_at=model.taken_at,
        )

    async def create(self, result: Result) -> Result:
        db_result = ResultsModel(
            id=result.id,
            user_id=result.user_id,
            respondent_name=result.respondent_name,
            quiz_id=result.quiz_id,
            score=result.score,
            total_questions=result.total_questions,
            taken_at=result.taken_at,
        )
        self.db.add(db_result)
        self.db.commit()
        self.db.refresh(db_result)
        return self._to_entity(db_result)

    async def get_by_quiz_id(self, quiz_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        db_results = (
            self.db.query(ResultsModel)
            .filter(ResultsModel.quiz_id == quiz_id)
            .order_by(ResultsModel.taken_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_results]

    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        db_results = (
            self.db.query(ResultsModel)
            .filter(ResultsModel.user_id == user_id)
            .order_by(ResultsModel.taken_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(r) for r in db_results]
