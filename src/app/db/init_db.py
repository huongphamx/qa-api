from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas import LecturerCreate


async def init_db(db: AsyncSession):
    """
    Create head lecturer. Will ask for email and password
    """
    lecturer = await crud.lecturer.get_by_email(db, email=settings.FIRST_SUPERUSER)

    if not lecturer:
        obj_in = LecturerCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_head=True,
            fullname="Admin",
        )

        await crud.lecturer.create(db, obj_in)
