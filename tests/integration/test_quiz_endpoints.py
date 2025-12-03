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


def create_journey(client: TestClient, token: str) -> str:
    """Helper function to create a journey and return its ID."""
    response = client.post(
        "/api/journeys/",
        json={"title": "Test Journey", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["id"]


def test_create_quiz(client: TestClient) -> None:
    """Test creating a quiz."""
    token = get_auth_token(client)
    journey_id = create_journey(client, token)

    response = client.post(
        "/api/quizzes/",
        json={
            "title": "Python Variables",
            "description": "Test your knowledge of Python variables",
            "journey_id": journey_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Variables"
    assert data["journey_id"] == journey_id


def test_get_quizzes_by_journey(client: TestClient) -> None:
    """Test getting all quizzes for a journey."""
    token = get_auth_token(client)
    journey_id = create_journey(client, token)

    # Create quizzes
    client.post(
        "/api/quizzes/",
        json={
            "title": "Quiz 1",
            "description": "Description 1",
            "journey_id": journey_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/quizzes/",
        json={
            "title": "Quiz 2",
            "description": "Description 2",
            "journey_id": journey_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get quizzes
    response = client.get(
        f"/api/quizzes/journey/{journey_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_quiz_by_id(client: TestClient) -> None:
    """Test getting a quiz by ID."""
    token = get_auth_token(client)
    journey_id = create_journey(client, token)

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Test Quiz",
            "description": "Test Description",
            "journey_id": journey_id,
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


def test_update_quiz(client: TestClient) -> None:
    """Test updating a quiz."""
    token = get_auth_token(client)
    journey_id = create_journey(client, token)

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "Original Title",
            "description": "Original Description",
            "journey_id": journey_id,
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


def test_delete_quiz(client: TestClient) -> None:
    """Test deleting a quiz."""
    token = get_auth_token(client)
    journey_id = create_journey(client, token)

    # Create quiz
    create_response = client.post(
        "/api/quizzes/",
        json={
            "title": "To Be Deleted",
            "description": "Description",
            "journey_id": journey_id,
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
