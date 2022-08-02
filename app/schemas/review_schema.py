from datetime import datetime
from pydantic import BaseModel, Field
from ..schemas.user_schema import UserOut


class ReviewBase(BaseModel):

    user: UserOut
    user_id: int
    travely_id: int
    review: str

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
