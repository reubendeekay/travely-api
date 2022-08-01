from typing import List
from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models

from ..schemas import booking_schema


router = APIRouter(tags=["Booking"], prefix="/bookings",)


# Book a Travely
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=booking_schema.BookingOut)
async def create_booking(booking: booking_schema.BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_booking = models.BookingModel(
        user_id=current_user.user_id,  **booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# Get all bookings
@router.get("/", response_model=List[booking_schema.BookingOut], status_code=status.HTTP_200_OK)
async def get_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(models.BookingModel).all()


# Get a booking by User ID
@router.get("/user/{user_id}", response_model=List[booking_schema.BookingOut], status_code=status.HTTP_200_OK)
async def get_bookings_by_user(user_id: str, db: Session = Depends(get_db)):
    return db.query(models.BookingModel).filter(models.BookingModel.user_id == user_id).all()

# Get a booking by Travely


@router.get("/travely/{travely_id}", response_model=List[booking_schema.BookingOut], status_code=status.HTTP_200_OK)
async def get_bookings_by_travely(travely_id: str, db: Session = Depends(get_db)):
    all_rooms = db.query(models.RoomModel).filter(
        models.RoomModel.travely_id == travely_id).all()

    if all_rooms is None:
        raise HTTPException(status_code=404, detail="Rooms not found")
    for room in all_rooms:
        booking = db.query(models.BookingModel).filter(
            models.BookingModel.room_id == room.id).all()
        if booking is None:
            raise HTTPException(status_code=404, detail="Bookings not found")
        return booking


# Get a booking
@router.get("/{booking_id}", response_model=booking_schema.BookingOut, status_code=status.HTTP_200_OK)
async def get_booking(booking_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    booking = db.query(models.BookingModel).filter(
        models.BookingModel.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# Delete a booking
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    booking = db.query(models.BookingModel).filter(
        models.BookingModel.id == booking_id).delete(synchronize_session=False)
    db.commit()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")


# Update a booking
@router.put("/{booking_id}", status_code=status.HTTP_200_OK)
async def update_booking(booking_id: str, booking: booking_schema.BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    book = db.query(models.BookingModel).filter(
        models.BookingModel.id == booking_id)
    if book.first() is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    book.update(booking.dict())

    db.commit()
    db.refresh(booking)
    return booking
