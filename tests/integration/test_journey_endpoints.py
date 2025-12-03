import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient, username: str = "testuser") -> str:
    """Helper function to get authentication token."""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpassword123",
        },
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": "testpassword123"},
    )
    return response.json()["access_token"]


def test_create_journey(client: TestClient) -> None:
    """Test creating a journey."""
    token = get_auth_token(client)

    response = client.post(
        "/api/journeys/",
        json={
            "title": "Python Basics",
            "description": "Learn Python fundamentals",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Basics"
    assert data["description"] == "Learn Python fundamentals"
    assert "id" in data


def test_get_journeys(client: TestClient) -> None:
    """Test getting all journeys for user."""
    token = get_auth_token(client)

    # Create journeys
    client.post(
        "/api/journeys/",
        json={"title": "Journey 1", "description": "Description 1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/journeys/",
        json={"title": "Journey 2", "description": "Description 2"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get journeys
    response = client.get(
        "/api/journeys/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_journey_by_id(client: TestClient) -> None:
    """Test getting a journey by ID."""
    token = get_auth_token(client)

    # Create journey
    create_response = client.post(
        "/api/journeys/",
        json={"title": "Test Journey", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    journey_id = create_response.json()["id"]

    # Get journey
    response = client.get(
        f"/api/journeys/{journey_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == journey_id
    assert data["title"] == "Test Journey"


def test_update_journey(client: TestClient) -> None:
    """Test updating a journey."""
    token = get_auth_token(client)

    # Create journey
    create_response = client.post(
        "/api/journeys/",
        json={"title": "Original Title", "description": "Original Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    journey_id = create_response.json()["id"]

    # Update journey
    response = client.put(
        f"/api/journeys/{journey_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original Description"


def test_delete_journey(client: TestClient) -> None:
    """Test deleting a journey."""
    token = get_auth_token(client)

    # Create journey
    create_response = client.post(
        "/api/journeys/",
        json={"title": "To Be Deleted", "description": "Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    journey_id = create_response.json()["id"]

    # Delete journey
    response = client.delete(
        f"/api/journeys/{journey_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    # Verify journey is deleted
    get_response = client.get(
        f"/api/journeys/{journey_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404


def test_unauthorized_access(client: TestClient) -> None:
    """Test accessing journeys without authentication."""
    response = client.get("/api/journeys/")
    assert response.status_code == 401
