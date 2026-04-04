from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from uuid import UUID

from ...infrastructure.auth import get_password_hash
from ...application.use_cases import UserUseCases
from ...application.use_cases.user_use_cases import get_user_use_cases
from ...domain.entities.user import User
from ..schemas import UserResponse, UserUpdate
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/users", tags=["users"])
UserUseCasesDep = Annotated[UserUseCases, Depends(get_user_use_cases)]


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_use_cases: UserUseCasesDep = ...,
    current_user: User = Depends(get_current_active_user),
) -> List[UserResponse]:
    """Get all users (requires authentication)."""
    users = await user_use_cases.get_all_users(skip=skip, limit=limit)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_use_cases: UserUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """Get a user by ID."""
    user = await user_use_cases.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_use_cases: UserUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """Update a user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user = await user_use_cases.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password is not None:
        user.hashed_password = get_password_hash(user_data.password)
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    try:
        updated_user = await user_use_cases.update_user(user)
        return UserResponse(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_use_cases: UserUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    try:
        await user_use_cases.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
