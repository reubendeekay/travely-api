from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import tokens, user_schema
from ..database import get_db
from .. import models
from ..oauth2 import verify_password, create_access_token
from sqlalchemy.orm import Session


router = APIRouter(tags=["Login"], prefix="/login")


@router.post("/", response_model=tokens.Token, status_code=status.HTTP_200_OK)
async def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    get_user = db.query(models.UserModel).filter(
        models.UserModel.email == user.email).first()

    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, get_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    user_id = get_user.id

    return create_access_token(data={"user_id": user_id})
