from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Quiz:
    """Domain entity representing a quiz."""

    def __init__(
        self,
        title: str,
        description: str,
        journey_id: Optional[UUID] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.journey_id = journey_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"Quiz(id={self.id}, title={self.title}, journey_id={self.journey_id})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quiz):
            return False
        return self.id == other.id
