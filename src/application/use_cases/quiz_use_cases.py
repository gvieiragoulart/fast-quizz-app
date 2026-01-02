from typing import Optional, List
from uuid import UUID

from ...domain.entities.quiz import Quiz
from ...domain.repositories.quiz_repository import QuizRepository


class QuizUseCases:
    """Use cases for Quiz entity."""

    def __init__(self, quiz_repository: QuizRepository):
        self.quiz_repository = quiz_repository

    async def create_quiz(self, quiz: Quiz) -> Quiz:
        """Create a new quiz."""
        return await self.quiz_repository.create(quiz)

    async def get_quiz(self, quiz_id: UUID, include_questions: bool = False) -> Optional[Quiz]:
        """Get a quiz by ID."""
        return await self.quiz_repository.get_by_id(quiz_id, include_questions=include_questions)


    async def get_all_quizzes(self, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """Get all quizzes with pagination."""
        return await self.quiz_repository.get_all(skip=skip, limit=limit)

    async def get_journey_quizzes(
        self, journey_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Quiz]:
        """Get all quizzes for a specific journey."""
        return await self.quiz_repository.get_by_journey_id(
            journey_id=journey_id, skip=skip, limit=limit
        )

    async def update_quiz(self, quiz: Quiz) -> Quiz:
        """Update a quiz."""
        existing_quiz = await self.quiz_repository.get_by_id(quiz.id)
        if not existing_quiz:
            raise ValueError(f"Quiz with ID '{quiz.id}' not found")

        return await self.quiz_repository.update(quiz)

    async def delete_quiz(self, quiz_id: UUID) -> bool:
        """Delete a quiz."""
        existing_quiz = await self.quiz_repository.get_by_id(quiz_id)
        if not existing_quiz:
            raise ValueError(f"Quiz with ID '{quiz_id}' not found")

        return await self.quiz_repository.delete(quiz_id)
