from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_handler import OrderService
from pydantic import BaseModel
from typing import List

api = APIRouter()

class OrderItemSchema(BaseModel):
    item_id: int
    quantity: int

class OrderAdd(BaseModel):
    customer_id: int
    visit_id: int
    items: List[OrderItemSchema]

@api.post("/orders/add")
def add_to_order(data: OrderAdd, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    items_list = [item.dict() for item in data.items]
    order = order_service.add_to_order(data.visit_id, data.customer_id, items_list)
    return order

@api.get("/orders/visit/{visit_id}")
def get_order_by_visit(visit_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    order = order_service.get_order_by_visit(visit_id)
    if not order:
        raise HTTPException(status_code=404, detail="No order found for this visit")
    items = order_service.get_order_items(order.order_id)
    return {
        "order": order,
        "items": items
    }

@api.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_customer_orders(customer_id)
