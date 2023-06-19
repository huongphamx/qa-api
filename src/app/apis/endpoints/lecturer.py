from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import MessageSchema, MessageType
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas, crud
from app.apis.deps import get_current_lecturer, get_current_head_lecturer, get_async_db
from app.core.email_config import fm
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


# @router.post(
#     "/",
#     response_model=schemas.Lecturer,
#     dependencies=[Depends(get_current_head_lecturer)],
# )
# async def create_new_lecturer(
#     db: AsyncSession = Depends(get_async_db), *, obj_in: schemas.LecturerCreate
# ):
#     db_obj = await crud.lecturer.get_by_email(db, email=obj_in.email)
#     if db_obj is not None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="LECTURER_EXISTED"
#         )
#     return await crud.lecturer.create(db, obj_in)


@router.delete("/{lecturer_id}", response_model=schemas.Lecturer)
async def delete_lecturer(
    *, lecturer_id: int, db: AsyncSession = Depends(get_async_db)
):
    db_obj = await crud.lecturer.get(db, lecturer_id)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="LECTURER_NOT_EXISTED"
        )
    obj = await crud.lecturer.remove(db, db_obj)
    return obj


@router.post("/invite")
async def invite_lecturer(
    *,
    db: AsyncSession = Depends(get_async_db),
    invitation_data: schemas.LecturerInvitation,
    background_tasks: BackgroundTasks
):
    """
    First check if lecturer email existed
    - If email exist and lecturer is active, then raise error
    - If email exist but not active, i.e. lecturer not accept invitation
    then resend invitation email
    - If email not exist, i.e. lecturer not be invited, then
    send email and create new lecturer with is_active = False
    """
    db_obj = await crud.lecturer.get_by_email(db, email=invitation_data.email)
    if db_obj is not None and db_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="LECTURER_EXISTED"
        )

    # TODO: generate invitation token
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """  # TODO
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[invitation_data.email],
        body=html,
        subtype=MessageType.html,
    )
    if db_obj is not None and not db_obj.is_active:
        background_tasks.add_task(fm.send_message, message)

    if db_obj is None:
        background_tasks.add_task(fm.send_message, message)
        db_obj = models.Lecturer(
            email=invitation_data.email,
            is_head=False,
            is_active=False,
            hashed_password="",
            full_name="Not set",
        )
        db.add(db_obj)
        await db.commit()

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"detail": "EMAIL_SENT"}
    )


@router.post("/accept-invitation")
async def accept_invitation():
    pass
