import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient, username: str = "testuser") -> str:
    """Helper function to get authentication token."""
    client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpassword123",
        },
    )
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": "testpassword123"},
    )
    return response.json()["access_token"]


def create_journey_and_quiz(client: TestClient, token: str) -> str:
    """Helper function to create journey and quiz, return quiz ID."""
    journey_response = client.post(
        "/api/journeys/",
        json={"title": "Test Journey", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    journey_id = journey_response.json()["id"]

    quiz_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Test Quiz",
            "description": "Test Description",
            "journey_id": journey_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return quiz_response.json()["id"]


def test_create_question(client: TestClient) -> None:
    """Test creating a question."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "What is 2 + 2?"
    assert data["correct_answer"] == "4"
    assert len(data["options"]) == 4


def test_create_question_invalid_answer(client: TestClient) -> None:
    """Test creating a question with invalid correct answer."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": ["3", "4", "5", "6"],
            "correct_answer": "7",  # Not in options
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_get_questions_by_quiz(client: TestClient) -> None:
    """Test getting all questions for a quiz."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create questions
    client.post(
        "/api/questions/",
        json={
            "text": "Question 1",
            "quiz_id": quiz_id,
            "options": ["A", "B"],
            "correct_answer": "A",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/questions/",
        json={
            "text": "Question 2",
            "quiz_id": quiz_id,
            "options": ["C", "D"],
            "correct_answer": "C",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get questions (should not include correct answers)
    response = client.get(
        f"/api/questions/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Verify correct_answer is not in response
    assert "correct_answer" not in data[0]


def test_get_question_by_id(client: TestClient) -> None:
    """Test getting a question by ID."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create question
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "Test Question",
            "quiz_id": quiz_id,
            "options": ["A", "B", "C"],
            "correct_answer": "B",
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


def test_check_answer_correct(client: TestClient) -> None:
    """Test checking a correct answer."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create question
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": ["3", "4", "5"],
            "correct_answer": "4",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Check correct answer
    response = client.post(
        f"/api/questions/{question_id}/check",
        json={"answer": "4"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["correct_answer"] is None


def test_check_answer_incorrect(client: TestClient) -> None:
    """Test checking an incorrect answer."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create question
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "What is 2 + 2?",
            "quiz_id": quiz_id,
            "options": ["3", "4", "5"],
            "correct_answer": "4",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Check incorrect answer
    response = client.post(
        f"/api/questions/{question_id}/check",
        json={"answer": "3"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["correct_answer"] == "4"


def test_update_question(client: TestClient) -> None:
    """Test updating a question."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create question
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "Original Question",
            "quiz_id": quiz_id,
            "options": ["A", "B"],
            "correct_answer": "A",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    question_id = create_response.json()["id"]

    # Update question
    response = client.put(
        f"/api/questions/{question_id}",
        json={"text": "Updated Question"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Updated Question"


def test_delete_question(client: TestClient) -> None:
    """Test deleting a question."""
    token = get_auth_token(client)
    quiz_id = create_journey_and_quiz(client, token)

    # Create question
    create_response = client.post(
        "/api/questions/",
        json={
            "text": "To Be Deleted",
            "quiz_id": quiz_id,
            "options": ["A", "B"],
            "correct_answer": "A",
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
