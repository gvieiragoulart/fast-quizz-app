from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from .option import Option


class Question:
    """Domain entity representing a question with multiple choice options."""

    def __init__(
        self,
        text: str,
        quiz_id: UUID,
        options: List[Option],
        correct_answer: str,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.text = text
        self.quiz_id = quiz_id
        self.options = options
        self.correct_answer = correct_answer
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"Question(id={self.id}, text={self.text[:50]}...)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Question):
            return False
        return self.id == other.id

    def is_correct(self, answer: str) -> bool:
        """Check if the provided answer is correct."""
        return answer == self.correct_answer
