from typing import Optional, List
from uuid import UUID

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository


class UserUseCases:
    """Use cases for User entity."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        """Create a new user."""
        # Check if username already exists
        existing_user = await self.user_repository.get_by_username(user.username)
        if existing_user:
            raise ValueError(f"Username '{user.username}' already exists")

        # Check if email already exists
        existing_email = await self.user_repository.get_by_email(user.email)
        if existing_email:
            raise ValueError(f"Email '{user.email}' already exists")

        return await self.user_repository.create(user)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return await self.user_repository.get_by_username(username)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return await self.user_repository.get_all(skip=skip, limit=limit)

    async def update_user(self, user: User) -> User:
        """Update a user."""
        existing_user = await self.user_repository.get_by_id(user.id)
        if not existing_user:
            raise ValueError(f"User with ID '{user.id}' not found")

        return await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User with ID '{user_id}' not found")

        return await self.user_repository.delete(user_id)
