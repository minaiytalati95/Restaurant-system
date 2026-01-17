from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from datetime import datetime

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def add_to_order(self, visit_id: int, customer_id: int, items: list):
        """
        items: list of dicts with {'item_id': int, 'quantity': int}
        Consolidates items into a single order per visit.
        """
        # Check if an order already exists for this visit
        order = self.db.query(Order).filter(Order.visit_id == visit_id).first()
        
        if not order:
            order = Order(
                customer_id=customer_id,
                visit_id=visit_id,
                order_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            self.db.add(order)
            self.db.flush() # Get order_id
        
        for item_data in items:
            item_id = item_data['item_id']
            quantity = item_data['quantity']
            
            # Check if this item is already in the order
            order_item = self.db.query(OrderItem).filter(
                OrderItem.order_id == order.order_id,
                OrderItem.item_id == item_id
            ).first()
            
            if order_item:
                # Consolidate quantity
                order_item.quantity += quantity
            else:
                # Add new item
                order_item = OrderItem(
                    order_id=order.order_id,
                    item_id=item_id,
                    quantity=quantity
                )
                self.db.add(order_item)
        
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_visit(self, visit_id: int):
        return self.db.query(Order).filter(Order.visit_id == visit_id).first()

    def get_order_items(self, order_id: int):
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    def get_customer_orders(self, customer_id: int):
        return self.db.query(Order).filter(Order.customer_id == customer_id).all()