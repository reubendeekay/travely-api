from datetime import datetime
from typing import List


from pydantic import BaseModel, Field

from app.schemas.review_schema import ReviewBase
from . import user_schema, room_schema


class TravelyBase(BaseModel):
    cover_image: str

    images: list = []
    name: str
    city: str

    description: str
    price: float
    latitude: float
    longitude: float
    address: str = None
    ammenities: list = []
    category = str
    tags: list = []
    views: int = 0
    rating: float = 0
    is_available: bool = True
    is_active: bool = True

    bookings: int = 0

    class Config:
        orm_mode = True


class TravelyOut(BaseModel):
    id: int
    owner_id: int
    cover_image: str
    name: str
    price: float
    address: str
    city: str
    rating: float
    latitude: float
    longitude: float

    created_at: datetime

    class Config:
        orm_mode = True


class TravelyDetails(TravelyBase):
    id: int
    owner_id: int
    owner: user_schema.UserOut
    rooms: List[room_schema.RoomOut]

    createdAt: datetime = Field(
        default_factory=datetime.now, alias="createdAt")

    class Config:
        orm_mode = True


class TravelyCreate(TravelyBase):
    pass
