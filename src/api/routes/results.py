from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from uuid import UUID, uuid4

from ...application.use_cases import QuizUseCases, ResultUseCases
from ...application.use_cases.quiz_use_cases import get_quiz_use_cases
from ...application.use_cases.result_use_cases import get_result_use_cases
from ...domain.entities.results import Result
from ...domain.entities.user import User
from ..schemas.results import ResultCreate, ResultResponse, ResultsListResponse
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/api/results", tags=["results"])
QuizUseCasesDep = Annotated[QuizUseCases, Depends(get_quiz_use_cases)]
ResultUseCasesDep = Annotated[ResultUseCases, Depends(get_result_use_cases)]


@router.get("/me", response_model=ResultsListResponse)
async def get_my_results(
    skip: int = 0,
    limit: int = 100,
    result_use_cases: ResultUseCasesDep = ...,
    current_user: User = Depends(get_current_active_user),
) -> ResultsListResponse:
    """Get all quiz results for the current user."""
    results = await result_use_cases.get_results_by_user(
        user_id=current_user.id, skip=skip, limit=limit
    )
    items = [
        ResultResponse(
            id=r.id,
            user_id=r.user_id,
            respondent_name=r.respondent_name,
            quiz_id=r.quiz_id,
            score=r.score,
            total_questions=r.total_questions,
            taken_at=r.taken_at,
        )
        for r in results
    ]
    return ResultsListResponse(items=items, total=len(items))


@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(
    result_data: ResultCreate,
    quiz_use_cases: QuizUseCasesDep,
    result_use_cases: ResultUseCasesDep,
) -> ResultResponse:
    """Submit a quiz result."""
    quiz = await quiz_use_cases.get_quiz(result_data.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    result = Result(
        id=uuid4(),
        user_id=result_data.user_id,
        respondent_name=result_data.respondent_name,
        quiz_id=result_data.quiz_id,
        score=result_data.score,
        total_questions=result_data.total_questions,
    )

    created = await result_use_cases.create_result(result)
    return ResultResponse(
        id=created.id,
        user_id=created.user_id,
        respondent_name=created.respondent_name,
        quiz_id=created.quiz_id,
        score=created.score,
        total_questions=created.total_questions,
        taken_at=created.taken_at,
    )


@router.get("/quiz/{quiz_id}", response_model=ResultsListResponse)
async def get_results_by_quiz(
    quiz_id: UUID,
    skip: int = 0,
    limit: int = 100,
    quiz_use_cases: QuizUseCasesDep = ...,
    result_use_cases: ResultUseCasesDep = ...,
) -> ResultsListResponse:
    """Get all results for a specific quiz."""
    quiz = await quiz_use_cases.get_quiz(quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    results = await result_use_cases.get_results_by_quiz(quiz_id, skip=skip, limit=limit)
    items = [
        ResultResponse(
            id=r.id,
            user_id=r.user_id,
            respondent_name=r.respondent_name,
            quiz_id=r.quiz_id,
            score=r.score,
            total_questions=r.total_questions,
            taken_at=r.taken_at,
        )
        for r in results
    ]
    return ResultsListResponse(items=items, total=len(items))
