from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.menu_handler import Menu
from pydantic import BaseModel

api = APIRouter()

class ItemUpdate(BaseModel):
    name: str
    category: str
    price: int

class ItemCreate(BaseModel):
    name: str
    category: str
    price: int

@api.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    menu_service = Menu(db)
    return menu_service.get_all_items()

@api.get("/menu/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    menu_service = Menu(db)
    item = menu_service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@api.get("/menu/category/{category}")
def get_items_by_category(category: str, db: Session = Depends(get_db)):
    menu_service = Menu(db)
    return menu_service.get_items_by_category(category)

@api.delete("/menu/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    menu_service = Menu(db)
    success = menu_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

@api.put("/menu/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    menu_service = Menu(db)
    success = menu_service.update_item(item_id, item.name, item.category, item.price)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}

@api.post("/menu")
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    menu_service = Menu(db)
    new_item = menu_service.add_item(item.name, item.category, item.price)
    return new_item
