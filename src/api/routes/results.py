from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID, uuid4

from ...infrastructure.database import get_db
from ...infrastructure.repositories import QuizRepositoryImpl, ResultRepositoryImpl
from ...application.use_cases import QuizUseCases, ResultUseCases
from ...domain.entities.results import Result
from ..schemas.results import ResultCreate, ResultResponse, ResultsListResponse

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(
    result_data: ResultCreate,
    db: Session = Depends(get_db),
) -> ResultResponse:
    """Submit a quiz result."""
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(result_data.quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    result_repo = ResultRepositoryImpl(db)
    result_use_cases = ResultUseCases(result_repo)

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
    db: Session = Depends(get_db),
) -> ResultsListResponse:
    """Get all results for a specific quiz."""
    quiz_repo = QuizRepositoryImpl(db)
    quiz_use_cases = QuizUseCases(quiz_repo)
    quiz = await quiz_use_cases.get_quiz(quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    result_repo = ResultRepositoryImpl(db)
    result_use_cases = ResultUseCases(result_repo)

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
