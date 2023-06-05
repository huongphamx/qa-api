from typing import Any

from pydantic import BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    SECRET_KEY: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("ASYNC_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_async_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    GMAIL_ADDRESS: EmailStr
    GMAIL_APP_PASSWORD: str
    GMAIL_PORT: int
    GMAIL_SMTP_SERVER: str
    GMAIL_FROM_NAME: str


settings = Settings()
