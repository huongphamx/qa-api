from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, get_password_hash
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

    async def create(self, db: AsyncSession, obj_in: LecturerCreate):
        db_obj = Lecturer(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            fullname=obj_in.fullname,
            is_head=obj_in.is_head,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


lecturer = CRUDLecturer(Lecturer)
