from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas, crud
from app.apis.deps import get_current_lecturer, get_current_head_lecturer, get_async_db
from app.core.paginate import PagedResponseSchema, PageParams, paginate

router = APIRouter()


@router.get("/me", response_model=schemas.Lecturer)
async def get_user_me(
    current_lecturer: models.Lecturer = Depends(get_current_lecturer),
):
    return current_lecturer


@router.get(
    "/",
    response_model=PagedResponseSchema[schemas.Lecturer],
    dependencies=[Depends(get_current_head_lecturer)],
)
async def read_lecturers(
    db: AsyncSession = Depends(get_async_db),
    page_params: PageParams = Depends(),
):
    query = crud.lecturer.query_get_multi()
    return await paginate(db, query, page_params, schemas.Lecturer)


@router.post(
    "/",
    response_model=schemas.Lecturer,
    dependencies=[Depends(get_current_head_lecturer)],
)
async def create_new_lecturer(
    db: AsyncSession = Depends(get_async_db), *, obj_in: schemas.LecturerCreate
):
    db_obj = await crud.lecturer.get_by_email(db, email=obj_in.email)
    if db_obj is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="LECTURER_EXISTED"
        )
    return await crud.lecturer.create(db, obj_in)
