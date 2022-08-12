
from datetime import datetime

from pydantic import BaseModel


class RoomBase(BaseModel):
    images: list[str] = []
    name: str
    price: float
    travely_id: str
    description: str
    rating: float = 0
    bookings: int = 0
    quantity: int = 0
    is_available: bool = True

    class Config:
        orm_mode = True


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
