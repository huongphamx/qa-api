from fastapi import APIRouter, Depends

from app import models, schemas
from app.apis.deps import get_current_lecturer

router = APIRouter()


@router.get("/me", response_model=schemas.Lecturer)
async def get_user_me(
    current_lecturer: models.Lecturer = Depends(get_current_lecturer),
):
    return current_lecturer
