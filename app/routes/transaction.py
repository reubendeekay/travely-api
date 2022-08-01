from fastapi import APIRouter, status, Depends, HTTPException
from .. import models
from sqlalchemy.orm import Session
from ..schemas import transaction_schema
from ..database import get_db
from ..utils import mpesa
from ..oauth2 import get_current_user

router = APIRouter(tags=["Transactions"], prefix="/transactions")


def create_transaction(transaction: transaction_schema.TransactionBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_transaction = models.TransactionModel(
        user_id=current_user.user_id, **transaction.dict())
    if(transaction.payment_method.to_lower() == 'm-pesa'):
        mpesa.pay_cb2()
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=transaction_schema.TransactionOut)
async def create_mpesa():
    await mpesa.pay_cb2()
    return {'message': 'Success'}
