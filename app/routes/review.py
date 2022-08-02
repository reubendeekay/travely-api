from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from ..schemas import review_schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..oauth2 import get_current_user


router = APIRouter(tags=["Reviews"], prefix="/reviews",)


# GET REVIEWS
@router.get("/", response_model=List[review_schema.ReviewOut], status_code=status.HTTP_200_OK)
async def get_reviews(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 50, skip: int = 0, search: str = None):
    return db.query(models.ReviewModel).offset(skip).limit(limit).all()


# POST REVIEW
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=review_schema.ReviewOut)
async def create_review(review: review_schema.ReviewCreate, db: Session = Depends(get_db)):

    new_review = models.ReviewModel(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

# DELETE REVIEW


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    review = db.query(models.ReviewModel).filter(
        models.ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return review
