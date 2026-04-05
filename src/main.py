from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.routes import (
    auth_router,
    users_router,
    journeys_router,
    quizzes_router,
    questions_router,
    results_router,
)
from .infrastructure.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Quiz App",
    description="A quiz application with Clean Architecture, OAuth2, and CRUD operations",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(journeys_router)
app.include_router(quizzes_router)
app.include_router(questions_router)
app.include_router(results_router)

# Serve uploaded files
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI Quiz App",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
