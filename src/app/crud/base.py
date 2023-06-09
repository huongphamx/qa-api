from typing import Any, Generic, TypeVar, Type

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_model import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any):
        return await db.scalar(select(self.model).where(self.model.id == id))

    def query_get_multi(self):
        query = select(self.model).order_by(self.model.id.desc())
        # query = select(self.model).order_by(self.model.created_at.desc())
        return query

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: ModelType) -> ModelType:
        await db.delete(db_obj)
        await db.commit()
        return db_obj
