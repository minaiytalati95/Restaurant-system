from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class Visitation(Base):
    __tablename__ = "visitations"

    visit_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    visit_datetime = Column(String)
    num_people = Column(Integer)
    reservation_made = Column(Boolean)
