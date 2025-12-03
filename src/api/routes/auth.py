from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ...infrastructure.database import get_db
from ...infrastructure.auth import verify_password, create_access_token, get_password_hash
from ...infrastructure.repositories import UserRepositoryImpl
from ...application.use_cases import UserUseCases
from ...domain.entities.user import User
from ..schemas import Token, LoginRequest, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Register a new user."""
    user_repo = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repo)

    # Create user entity
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    try:
        created_user = await user_use_cases.create_user(user)
        return UserResponse(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)) -> Token:
    """Authenticate a user and return a JWT token."""
    user_repo = UserRepositoryImpl(db)
    user_use_cases = UserUseCases(user_repo)

    user = await user_use_cases.get_user_by_username(login_data.username)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
