from datetime import datetime, timezone
from typing import Optional, Dict
from uuid import UUID, uuid4


class Option:
    """Domain entity representing a single question option (answer)."""

    def __init__(
        self,
        reference_id: int,
        text: Optional[str] = None,
        order: int = 0,
        is_correct: bool = False,
        image_url: Optional[str] = None,
        metadata: Optional[Dict] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.reference_id = reference_id
        self.text = text
        self.order = order
        self.is_correct = is_correct
        self.image_url = image_url
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        preview = self.text[:30] + "..." if self.text and len(self.text) > 30 else self.text
        return f"Option(id={self.id}, reference_id={self.reference_id}, text={preview}, order={self.order}, is_correct={self.is_correct})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Option):
            return False
        return self.id == other.id
