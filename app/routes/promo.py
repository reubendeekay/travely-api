from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import promo_schema
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db


router = APIRouter(tags=["Promotions"], prefix="/promos")


@router.get("/", response_model=List[promo_schema.PromoOut], status_code=status.HTTP_200_OK)
async def get_promos(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 50, skip: int = 0, search: str = None):
    return db.query(models.PromotionModel).offset(skip).limit(limit).all()


@router.get("/{promo_id}", response_model=promo_schema.PromoDetails, status_code=status.HTTP_200_OK)
async def get_promo(promo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    promo = db.query(models.PromotionModel).filter(
        models.PromotionModel.id == promo_id).first()
    if promo is None:
        raise HTTPException(status_code=404, detail="Promo not found")
    return promo


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=promo_schema.PromoDetails)
async def create_promo(promo: promo_schema.PromoBase, db: Session = Depends(get_db)):
    # Check if promo already exists
    promo_exists = db.query(models.PromotionModel).filter(
        models.PromotionModel.name == promo.name).first()
    if promo_exists is not None:
        raise HTTPException(
            status_code=400, detail="Promo already exists")

    new_promo = models.PromotionModel(**promo.dict())
    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)

    return new_promo


@router.delete("/{promo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_promo(promo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    promo = db.query(models.PromotionModel).filter(
        models.PromotionModel.id == promo_id).first()
    if promo is None:
        raise HTTPException(status_code=404, detail="Promo not found")
    db.delete(promo)
    db.commit()
    return None


@router.put("/{promo_id}", response_model=promo_schema.PromoDetails, status_code=status.HTTP_200_OK)
async def update_promo(promo_id: int, promo: promo_schema.PromoBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    promo_exists = db.query(models.PromotionModel).filter(
        models.PromotionModel.id == promo_id)
    if promo_exists.first() is None:
        raise HTTPException(status_code=404, detail="Promo not found")

    promo_exists.update(promo.dict())

    db.commit()

    return promo_exists.first()
