from typing import Optional, List
from uuid import UUID

from ...domain.entities.question import Question
from ...domain.entities.option import Option
from ...domain.repositories.question_repository import QuestionRepository


class QuestionUseCases:
    """Use cases for Question entity."""

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def create_question(self, question: Question) -> Question:
        """Create a new question."""
        # normalize options: accept domain Option instances or mapping/pydantic objects or plain strings
        normalized_options = []
        for opt in question.options or []:
            normalized_options.append(
                Option(
                    text=getattr(opt, "text", None),
                    order=getattr(opt, "order", 0) or 0,
                    is_correct=getattr(opt, "is_correct", False) or False,
                    image_url=getattr(opt, "image_url", None),
                    metadata=getattr(opt, "metadata", None),
                )
            )

        question.options = normalized_options

        if question.correct_answer not in [option.text for option in question.options]:
            raise ValueError("Correct answer must be one of the options")

        return await self.question_repository.create(question)

    async def get_question(self, question_id: UUID) -> Optional[Question]:
        """Get a question by ID."""
        return await self.question_repository.get_by_id(question_id)

    async def get_all_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions with pagination."""
        return await self.question_repository.get_all(skip=skip, limit=limit)

    async def get_quiz_questions(
        self, quiz_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Question]:
        """Get all questions for a specific quiz."""
        return await self.question_repository.get_by_quiz_id(
            quiz_id=quiz_id, skip=skip, limit=limit
        )

    async def update_question(self, question: Question) -> Question:
        """Update a question."""
        existing_question = await self.question_repository.get_by_id(question.id)
        if not existing_question:
            raise ValueError(f"Question with ID '{question.id}' not found")
        # normalize options similar to create
        normalized_options = []
        for opt in question.options or []:
            normalized_options.append(
                Option(
                    text=getattr(opt, "text", None),
                    order=getattr(opt, "order", 0) or 0,
                    is_correct=getattr(opt, "is_correct", False) or False,
                    image_url=getattr(opt, "image_url", None),
                    metadata=getattr(opt, "metadata", None),
                )
            )

        question.options = normalized_options

        if question.correct_answer not in [option.text for option in question.options]:
            raise ValueError("Correct answer must be one of the options")

        return await self.question_repository.update(question)

    async def delete_question(self, question_id: UUID) -> bool:
        """Delete a question."""
        existing_question = await self.question_repository.get_by_id(question_id)
        if not existing_question:
            raise ValueError(f"Question with ID '{question_id}' not found")

        return await self.question_repository.delete(question_id)
