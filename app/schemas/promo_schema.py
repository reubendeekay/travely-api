from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class PromoType(str, Enum):
    link = "link"
    travely = "travely"
    destination = "destination"
    user = "user"


class PromoBase(BaseModel):
    cover_image: str
    name: str
    description: float
    user_id: int
    type: PromoType
    action: str
    views: int = 0
    clicks: int = 0

    class Config:
        orm_mode = True


class PromoOut(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    cover_image: str

    class Config:
        orm_mode = True


class PromoDetails(PromoBase):
    id: int
    created_at: datetime
