from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.journey import Journey
from ...domain.repositories.journey_repository import JourneyRepository
from ..database.models import JourneyModel


class JourneyRepositoryImpl(JourneyRepository):
    """SQLAlchemy implementation of JourneyRepository."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: JourneyModel) -> Journey:
        """Convert database model to domain entity."""
        return Journey(
            id=model.id,
            title=model.title,
            description=model.description,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Journey) -> JourneyModel:
        """Convert domain entity to database model."""
        return JourneyModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, journey: Journey) -> Journey:
        """Create a new journey."""
        db_journey = self._to_model(journey)
        self.db.add(db_journey)
        self.db.commit()
        self.db.refresh(db_journey)
        return self._to_entity(db_journey)

    async def get_by_id(self, journey_id: UUID) -> Optional[Journey]:
        """Get a journey by ID."""
        db_journey = self.db.query(JourneyModel).filter(JourneyModel.id == journey_id).first()
        return self._to_entity(db_journey) if db_journey else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Journey]:
        """Get all journeys with pagination."""
        db_journeys = self.db.query(JourneyModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_journey) for db_journey in db_journeys]

    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Journey]:
        """Get all journeys for a specific user."""
        db_journeys = (
            self.db.query(JourneyModel)
            .filter(JourneyModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(db_journey) for db_journey in db_journeys]

    async def update(self, journey: Journey) -> Journey:
        """Update a journey."""
        db_journey = self.db.query(JourneyModel).filter(JourneyModel.id == journey.id).first()
        if db_journey:
            db_journey.title = journey.title
            db_journey.description = journey.description
            db_journey.user_id = journey.user_id
            db_journey.updated_at = journey.updated_at
            self.db.commit()
            self.db.refresh(db_journey)
            return self._to_entity(db_journey)
        raise ValueError(f"Journey with ID '{journey.id}' not found")

    async def delete(self, journey_id: UUID) -> bool:
        """Delete a journey."""
        db_journey = self.db.query(JourneyModel).filter(JourneyModel.id == journey_id).first()
        if db_journey:
            self.db.delete(db_journey)
            self.db.commit()
            return True
        return False
