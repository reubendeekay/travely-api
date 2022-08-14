
from ..oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, Body, Depends,  HTTPException, status
from ..schemas import user_schema
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

from ..oauth2 import hash_password
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    tags=["User"],
    prefix="/users",
)


# HELPER FUNCTIONS
def add_recent_search(search: user_schema.RecentSearch, db: Session = Depends(get_db),  current_user=Depends(get_current_user)):

    new_search = models.RecentSearchModel(
        user_id=current_user.user_id,
        name=search
    )
    db.add(new_search)


# ROUTES

# GET  USERS
@router.get("/", response_model=List[user_schema.UserOut], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 50, skip: int = 0, search: str = None):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


# GET A SPECIFIC USER

@router.get("/{user_id}", response_model=user_schema.UserOut, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    user = db.query(models.UserModel).filter(
        models.UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# CREATE A USER

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user_exists = db.query(models.UserModel).filter(
        models.UserModel.email == user.email).first()
    if user_exists is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user.password = hash_password(user.password)

    new_user = models.UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# # DELETE A USER


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(
        models.UserModel.id == user_id).delete(synchronize_session=False)
    db.commit()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")


# # UPDATE A USER

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=user_schema.UserOut)
async def update_user(user_id: str, user: user_schema.UserCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_exists = db.query(models.UserModel).filter(models.UserModel.id == user_id).update(
        user.dict(), synchronize_session=False)
    db.commit()
    if user_exists is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.refresh(user_exists)
    return user_exists
