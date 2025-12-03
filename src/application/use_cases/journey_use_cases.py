from typing import Optional, List
from uuid import UUID

from ...domain.entities.journey import Journey
from ...domain.repositories.journey_repository import JourneyRepository


class JourneyUseCases:
    """Use cases for Journey entity."""

    def __init__(self, journey_repository: JourneyRepository):
        self.journey_repository = journey_repository

    async def create_journey(self, journey: Journey) -> Journey:
        """Create a new journey."""
        return await self.journey_repository.create(journey)

    async def get_journey(self, journey_id: UUID) -> Optional[Journey]:
        """Get a journey by ID."""
        return await self.journey_repository.get_by_id(journey_id)

    async def get_all_journeys(self, skip: int = 0, limit: int = 100) -> List[Journey]:
        """Get all journeys with pagination."""
        return await self.journey_repository.get_all(skip=skip, limit=limit)

    async def get_user_journeys(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Journey]:
        """Get all journeys for a specific user."""
        return await self.journey_repository.get_by_user_id(
            user_id=user_id, skip=skip, limit=limit
        )

    async def update_journey(self, journey: Journey) -> Journey:
        """Update a journey."""
        existing_journey = await self.journey_repository.get_by_id(journey.id)
        if not existing_journey:
            raise ValueError(f"Journey with ID '{journey.id}' not found")

        return await self.journey_repository.update(journey)

    async def delete_journey(self, journey_id: UUID) -> bool:
        """Delete a journey."""
        existing_journey = await self.journey_repository.get_by_id(journey_id)
        if not existing_journey:
            raise ValueError(f"Journey with ID '{journey_id}' not found")

        return await self.journey_repository.delete(journey_id)
