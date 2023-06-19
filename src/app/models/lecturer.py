import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Lecturer(Base):
    __tablename__ = "lecturer"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str]
    is_head: Mapped[bool] = mapped_column(default=False)
    fullname: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=False, nullable=True)
    last_invitation_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
