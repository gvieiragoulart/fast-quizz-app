from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ..database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, user: User) -> User:
        """Create a new user."""
        db_user = self._to_model(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        db_users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_user) for db_user in db_users]

    async def update(self, user: User) -> User:
        """Update a user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.username = user.username
            db_user.email = user.email
            db_user.hashed_password = user.hashed_password
            db_user.is_active = user.is_active
            db_user.updated_at = user.updated_at
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_entity(db_user)
        raise ValueError(f"User with ID '{user.id}' not found")

    async def delete(self, user_id: UUID) -> bool:
        """Delete a user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
