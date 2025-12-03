from uuid import uuid4
from datetime import datetime

from src.domain.entities.quiz import Quiz


def test_create_quiz() -> None:
    """Test creating a quiz entity."""
    journey_id = uuid4()
    quiz = Quiz(
        title="Variables and Data Types",
        description="Learn about Python variables",
        journey_id=journey_id,
    )

    assert quiz.title == "Variables and Data Types"
    assert quiz.description == "Learn about Python variables"
    assert quiz.journey_id == journey_id
    assert quiz.id is not None
    assert isinstance(quiz.created_at, datetime)
    assert isinstance(quiz.updated_at, datetime)


def test_quiz_equality() -> None:
    """Test quiz equality based on ID."""
    quiz_id = uuid4()
    journey_id = uuid4()
    quiz1 = Quiz(
        id=quiz_id,
        title="Quiz 1",
        description="Description 1",
        journey_id=journey_id,
    )
    quiz2 = Quiz(
        id=quiz_id,
        title="Quiz 2",
        description="Description 2",
        journey_id=journey_id,
    )
    quiz3 = Quiz(
        title="Quiz 3",
        description="Description 3",
        journey_id=journey_id,
    )

    assert quiz1 == quiz2
    assert quiz1 != quiz3


def test_quiz_repr() -> None:
    """Test quiz string representation."""
    journey_id = uuid4()
    quiz = Quiz(
        title="Test Quiz",
        description="Test Description",
        journey_id=journey_id,
    )

    repr_str = repr(quiz)
    assert "Quiz" in repr_str
    assert "Test Quiz" in repr_str
