from sqlalchemy.sql.expression import text

from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, Float, Index, Computed
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import TIMESTAMP


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    last_seen = Column(TIMESTAMP(timezone=True),
                       server_default=text('NOW()'), nullable=False)
    phone_number = Column(String)
    profile_pic = Column(String)
    push_token = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)


class TravelyModel(Base):
    __tablename__ = "travelies"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("UserModel")
    name = Column(String)
    images = Column(ARRAY(String))
    price = Column(Integer)
    description = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)
    address = Column(String)
    ammenities = Column(String)
    category = Column(String)
    tags = Column(ARRAY(String))
    views = Column(Integer)
    rating = Column(Integer)
    bookings = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    ammenities = Column(ARRAY(String))


class RoomModel(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    travely_id = Column(Integer, ForeignKey(
        'travelies.id', ondelete="CASCADE"), nullable=False)
    name = Column(String)
    images = Column(ARRAY(String))
    price = Column(Float)
    description = Column(String)
    rating = Column(Integer)
    bookings = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)


class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    room_id = Column(Integer, ForeignKey(
        "rooms.id", ondelete="CASCADE"), nullable=False)
    guests = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)

    status = Column(String)
    check_in = Column(TIMESTAMP(timezone=True),
                      server_default=text('NOW()'), nullable=False)
    check_out = Column(TIMESTAMP(timezone=True),
                       server_default=text('NOW()'), nullable=False)
    amount = Column(Float)


class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(Integer, ForeignKey(
        "bookings.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float)
    transaction_id = Column(String)
    payment_method = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
