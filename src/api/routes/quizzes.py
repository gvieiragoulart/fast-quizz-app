from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.domain.entities.question import Question

from ...infrastructure.database import get_db
from ...infrastructure.repositories import (
    QuizRepositoryImpl, 
    JourneyRepositoryImpl,
    QuestionRepositoryImpl,
)
from ...application.use_cases import (
    QuizUseCases, 
    JourneyUseCases,
    QuestionUseCases,
)
from ...domain.entities.quiz import Quiz
from ...domain.entities.user import User
from ..schemas import QuizCreate, QuizResponse, QuizUpdate
from ..dependencies import get_current_active_user


router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizResponse:
    """Create a new quiz."""
    # Verify journey exists and belongs to user

    if quiz_data.journey_id:
        journey_repo = JourneyRepositoryImpl(db)
        journey_use_cases = JourneyUseCases(journey_repo)
        journey = await journey_use_cases.get_journey(quiz_data.journey_id)

        if not journey:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found"
            )

        if journey.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create quiz in this journey",
            )

    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)

    quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        journey_id=quiz_data.journey_id if quiz_data.journey_id else None,
    )

    created_quiz = await quiz_use_cases.create_quiz(quiz)

    questions = quiz_data.questions or []
    created_questions = []

    if questions:
        question_repo = QuestionRepositoryImpl(db)
        question_use_cases = QuestionUseCases(question_repo)
        for question in questions:
            if question.question_id:
                pass

            created_question = await question_use_cases.create_question(
                Question(
                    text=question.text,
                    options=question.options,
                    correct_answer=question.correct_answer,
                    quiz_id=created_quiz.id,
                )
            )

            if created_question:
                created_questions.append(created_question)

    return QuizResponse(
        id=created_quiz.id,
        title=created_quiz.title,
        description=created_quiz.description,
        questions=created_questions,
        journey_id=created_quiz.journey_id,
        created_at=created_quiz.created_at,
        updated_at=created_quiz.updated_at,
    )


@router.get("/journey/{journey_id}", response_model=List[QuizResponse])
async def get_quizzes_by_journey(
    journey_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[QuizResponse]:
    """Get all quizzes for a specific journey."""
    # Verify journey exists and belongs to user
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
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

    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)

    quizzes = await quiz_use_cases.get_journey_quizzes(
        journey_id=journey_id, skip=skip, limit=limit
    )
    return [
        QuizResponse(
            id=quiz.id,
            title=quiz.title,
            description=quiz.description,
            journey_id=quiz.journey_id,
            created_at=quiz.created_at,
            updated_at=quiz.updated_at,
        )
        for quiz in quizzes
    ]


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizResponse:
    """Get a quiz by ID."""
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)

    quiz = await quiz_use_cases.get_quiz(
        quiz_id, 
        include_questions=True
    )
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    return QuizResponse(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        journey_id=quiz.journey_id,
        created_at=quiz.created_at,
        updated_at=quiz.updated_at,
        questions=quiz.questions or [],
    )


@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: UUID,
    quiz_data: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizResponse:
    """Update a quiz."""
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)

    quiz = await quiz_use_cases.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    # Verify journey belongs to user
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this quiz",
        )

    # Update fields if provided
    if quiz_data.title is not None:
        quiz.title = quiz_data.title
    if quiz_data.description is not None:
        quiz.description = quiz_data.description
    if quiz_data.journey_id is not None:
        # Verify new journey exists and belongs to user
        new_journey = await journey_use_cases.get_journey(quiz_data.journey_id)
        if not new_journey or new_journey.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to move quiz to this journey",
            )
        quiz.journey_id = quiz_data.journey_id

    try:
        updated_quiz = await quiz_use_cases.update_quiz(quiz)
        return QuizResponse(
            id=updated_quiz.id,
            title=updated_quiz.title,
            description=updated_quiz.description,
            journey_id=updated_quiz.journey_id,
            created_at=updated_quiz.created_at,
            updated_at=updated_quiz.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a quiz."""
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)

    quiz = await quiz_use_cases.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    # Verify journey belongs to user
    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this quiz",
        )

    try:
        await quiz_use_cases.delete_quiz(quiz_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
