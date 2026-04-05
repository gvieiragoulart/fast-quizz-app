from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class FeedbackMode(str, Enum):
    FINAL = "final"
    IMEDIATO = "imediato"


class Difficulty(str, Enum):
    FACIL = "facil"
    MEDIO = "medio"
    DIFICIL = "dificil"
    EXPERT = "expert"


class Quiz:
    def __init__(
        self,
        title: str,
        description: str,
        journey_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        id: Optional[UUID] = None,
        questions: Optional[list] = None,
        estimated_time: Optional[int] = None,
        feedback_mode: FeedbackMode = FeedbackMode.FINAL,
        difficulty: Difficulty = Difficulty.FACIL,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.journey_id = journey_id
        self.user_id = user_id
        self.questions = questions or []
        self.estimated_time = estimated_time
        self.feedback_mode = feedback_mode
        self.difficulty = difficulty
        self.image_url = image_url
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Quiz(id={self.id}, title={self.title}, journey_id={self.journey_id}, questions={len(self.questions)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quiz):
            return False
        return self.id == other.id
