from datetime import datetime
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    id: int
    user_name: str
    user_id: str
    review: str
    rating: int
    created_at: datetime

    class Config:
        orm_mode = True
