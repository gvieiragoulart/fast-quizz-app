from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.journey import Journey


class JourneyRepository(ABC):
    """Abstract repository interface for Journey entity."""

    @abstractmethod
    async def create(self, journey: Journey) -> Journey:
        """Create a new journey."""
        pass

    @abstractmethod
    async def get_by_id(self, journey_id: UUID) -> Optional[Journey]:
        """Get a journey by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Journey]:
        """Get all journeys with pagination."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Journey]:
        """Get all journeys for a specific user."""
        pass

    @abstractmethod
    async def update(self, journey: Journey) -> Journey:
        """Update a journey."""
        pass

    @abstractmethod
    async def delete(self, journey_id: UUID) -> bool:
        """Delete a journey."""
        pass
