from fastapi import APIRouter

from .endpoints import auth, lecturer


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(lecturer.router, prefix="/lecturers", tags=["lecturers"])
