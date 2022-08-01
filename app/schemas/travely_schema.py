from datetime import datetime


from pydantic import BaseModel, Field

from app.schemas.review_schema import ReviewBase


class TravelyBase(BaseModel):

    images: list = []
    name: str

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

    bookings: int = 0

    class Config:
        orm_mode = True


class TravelyOut(TravelyBase):
    id: int
    owner_id: int

    created_at: datetime


class TravelyDetails(TravelyBase):
    id: int
    # reviews: List[ReviewBase] = []

    createdAt: datetime = Field(
        default_factory=datetime.now, alias="createdAt")


class TravelyCreate(TravelyBase):

    pass
