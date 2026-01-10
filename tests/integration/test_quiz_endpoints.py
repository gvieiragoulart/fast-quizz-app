import pytest
from fastapi.testclient import TestClient


def test_create_quiz(client: TestClient, token) -> None:
    """Test creating a quiz without journey."""
    response = client.post(
        "/api/quizzes/",
        json={
            "title": "Python Variables",
            "description": "Test your knowledge of Python variables",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Variables"
    assert data["journey_id"] is None


def test_get_quiz_by_id(client: TestClient, token) -> None:
    """Test getting a quiz by ID."""

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Test Quiz",
            "description": "Test Description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    quiz_id = create_response.json()["id"]

    # Get quiz
    response = client.get(
        f"/api/quizzes/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == quiz_id
    assert data["title"] == "Test Quiz"


def test_update_quiz(client: TestClient, token) -> None:
    """Test updating a quiz."""

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Original Title",
            "description": "Original Description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    quiz_id = create_response.json()["id"]

    # Update quiz
    response = client.put(
        f"/api/quizzes/{quiz_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_quiz(client: TestClient, token) -> None:
    """Test deleting a quiz."""

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "To Be Deleted",
            "description": "Description",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    quiz_id = create_response.json()["id"]

    # Delete quiz
    response = client.delete(
        f"/api/quizzes/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    # Verify quiz is deleted
    get_response = client.get(
        f"/api/quizzes/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404
