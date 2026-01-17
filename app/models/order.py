from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_datetime = Column(String)
    visit_id = Column(Integer, ForeignKey("visitations.visit_id"))
