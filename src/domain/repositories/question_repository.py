from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.question import Question


class QuestionRepository(ABC):
    """Abstract repository interface for Question entity."""

    @abstractmethod
    async def create(self, question: Question) -> Question:
        """Create a new question."""
        pass

    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        """Get a question by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions with pagination."""
        pass

    @abstractmethod
    async def get_by_quiz_id(self, quiz_id: UUID, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions for a specific quiz."""
        pass

    @abstractmethod
    async def update(self, question: Question) -> Question:
        """Update a question."""
        pass

    @abstractmethod
    async def delete(self, question_id: UUID) -> bool:
        """Delete a question."""
        pass
