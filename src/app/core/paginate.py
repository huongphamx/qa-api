from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class PageParams(BaseModel):
    """Request query params for paginated API."""

    page: int = Field(default=0, ge=0)
    size: int = Field(default=10, ge=1, le=100)


T = TypeVar("T", bound=BaseModel)


class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]


async def paginate(
    db: AsyncSession, query, page_params: PageParams, ResponseSchema: T
) -> PagedResponseSchema[T]:
    """Paginate the query."""

    paginated_query = (
        (
            await db.scalars(
                query.offset(page_params.page * page_params.size).limit(
                    page_params.size
                )
            )
        )
        .unique()
        .all()
    )

    return PagedResponseSchema(
        total=await db.scalar(select(func.count()).select_from(query)),  # type: ignore
        page=page_params.page,
        size=page_params.size,
        results=[ResponseSchema.from_orm(item) for item in paginated_query],
    )
