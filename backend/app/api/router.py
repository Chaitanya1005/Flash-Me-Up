from fastapi import APIRouter
from app.api.endpoints import users, documents, flashcards, stats

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
