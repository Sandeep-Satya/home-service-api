cat > ~/home-services-api/main.py << 'EOF'
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import engine, Base, get_db
import models
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Services API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    user_id: Optional[int] = None
    class Config:
        from_attributes = True

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str

# ---------- Startup ----------
@app.on_event("startup")
def seed_services():
    db = next(get_db())
    if db.query(models.Service).count() == 0:
        for name in ["AC Technician", "Plumber", "Electrician", "Painter", "Daily Wage Worker"]:
            db.add(models.Service(name=name))
        db.commit()
    db.close()

# ---------- Auth Routes ----------
@app.post("/auth/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        name=req.name,
        email=req.email,
        password=auth.hash_password(req.password),
        role="customer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth.create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "role": user.role, "name": user.name}

@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not auth.verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "role": user.role, "name": user.name}

# ---------- Routes ----------
@app.get("/")
def read_root():
    return {"message": "Welcome to the Home Services API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/services", response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingRequest, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    service = db.query(models.Service).filter(models.Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=400, detail=f"Service with id {booking.service_id} does not exist")
    new_booking = models.Booking(
        customer_name=booking.customer_name,
        phone_number=booking.phone_number,
        address=booking.address,
        service_id=booking.service_id,
        preferred_time=booking.preferred_time,
        status="pending",
        user_id=current_user.id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role == "admin":
        return db.query(models.Booking).all()
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking with id {booking_id} not found")
    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return booking
EOF
