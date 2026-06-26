from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import engine, Base, get_db
import models

# This creates the actual table in Postgres if it doesn't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Services API")

# Request shape — what the customer sends
class BookingRequest(BaseModel):
    customer_name: str
    phone_number: str
    address: str
    service_type: str
    preferred_time: str

# Response shape — what we send back
class BookingResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    address: str
    service_type: str
    preferred_time: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Home Services API"}

@app.get("/services")
def get_services():
    services = [
        {"id": 1, "name": "AC Technician"},
        {"id": 2, "name": "Plumber"},
        {"id": 3, "name": "Electrician"},
        {"id": 4, "name": "Painter"},
        {"id": 5, "name": "Daily Wage Worker"},
    ]
    return {"services": services}

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingRequest, db: Session = Depends(get_db)):
    new_booking = models.Booking(
        customer_name=booking.customer_name,
        phone_number=booking.phone_number,
        address=booking.address,
        service_type=booking.service_type,
        preferred_time=booking.preferred_time,
        status="pending"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()
