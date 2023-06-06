from pydantic import BaseModel


class LecturerBase(BaseModel):
    email: str | None
    is_head: bool = False
    fullname: str | None


class LecturerCreate(LecturerBase):
    email: str
    password: str
    fullname: str


class LecturerUpdate(LecturerBase):
    password: str | None


class Lecturer(LecturerBase):
    email: str
    is_head: bool
    fullname: str

    class Config:
        orm_mode = True
