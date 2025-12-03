import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    """Test user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    assert "id" in data


def test_register_duplicate_username(client: TestClient) -> None:
    """Test registering with duplicate username."""
    # Register first user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "password123",
        },
    )

    # Try to register with same username
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_register_duplicate_email(client: TestClient) -> None:
    """Test registering with duplicate email."""
    # Register first user
    client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    # Try to register with same email
    response = client.post(
        "/api/auth/register",
        json={
            "username": "user2",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(client: TestClient) -> None:
    """Test successful login."""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient) -> None:
    """Test login with wrong password."""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "correctpassword",
        },
    )

    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    """Test login with non-existent user."""
    response = client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "password123"},
    )
    assert response.status_code == 401
