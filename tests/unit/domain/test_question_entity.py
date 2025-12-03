from uuid import uuid4
from datetime import datetime

from src.domain.entities.question import Question


def test_create_question() -> None:
    """Test creating a question entity."""
    quiz_id = uuid4()
    options = ["int", "str", "float", "bool"]
    question = Question(
        text="What is the default data type for numbers in Python?",
        quiz_id=quiz_id,
        options=options,
        correct_answer="int",
    )

    assert question.text == "What is the default data type for numbers in Python?"
    assert question.quiz_id == quiz_id
    assert question.options == options
    assert question.correct_answer == "int"
    assert question.id is not None
    assert isinstance(question.created_at, datetime)
    assert isinstance(question.updated_at, datetime)


def test_question_is_correct() -> None:
    """Test checking if an answer is correct."""
    quiz_id = uuid4()
    question = Question(
        text="What is 2 + 2?",
        quiz_id=quiz_id,
        options=["3", "4", "5", "6"],
        correct_answer="4",
    )

    assert question.is_correct("4") is True
    assert question.is_correct("3") is False
    assert question.is_correct("5") is False


def test_question_equality() -> None:
    """Test question equality based on ID."""
    question_id = uuid4()
    quiz_id = uuid4()
    question1 = Question(
        id=question_id,
        text="Question 1",
        quiz_id=quiz_id,
        options=["A", "B"],
        correct_answer="A",
    )
    question2 = Question(
        id=question_id,
        text="Question 2",
        quiz_id=quiz_id,
        options=["C", "D"],
        correct_answer="C",
    )
    question3 = Question(
        text="Question 3",
        quiz_id=quiz_id,
        options=["E", "F"],
        correct_answer="E",
    )

    assert question1 == question2
    assert question1 != question3


def test_question_repr() -> None:
    """Test question string representation."""
    quiz_id = uuid4()
    question = Question(
        text="This is a very long question text that should be truncated in the repr",
        quiz_id=quiz_id,
        options=["A", "B"],
        correct_answer="A",
    )

    repr_str = repr(question)
    assert "Question" in repr_str
