from sqlalchemy import Column, Integer, String
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    category = Column(String)
    price_inr = Column(Integer)