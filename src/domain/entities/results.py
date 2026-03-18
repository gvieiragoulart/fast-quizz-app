from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

class Result:
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        respondent_name: str,
        quiz_id: UUID,
        score: float,
        total_questions: int,
        taken_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.respondent_name = respondent_name
        self.quiz_id = quiz_id
        self.score = score
        self.total_questions = total_questions
        self.taken_at = taken_at or datetime.now(timezone.utc)

    def __repr__(self):
        return f"Result(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score}/{self.total_questions})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Result):
            return False
        return self.id == other.id