from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from uuid import UUID

from ...application.use_cases import QuestionUseCases, QuizUseCases, JourneyUseCases
from ...application.use_cases.question_use_cases import get_question_use_cases
from ...application.use_cases.quiz_use_cases import get_quiz_use_cases
from ...application.use_cases.journey_use_cases import get_journey_use_cases
from ...domain.entities.question import Question
from ...domain.entities.user import User
from ..schemas import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuestionResponseWithAnswer,
    AnswerCheck,
    AnswerResult,
    OptionAnswerResponse,
)
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/questions", tags=["questions"])
QuestionUseCasesDep = Annotated[QuestionUseCases, Depends(get_question_use_cases)]
QuizUseCasesDep = Annotated[QuizUseCases, Depends(get_quiz_use_cases)]
JourneyUseCasesDep = Annotated[JourneyUseCases, Depends(get_journey_use_cases)]


@router.post("/batch", response_model=List[QuestionResponseWithAnswer], status_code=status.HTTP_201_CREATED)
async def create_questions_batch(
    questions_data: List[QuestionCreate],
    quiz_use_cases: QuizUseCasesDep,
    question_use_cases: QuestionUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> List[QuestionResponseWithAnswer]:
    """Create multiple questions in a batch."""
    created_questions = []
    for question_data in questions_data:
        question_response = await create_question(
            question_data=question_data,
            quiz_use_cases=quiz_use_cases,
            question_use_cases=question_use_cases,
            current_user=current_user,
        )
        created_questions.append(question_response.dict())
    return created_questions


@router.post("/", response_model=QuestionResponseWithAnswer, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    quiz_use_cases: QuizUseCasesDep,
    question_use_cases: QuestionUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponseWithAnswer:
    """Create a new question."""
    quiz = await quiz_use_cases.get_quiz(question_data.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

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
            options=[
                OptionAnswerResponse(
                    id=opt.id,
                    reference_id=opt.reference_id,
                    text=opt.text,
                    order=opt.order,
                    is_correct=opt.is_correct,
                )
                for opt in created_question.options
            ],
            correct_answer=created_question.correct_answer,
            created_at=created_question.created_at,
            updated_at=created_question.updated_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/quiz", response_model=List[QuestionResponse])
async def get_questions_by_quiz(
    quiz_id: UUID,
    skip: int = 0,
    limit: int = 100,
    quiz_use_cases: QuizUseCasesDep = ...,
    question_use_cases: QuestionUseCasesDep = ...,
) -> List[QuestionResponse]:
    """Get all questions for a specific quiz (without correct answers)."""
    quiz = await quiz_use_cases.get_quiz(quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    questions = await question_use_cases.get_quiz_questions(
        quiz_id=quiz_id, skip=skip, limit=limit
    )
    return [
        QuestionResponse(
            id=question.id,
            text=question.text,
            quiz_id=question.quiz_id,
            options=[
                OptionAnswerResponse(
                    id=opt.id,
                    reference_id=opt.reference_id,
                    text=opt.text,
                    order=opt.order,
                    is_correct=opt.is_correct,
                )
                for opt in question.options
            ],
            created_at=question.created_at,
            updated_at=question.updated_at,
        )
        for question in questions
    ]


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: UUID,
    question_use_cases: QuestionUseCasesDep,
    quiz_use_cases: QuizUseCasesDep,
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponse:
    """Get a question by ID (without correct answer)."""
    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    if quiz.journey_id:
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
        options=[
            OptionAnswerResponse(
                id=opt.id,
                reference_id=opt.reference_id,
                text=opt.text,
                order=opt.order,
                is_correct=opt.is_correct,
            )
            for opt in question.options
        ],
        created_at=question.created_at,
        updated_at=question.updated_at,
    )


@router.put("/{question_id}", response_model=QuestionResponseWithAnswer)
async def update_question(
    question_id: UUID,
    question_data: QuestionUpdate,
    question_use_cases: QuestionUseCasesDep,
    quiz_use_cases: QuizUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> QuestionResponseWithAnswer:
    """Update a question."""
    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    try:
        updated_question = await question_use_cases.update_question(
            Question(
                id=question.id,
                text=question_data.text if question_data.text is not None else question.text,
                quiz_id=question.quiz_id,
                options=question_data.options if question_data.options is not None else question.options,
                correct_answer=question_data.correct_answer if question_data.correct_answer is not None else question.correct_answer,
            )
        )

        return QuestionResponseWithAnswer(
            id=updated_question.id,
            text=updated_question.text,
            quiz_id=updated_question.quiz_id,
            options=[
                OptionAnswerResponse(
                    id=opt.id,
                    reference_id=opt.reference_id,
                    text=opt.text,
                    order=opt.order,
                    is_correct=opt.is_correct,
                )
                for opt in updated_question.options
            ],
            correct_answer=updated_question.correct_answer,
            created_at=updated_question.created_at,
            updated_at=updated_question.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: UUID,
    question_use_cases: QuestionUseCasesDep,
    quiz_use_cases: QuizUseCasesDep,
    journey_use_cases: JourneyUseCasesDep,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete a question."""
    question = await question_use_cases.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    quiz = await quiz_use_cases.get_quiz(question.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    if quiz.journey_id:
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
