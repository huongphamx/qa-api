from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.apis.deps import get_async_db
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login-token", response_model=schemas.Token)
async def login(
    db: AsyncSession = Depends(get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    lecturer = await crud.lecturer.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )
    if not lecturer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="LOGIN_BAD_CREDENTIALS"
        )
    return {
        "access_token": create_access_token(lecturer.id),
        "token_type": "bearer",
    }
