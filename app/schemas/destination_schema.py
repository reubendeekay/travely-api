

from typing import List
from pydantic import BaseModel
from .travely_schema import TravelyOut


class DestinationBase(BaseModel):
    images: List[str]
    city: str
    country: str
    description: str
    bookings: int = 0
    views: int = 0

    class Config:
        orm_mode = True


class DestinationCreate(DestinationBase):
    pass


class DestinationOut(DestinationBase):
    id: int
    travelies: List[TravelyOut]
