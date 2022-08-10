
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from ..schemas import travely_schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..oauth2 import get_current_user


router = APIRouter(tags=["Travelies"], prefix="/travelies",)

# GET TRAVELIES


@router.get("/", response_model=List[travely_schema.TravelyOut], status_code=status.HTTP_200_OK)
async def get_travelies(current_user=Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50, skip: int = 0, search: str = "", category: str = "",):
    return db.query(models.TravelyModel).filter(models.TravelyModel.name.contains(search) | models.TravelyModel.category.contains(category)).offset(skip).limit(limit).all()


# GET A SPECIFIC TRAVELY

@router.get("/{travely_id}", response_model=travely_schema.TravelyDetails, status_code=status.HTTP_200_OK)
async def get_travely(travely_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id).first()
    if travely is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    return travely


# CREATE A TRAVELY

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=travely_schema.TravelyOut)
async def create_travely(travely: travely_schema.TravelyCreate, status_code=status.HTTP_201_CREATED, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    new_travely = models.TravelyModel(
        owner_id=current_user.user_id, **travely.dict())
    db.add(new_travely)
    db.commit()
    db.refresh(new_travely)
    return new_travely


# DELETE A TRAVELY
@router.delete("/{travely_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_travely(travely_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id).delete(synchronize_session=False)
    db.commit()
    if travely is None:
        raise HTTPException(status_code=404, detail="Travely not found")


# UPDATE A TRAVELY
@router.put("/{travely_id}", status_code=status.HTTP_200_OK, response_model=travely_schema.TravelyOut)
async def update_travely(travely_id: str, travely: travely_schema.TravelyCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely_to_update = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id)
    if travely_to_update.first() is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    travely_to_update.update(travely.dict())
    db.commit()
    db.refresh(travely_to_update.first())
    return travely_to_update.first()
