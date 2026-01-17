from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.customer_handler import CustomerService
from pydantic import BaseModel
from typing import Optional

api = APIRouter()

class CustomerCheckIn(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    city: Optional[str] = None
    num_people: int = 1
    reservation_made: bool = False

@api.post("/customers/check-in")
def check_in(data: CustomerCheckIn, db: Session = Depends(get_db)):
    customer_service = CustomerService(db)
    customer, visitation = customer_service.check_in(
        name=data.name,
        phone=data.phone,
        email=data.email,
        city=data.city,
        num_people=data.num_people,
        reservation_made=data.reservation_made
    )
    return {
        "customer": customer,
        "visitation": visitation
    }

@api.get("/customers/phone/{phone}")
def get_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    customer_service = CustomerService(db)
    customer = customer_service.get_customer_by_phone(phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
