from uuid import uuid4
from datetime import datetime

from src.domain.entities.user import User


def test_create_user() -> None:
    """Test creating a user entity."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password_123",
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password_123"
    assert user.is_active is True
    assert user.id is not None
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_equality() -> None:
    """Test user equality based on ID."""
    user_id = uuid4()
    user1 = User(
        id=user_id,
        username="user1",
        email="user1@example.com",
        hashed_password="hash1",
    )
    user2 = User(
        id=user_id,
        username="user2",
        email="user2@example.com",
        hashed_password="hash2",
    )
    user3 = User(
        username="user3",
        email="user3@example.com",
        hashed_password="hash3",
    )

    assert user1 == user2
    assert user1 != user3


def test_user_repr() -> None:
    """Test user string representation."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
    )

    repr_str = repr(user)
    assert "User" in repr_str
    assert "testuser" in repr_str
    assert "test@example.com" in repr_str
