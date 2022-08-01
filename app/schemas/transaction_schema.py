from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: float
    transaction_id: str
    booking_id: int
    payment_method: str

    class Config:
        orm_mode = True


class TransactionOut(TransactionBase):
    id: int
    created_at: datetime
    user_id: int
