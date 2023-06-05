from pydantic import BaseModel


class LecturerBase(BaseModel):
    email: str | None


class LecturerCreate(LecturerBase):
    email: str
    password: str


class LecturerUpdate(LecturerBase):
    password: str | None
