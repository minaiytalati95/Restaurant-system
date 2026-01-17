from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.visitation import Visitation
from datetime import datetime

class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer_by_phone(self, phone: str):
        return self.db.query(Customer).filter(Customer.phone == phone).first()

    def get_customer_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.customer_id == customer_id).first()

    def create_customer(self, name: str, phone: str, email: str = None, city: str = None):
        new_customer = Customer(
            name=name,
            phone=phone,
            email=email,
            city=city
        )
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def check_in(self, name: str, phone: str, email: str = None, city: str = None, num_people: int = 1, reservation_made: bool = False):
        # Find or create customer
        customer = self.get_customer_by_phone(phone)
        if not customer:
            customer = Customer(
                name=name,
                phone=phone,
                email=email,
                city=city
            )
            self.db.add(customer)
            self.db.flush() # Get customer_id

        # Log visitation
        visitation = Visitation(
            customer_id=customer.customer_id,
            visit_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            num_people=num_people,
            reservation_made=reservation_made
        )
        self.db.add(visitation)
        self.db.commit()
        self.db.refresh(visitation)
        self.db.refresh(customer)
        
        return customer, visitation
