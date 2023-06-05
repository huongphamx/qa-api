from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(settings.ASYNC_SQLALCHEMY_DATABASE_URI)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
