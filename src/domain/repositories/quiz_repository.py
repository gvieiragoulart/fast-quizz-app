from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.quiz import Quiz


class QuizRepository(ABC):
    """Abstract repository interface for Quiz entity."""

    @abstractmethod
    async def create(self, quiz: Quiz) -> Quiz:
        """Create a new quiz."""
        pass

    @abstractmethod
    async def get_by_id(self, quiz_id: UUID, include_questions: bool = False) -> Optional[Quiz]:
        """Get a quiz by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes with pagination."""
        pass

    @abstractmethod
    async def get_by_journey_id(self, journey_id: UUID, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes for a specific journey."""
        pass

    @abstractmethod
    async def update(self, quiz: Quiz) -> Quiz:
        """Update a quiz."""
        pass

    @abstractmethod
    async def delete(self, quiz_id: UUID) -> bool:
        """Delete a quiz."""
        pass
