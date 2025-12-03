from uuid import uuid4
from datetime import datetime

from src.domain.entities.journey import Journey


def test_create_journey() -> None:
    """Test creating a journey entity."""
    user_id = uuid4()
    journey = Journey(
        title="Python Basics",
        description="Learn Python fundamentals",
        user_id=user_id,
    )

    assert journey.title == "Python Basics"
    assert journey.description == "Learn Python fundamentals"
    assert journey.user_id == user_id
    assert journey.id is not None
    assert isinstance(journey.created_at, datetime)
    assert isinstance(journey.updated_at, datetime)


def test_journey_equality() -> None:
    """Test journey equality based on ID."""
    journey_id = uuid4()
    user_id = uuid4()
    journey1 = Journey(
        id=journey_id,
        title="Journey 1",
        description="Description 1",
        user_id=user_id,
    )
    journey2 = Journey(
        id=journey_id,
        title="Journey 2",
        description="Description 2",
        user_id=user_id,
    )
    journey3 = Journey(
        title="Journey 3",
        description="Description 3",
        user_id=user_id,
    )

    assert journey1 == journey2
    assert journey1 != journey3


def test_journey_repr() -> None:
    """Test journey string representation."""
    user_id = uuid4()
    journey = Journey(
        title="Test Journey",
        description="Test Description",
        user_id=user_id,
    )

    repr_str = repr(journey)
    assert "Journey" in repr_str
    assert "Test Journey" in repr_str
