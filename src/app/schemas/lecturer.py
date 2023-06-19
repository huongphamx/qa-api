from pydantic import BaseModel, EmailStr


class LecturerBase(BaseModel):
    email: str | None
    is_head: bool = False
    fullname: str | None


class LecturerCreate(LecturerBase):
    email: str
    password: str
    fullname: str


class LecturerInvitation(BaseModel):
    email: EmailStr


class LecturerAcceptInvitation(BaseModel):
    token: str
    fullname: str
    email: EmailStr
    password: str


class LecturerUpdate(LecturerBase):
    password: str | None


class Lecturer(LecturerBase):
    id: int
    email: str
    is_head: bool
    is_active: bool
    fullname: str

    class Config:
        orm_mode = True
