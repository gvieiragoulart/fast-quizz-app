from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


class Journey:
    """Domain entity representing a journey containing multiple quizzes."""

    def __init__(
        self,
        title: str,
        description: str,
        user_id: UUID,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"Journey(id={self.id}, title={self.title})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Journey):
            return False
        return self.id == other.id
