from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from uuid import UUID

from ...application.use_cases import JourneyUseCases
from ...application.use_cases.journey_use_cases import get_journey_use_cases
from ...domain.entities.journey import Journey
from ...domain.entities.user import User
from ..schemas import JourneyCreate, JourneyResponse, JourneyUpdate
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/journeys", tags=["journeys"])
JourneyUseCasesDep = Annotated[JourneyUseCases, Depends(get_journey_use_cases)]


@router.post("/", response_model=JourneyResponse, status_code=status.HTTP_201_CREATED)
async def create_journey(
    journey_data: JourneyCreate,
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Create a new journey."""
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
    journey_use_cases: JourneyUseCasesDep = ...,
    current_user: User = Depends(get_current_active_user),
) -> List[JourneyResponse]:
    """Get all journeys for the current user."""
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
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Get a journey by ID."""
    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

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
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> JourneyResponse:
    """Update a journey."""
    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

    if journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this journey",
        )

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
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a journey."""
    journey = await journey_use_cases.get_journey(journey_id)
    if not journey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
        )

    if journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this journey",
        )

    try:
        await journey_use_cases.delete_journey(journey_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
