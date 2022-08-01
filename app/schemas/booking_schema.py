from datetime import datetime
from pydantic import BaseModel


class BookingBase(BaseModel):

    room_id: int
    guests: int
    check_in: datetime
    check_out: datetime

    status: str = "pending"

    amount: float

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    user_id: int
    created_at: datetime
