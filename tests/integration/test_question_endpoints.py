import pytest
from fastapi.testclient import TestClient


def create_quiz(client: TestClient, token: str) -> str:
    """Helper function to create quiz, return quiz ID."""
    quiz_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Test Quiz",
            "description": "Test Description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return quiz_response.json()["id"]


def make_options(texts: list) -> list:
    """Helper to create options in the expected format."""
    return [
        {"reference_id": i + 1, "text": text, "order": i + 1}
        for i, text in enumerate(texts)
    ]


def test_create_question(client: TestClient, token) -> None:
    """Test creating a question."""
    quiz_id = create_quiz(client, token)

    response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": [
                {
                    "reference_id": 1,
                    "text": "teste3",
                    "order": 1,

                },
                {
                    "reference_id": 2,
                    "text": "teste4",
                    "order": 2,
                    "is_correct": True
                },
                {
                    "reference_id": 3,
                    "text": "teste5",
                    "order": 3
                },
                {
                    "reference_id": 4,
                    "text": "teste6",
                    "order": 4
                }
            ],
            "correct_answer": 2,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "What is 2 + 2?"
    assert data["correct_answer"] == 2
    assert len(data["options"]) == 4


def test_create_question_invalid_answer(client: TestClient, token) -> None:
    """Test creating a question with invalid correct answer."""
    quiz_id = create_quiz(client, token)

    response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": [
                {
                    "reference_id": 1,
                    "text": "3",
                    "order": 1,
                },
                {
                    "reference_id": 2,
                    "text": "4",
                    "order": 2,
                },
                {
                    "reference_id": 3,
                    "text": "5",
                    "order": 3,
                },
            ],
            "correct_answer": 7,  # Not in options (reference_ids are 1, 2, 3)
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_get_questions_by_quiz(client: TestClient, token) -> None:
    """Test getting all questions for a quiz."""
    quiz_id = create_quiz(client, token)

    # Create questions
    client.post(
        "/api/questions/",
        json={
            "text": "Question 1",
            "quiz_id": quiz_id,
            "options": [
                {
                    "reference_id": 1,
                    "text": "A",
                    "order": 1,
                },
                {
                    "reference_id": 2,
                    "text": "B",
                    "order": 2,
                }
            ],
            "correct_answer": 1,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/questions/",
        json={
            "text": "Question 2",
            "quiz_id": quiz_id,
            "options": [
                {
                    "reference_id": 1,
                    "text": "C",
                    "order": 1,
                },
                {
                    "reference_id": 2,
                    "text": "D",
                    "order": 2,
                }
            ],
            "correct_answer": 1,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get questions via query param (should not include correct answers)
    response = client.get(
        f"/api/questions/quiz?quiz_id={quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Verify correct_answer is not in response
    assert "correct_answer" not in data[0]


def test_get_question_by_id(client: TestClient, token) -> None:
    """Test getting a question by ID."""
    quiz_id = create_quiz(client, token)

    # Create question with proper options format
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "Test Question",
            "quiz_id": quiz_id,
            "options": make_options(["A", "B", "C"]),
            "correct_answer": 2,  # reference_id 2 = "B"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Get question (should not include correct answer)
    response = client.get(
        f"/api/questions/{question_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test Question"
    assert "correct_answer" not in data

def test_update_question(client: TestClient, token) -> None:
    """Test updating a question."""
    quiz_id = create_quiz(client, token)

    # Create question with proper options format
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "Original Question",
            "quiz_id": quiz_id,
            "options": make_options(["A", "B"]),
            "correct_answer": 1,  # reference_id 1 = "A"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Update question
    response = client.put(
        f"/api/questions/{question_id}",
        json={
            "text": "Updated Question",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Updated Question"


def test_delete_question(client: TestClient, token) -> None:
    """Test deleting a question."""
    quiz_id = create_quiz(client, token)

    # Create question with proper options format
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "To Be Deleted",
            "quiz_id": quiz_id,
            "options": make_options(["A", "B"]),
            "correct_answer": 1,  # reference_id 1 = "A"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Delete question
    response = client.delete(
        f"/api/questions/{question_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    # Verify question is deleted
    get_response = client.get(
        f"/api/questions/{question_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404
