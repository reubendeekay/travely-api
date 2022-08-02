from pydantic import BaseModel


class FavoriteBase(BaseModel):
    id: int
    user_id: int
    travely_id: int

    class Config:
        orm_mode = True
