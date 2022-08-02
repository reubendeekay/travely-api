from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import destination_schema
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db


router = APIRouter(tags=["Destination"], prefix="/destinations")


@router.get("/", response_model=List[destination_schema.DesriptionOut], status_code=status.HTTP_200_OK)
async def get_destinations(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 50, skip: int = 0, search: str = None):
    return db.query(models.DestinationModel).offset(skip).limit(limit).all()


@router.get("/{destination_id}", response_model=destination_schema.DestinationOut, status_code=status.HTTP_200_OK)
async def get_destination(destination_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    destination = db.query(models.DestinationModel).filter(
        models.DestinationModel.id == destination_id).first()
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=destination_schema.DesriptionOut)
async def create_destination(destination: destination_schema.DestinationCreate, db: Session = Depends(get_db)):
    # Check if destination already exists
    destination_exists = db.query(models.DestinationModel).filter(
        models.DestinationModel.name == destination.name).first()
    if destination_exists is not None:
        raise HTTPException(
            status_code=400, detail="Destination already exists")

    new_destination = models.DestinationModel(**destination.dict())
    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)

    return new_destination


@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_destination(destination_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    destination = db.query(models.DestinationModel).filter(
        models.DestinationModel.id == destination_id).first()
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    db.delete(destination)
    db.commit()
    return destination


@router.put("/{destination_id}", status_code=status.HTTP_200_OK, response_model=destination_schema.DestinationOut)
async def update_destination(destination_id: int, destination: destination_schema.DestinationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    destination_exists = db.query(models.DestinationModel).filter(
        models.DestinationModel.id == destination_id)
    if destination_exists.first() is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    destination_exists.update(destination.dict())

    db.commit()

    return destination_exists.first()
