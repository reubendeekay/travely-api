
import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):

    email: EmailStr
    full_name: str
    role: str
    is_active: bool = True

    phone_number: str
    profile_pic: str
    push_token: str = None
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    last_seen: datetime.datetime
    created_at: datetime.datetime


class UserCreate(UserBase):

    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
