from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    item_id = Column(Integer, ForeignKey("items.item_id"))
    quantity = Column(Integer)
