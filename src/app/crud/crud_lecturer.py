from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models import Lecturer
from app.schemas import LecturerCreate, LecturerUpdate


class CRUDLecturer(CRUDBase[Lecturer, LecturerCreate, LecturerUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str):
        return await db.scalar(select(Lecturer).where(Lecturer.email == email))

    async def authenticate(self, db: AsyncSession, email: str, password: str):
        lecturer = await self.get_by_email(db, email=email)
        if not lecturer:
            return None
        if not verify_password(password, lecturer.hashed_password):
            return None
        return lecturer


lecturer = CRUDLecturer(Lecturer)
