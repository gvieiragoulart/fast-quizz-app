from typing import Annotated, List
from uuid import UUID

from fastapi import Depends

from src.infrastructure.repositories.result_repository_impl import get_result_repository

from ...domain.entities.results import Result
from ...domain.repositories.result_repository import ResultRepository


class ResultUseCases:

    def __init__(self, result_repository: ResultRepository):
        self.result_repository = result_repository

    async def create_result(self, result: Result) -> Result:
        return await self.result_repository.create(result)

    async def get_results_by_quiz(self, quiz_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        return await self.result_repository.get_by_quiz_id(quiz_id, skip=skip, limit=limit)

    async def get_results_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        return await self.result_repository.get_by_user_id(user_id, skip=skip, limit=limit)


def get_result_use_cases(
    result_repository: Annotated[ResultRepository, Depends(get_result_repository)],
) -> ResultUseCases:
    return ResultUseCases(result_repository)
