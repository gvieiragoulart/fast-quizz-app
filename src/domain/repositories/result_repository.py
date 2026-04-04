from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.results import Result


class ResultRepository(ABC):

    @abstractmethod
    async def create(self, result: Result) -> Result:
        pass

    @abstractmethod
    async def get_by_quiz_id(self, quiz_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Result]:
        pass
