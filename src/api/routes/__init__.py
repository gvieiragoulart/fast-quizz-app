from .auth import router as auth_router
from .users import router as users_router
from .journeys import router as journeys_router
from .quizzes import router as quizzes_router
from .questions import router as questions_router

__all__ = [
    "auth_router",
    "users_router",
    "journeys_router",
    "quizzes_router",
    "questions_router",
]
