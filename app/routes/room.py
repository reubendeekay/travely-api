from typing import List

from sqlalchemy.orm import Session
from ..schemas.room_schema import RoomOut, RoomCreate
from fastapi import APIRouter, Body, Depends, HTTPException, status
from ..database import get_db
from .. import models

router = APIRouter(
    tags=["Rooms"],
    prefix="/rooms",
)

# CREATE A ROOM


@router.post("/", status_code=status.HTTP_201_CREATED, )
async def create_room(room: RoomCreate, db: Session = Depends(get_db), ):
    new_room = models.RoomModel(
        **room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# GET ALL ROOMS FOR A SPECIFIC TRAVELY
@router.get("/travely/{travely_id}", response_model=List[RoomOut], status_code=status.HTTP_200_OK)
async def get_rooms(travely_id: str, db: Session = Depends(get_db), ):
    travely = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id).first()
    if travely is None:
        raise HTTPException(status_code=404, detail="Travely not found")

    all_rooms = db.query(models.RoomModel).filter(
        models.RoomModel.travely_id == travely_id).all()
    if all_rooms is None:
        raise HTTPException(status_code=404, detail="Rooms not found")
    return all_rooms


# DELETE A ROOM
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: str, db: Session = Depends(get_db), ):
    room = db.query(models.RoomModel).filter(
        models.RoomModel.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return None

# UPDATE A ROOM


@router.put("/{room_id}", status_code=status.HTTP_200_OK)
async def update_room(room_id: str, room: RoomCreate, db: Session = Depends(get_db), ):
    room_to_update = db.query(models.RoomModel).filter(
        models.RoomModel.id == room_id)
    if room_to_update.first() is None:
        raise HTTPException(status_code=404, detail="Room not found")
    room_to_update.update(room.dict())
    db.commit()

    return room_to_update.first()
