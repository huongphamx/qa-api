from pydantic import BaseModel


class LecturerBase(BaseModel):
    email: str | None
    is_head: bool = False


class LecturerCreate(LecturerBase):
    email: str
    password: str
    fullname: str


class LecturerUpdate(LecturerBase):
    password: str | None
