from sqlalchemy.orm import Session
from app.models.item import Item

class Menu:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_items(self):
        return self.db.query(Item).all()

    def get_item(self, item_id: int):
        return self.db.query(Item).filter(Item.item_id == item_id).first()

    def get_items_by_category(self, category: str):
        return self.db.query(Item).filter(Item.category == category).all()

    def update_item(self, item_id: int, name: str, category: str, price: int):
        item = self.get_item(item_id)
        if item:
            item.item_name = name
            item.category = category
            item.price_inr = price
            self.db.commit()
            self.db.refresh(item)
            return True
        return False

    def delete_item(self, item_id: int):
        item = self.get_item(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def add_item(self, name: str, category: str, price: int):
        new_item = Item(item_name=name, category=category, price_inr=price)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item