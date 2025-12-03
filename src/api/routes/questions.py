from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ...infrastructure.database import get_db
from ...infrastructure.repositories import (
    QuestionRepositoryImpl,
    QuizRepositoryImpl,
    JourneyRepositoryImpl,
)
from ...application.use_cases import QuestionUseCases, QuizUseCases, JourneyUseCases
from ...domain.entities.question import Question
from ...domain.entities.user import User
from ..schemas import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuestionResponseWithAnswer,
    AnswerCheck,
    AnswerResult,
)
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponseWithAnswer, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponseWithAnswer:
    """Create a new question."""
    # Verify quiz exists and belongs to user
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(question_data.quiz_id)

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
            detail="Not authorized to create question in this quiz",
        )

    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    question = Question(
        text=question_data.text,
        quiz_id=question_data.quiz_id,
        options=question_data.options,
        correct_answer=question_data.correct_answer,
    )

    try:
        created_question = await question_use_cases.create_question(question)
        return QuestionResponseWithAnswer(
            id=created_question.id,
            text=created_question.text,
            quiz_id=created_question.quiz_id,
            options=created_question.options,
            correct_answer=created_question.correct_answer,
            created_at=created_question.created_at,
            updated_at=created_question.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/quiz/{quiz_id}", response_model=List[QuestionResponse])
async def get_questions_by_quiz(
    quiz_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[QuestionResponse]:
    """Get all questions for a specific quiz (without correct answers)."""
    # Verify quiz exists and belongs to user
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
            detail="Not authorized to access this quiz",
        )

    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    questions = await question_use_cases.get_quiz_questions(
        quiz_id=quiz_id, skip=skip, limit=limit
    )
    return [
        QuestionResponse(
            id=question.id,
            text=question.text,
            quiz_id=question.quiz_id,
            options=question.options,
            created_at=question.created_at,
            updated_at=question.updated_at,
        )
        for question in questions
    ]


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponse:
    """Get a question by ID (without correct answer)."""
    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    # Verify quiz and journey belong to user
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this question",
        )

    return QuestionResponse(
        id=question.id,
        text=question.text,
        quiz_id=question.quiz_id,
        options=question.options,
        created_at=question.created_at,
        updated_at=question.updated_at,
    )


@router.post("/{question_id}/check", response_model=AnswerResult)
async def check_answer(
    question_id: UUID,
    answer_data: AnswerCheck,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AnswerResult:
    """Check if an answer is correct for a question."""
    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    # Verify quiz and journey belong to user
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this question",
        )

    is_correct = question.is_correct(answer_data.answer)
    return AnswerResult(
        is_correct=is_correct,
        correct_answer=question.correct_answer if not is_correct else None,
    )


@router.put("/{question_id}", response_model=QuestionResponseWithAnswer)
async def update_question(
    question_id: UUID,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponseWithAnswer:
    """Update a question."""
    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    # Verify quiz and journey belong to user
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this question",
        )

    # Update fields if provided
    if question_data.text is not None:
        question.text = question_data.text
    if question_data.options is not None:
        question.options = question_data.options
    if question_data.correct_answer is not None:
        question.correct_answer = question_data.correct_answer
    if question_data.quiz_id is not None:
        # Verify new quiz exists and belongs to user
        new_quiz = await quiz_use_cases.get_quiz(question_data.quiz_id)
        if not new_quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="New quiz not found"
            )
        new_journey = await journey_use_cases.get_journey(new_quiz.journey_id)
        if not new_journey or new_journey.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to move question to this quiz",
            )
        question.quiz_id = question_data.quiz_id

    try:
        updated_question = await question_use_cases.update_question(question)
        return QuestionResponseWithAnswer(
            id=updated_question.id,
            text=updated_question.text,
            quiz_id=updated_question.quiz_id,
            options=updated_question.options,
            correct_answer=updated_question.correct_answer,
            created_at=updated_question.created_at,
            updated_at=updated_question.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a question."""
    question_repo = QuestionRepositoryImpl(db)
    question_use_cases = QuestionUseCases(question_repo)

    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    # Verify quiz and journey belong to user
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    journey_repo = JourneyRepositoryImpl(db)
    journey_use_cases = JourneyUseCases(journey_repo)
    journey = await journey_use_cases.get_journey(quiz.journey_id)

    if not journey or journey.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this question",
        )

    try:
        await question_use_cases.delete_question(question_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
