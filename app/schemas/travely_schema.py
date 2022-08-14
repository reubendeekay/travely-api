from curses.ascii import isdigit
from datetime import datetime
from typing import List, Literal, Union


from pydantic import BaseModel, Field, root_validator, parse_obj_as
from ..database import Base

from app.schemas.review_schema import ReviewBase
from . import user_schema, room_schema


class QueryFilter(BaseModel):
    field: str

    value: Union[str, int, datetime, float, list, dict]

    @root_validator
    def validate_value(cls, values):

        operator, value = values.get("operator"), values.get("value")

        # is int
        if not value.isdigit() and operator in {"<=", "<", ">", ">="}:
            raise ValueError("Not Found")

    def get_sqlalchemy_filter(model: Base, self):
        field = getattr(model, self.field)
        value = self.value

        if isinstance(value, str):
            if value.isdigit():
                value < float(value)
            else:
                value = value.lower()

        return field.contains(value)


class RulesBase(BaseModel):
    id: int
    check_in: datetime
    check_out: datetime
    pets: bool = False
    smoking: bool = False
    parties: bool = False
    travely_id: int

    class Config:
        orm_mode = True


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
    category = str

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
    rules: List[RulesBase] = []

    createdAt: datetime = Field(
        default_factory=datetime.now, alias="createdAt")

    class Config:
        orm_mode = True


class TravelyCreate(TravelyBase):
    pass
