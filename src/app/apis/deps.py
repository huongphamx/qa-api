from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app import crud
from app.db.session import async_session
from app.models import Lecturer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login-token")

ALGORITHM = "HS256"


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_lecturer(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        lecturer_id = payload.get("sub")
        if lecturer_id is None:
            raise credentials_exception
    except jwt.DecodeError:
        raise credentials_exception
    lecturer = await crud.lecturer.get(db=db, id=int(lecturer_id))
    if lecturer is None:
        raise credentials_exception
    return lecturer


async def get_current_head_lecturer(
    current_lecturer: Lecturer = Depends(get_current_lecturer),
):
    if not current_lecturer.is_head:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    return current_lecturer
