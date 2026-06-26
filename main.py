from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Home Services API")

# This defines what a booking request must look like
class BookingRequest(BaseModel):
    customer_name: str
    phone_number: str
    address: str
    service_type: str
    preferred_time: str

# This defines what we send back after saving it
class BookingResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    address: str
    service_type: str
    preferred_time: str
    status: str
    created_at: str

# Temporary in-memory storage (resets when server restarts)
bookings_db = []
booking_id_counter = 1

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
def create_booking(booking: BookingRequest):
    global booking_id_counter
    new_booking = {
        "id": booking_id_counter,
        "customer_name": booking.customer_name,
        "phone_number": booking.phone_number,
        "address": booking.address,
        "service_type": booking.service_type,
        "preferred_time": booking.preferred_time,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    bookings_db.append(new_booking)
    booking_id_counter += 1
    return new_booking

@app.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings():
    return bookings_db
