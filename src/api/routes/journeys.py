from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ...infrastructure.database import get_db
from ...infrastructure.repositories import JourneyRepositoryImpl
from ...application.use_cases import JourneyUseCases
from ...domain.entities.journey import Journey
from ...domain.entities.user import User
from ..schemas import JourneyCreate, JourneyResponse, JourneyUpdate
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/journeys", tags=["journeys"])


@router.post("/", response_model=JourneyResponse, status_code=status.HTTP_201_CREATED)
async def create_journey(
    journey_data: JourneyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Create a new journey."""
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)

    journey = Journey(
        title=journey_data.title,
        description=journey_data.description,
        user_id=current_user.id,
    )

    created_journey = await journey_use_cases.create_journey(journey)
    return JourneyResponse(
        id=created_journey.id,
        title=created_journey.title,
        description=created_journey.description,
        user_id=created_journey.user_id,
        created_at=created_journey.created_at,
        updated_at=created_journey.updated_at,
    )


@router.get("/", response_model=List[JourneyResponse])
async def get_journeys(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[JourneyResponse]:
    """Get all journeys for the current user."""
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)

    journeys = await journey_use_cases.get_user_journeys(
        user_id=current_user.id, skip=skip, limit=limit
    )
    return [
        JourneyResponse(
            id=journey.id,
            title=journey.title,
            description=journey.description,
            user_id=journey.user_id,
            created_at=journey.created_at,
            updated_at=journey.updated_at,
        )
        for journey in journeys
    ]


@router.get("/{journey_id}", response_model=JourneyResponse)
async def get_journey(
    journey_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Get a journey by ID."""
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)

    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

    # Check if user owns the journey
    if journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this journey",
        )

    return JourneyResponse(
        id=journey.id,
        title=journey.title,
        description=journey.description,
        user_id=journey.user_id,
        created_at=journey.created_at,
        updated_at=journey.updated_at,
    )


@router.put("/{journey_id}", response_model=JourneyResponse)
async def update_journey(
    journey_id: UUID,
    journey_data: JourneyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Update a journey."""
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)

    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

    # Check if user owns the journey
    if journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this journey",
        )

    # Update fields if provided
    if journey_data.title is not None:
        journey.title = journey_data.title
    if journey_data.description is not None:
        journey.description = journey_data.description

    try:
        updated_journey = await journey_use_cases.update_journey(journey)
        return JourneyResponse(
            id=updated_journey.id,
            title=updated_journey.title,
            description=updated_journey.description,
            user_id=updated_journey.user_id,
            created_at=updated_journey.created_at,
            updated_at=updated_journey.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{journey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journey(
    journey_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a journey."""
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)

    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

    # Check if user owns the journey
    if journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this journey",
        )

    try:
        await journey_use_cases.delete_journey(journey_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
