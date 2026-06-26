from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import engine, Base, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Services API")

# ---------- Schemas ----------

class ServiceResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    customer_name: str
    phone_number: str
    address: str
    service_id: int
    preferred_time: str

class BookingResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    address: str
    service_id: int
    preferred_time: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- Startup: seed default services if table is empty ----------

@app.on_event("startup")
def seed_services():
    db = next(get_db())
    if db.query(models.Service).count() == 0:
        default_services = ["AC Technician", "Plumber", "Electrician", "Painter", "Daily Wage Worker"]
        for name in default_services:
            db.add(models.Service(name=name))
        db.commit()
    db.close()

# ---------- Routes ----------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Home Services API"}

@app.get("/services", response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingRequest, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=400, detail=f"Service with id {booking.service_id} does not exist")

    new_booking = models.Booking(
        customer_name=booking.customer_name,
        phone_number=booking.phone_number,
        address=booking.address,
        service_id=booking.service_id,
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

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking with id {booking_id} not found")
    return booking
