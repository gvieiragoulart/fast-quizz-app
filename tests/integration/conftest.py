import pytest

from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
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
        json={"email": f"{username}@example.com", "password": "testpassword123"},
    )
    return response.json()["access_token"]