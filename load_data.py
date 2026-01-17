import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.item import Item
from app.models.customer import Customer
from app.models.visitation import Visitation
from app.models.order import Order
from app.models.order_item import OrderItem
import os

def load_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Load Items
        if db.query(Item).count() == 0:
            print("Loading items...")
            items_df = pd.read_csv("Dataset/items.csv")
            for _, row in items_df.iterrows():
                item = Item(
                    item_name=row['item_name'],
                    category=row['category'],
                    price_inr=row['price_inr']
                )
                db.add(item)
            db.commit()
            print(f"Loaded {len(items_df)} items.")

        # Load Customers
        if db.query(Customer).count() == 0:
            print("Loading customers...")
            customers_df = pd.read_csv("Dataset/customers.csv")
            for _, row in customers_df.iterrows():
                customer = Customer(
                    name=row['name'],
                    phone=str(row['phone']),
                    email=row['email'],
                    city=row['city']
                )
                db.add(customer)
            db.commit()
            print(f"Loaded {len(customers_df)} customers.")

        # Load Visitations
        if db.query(Visitation).count() == 0:
            print("Loading visitations...")
            visitations_df = pd.read_csv("Dataset/customer_visitation_logs.csv")
            for _, row in visitations_df.iterrows():
                # We trust CSV order matches auto-increment as IDs are 1-indexed and sequential
                visitation = Visitation(
                    customer_id=row['customer_id'],
                    visit_datetime=row['visit_datetime'],
                    num_people=row['num_people'],
                    reservation_made=bool(row['reservation_made'])
                )
                db.add(visitation)
            db.commit()
            print(f"Loaded {len(visitations_df)} visitations.")

        # Load Orders
        if db.query(Order).count() == 0:
            print("Loading orders...")
            orders_df = pd.read_csv("Dataset/orders.csv")
            for _, row in orders_df.iterrows():
                order = Order(
                    customer_id=row['customer_id'],
                    order_datetime=row['order_datetime'],
                    visit_id=row['visit_id']
                )
                db.add(order)
            db.commit()
            print(f"Loaded {len(orders_df)} orders.")

        # Load Order Items
        if db.query(OrderItem).count() == 0:
            print("Loading order items (this might take a while)...")
            order_items_df = pd.read_csv("Dataset/order_items.csv")
            # Batch insert for order items as it's large
            order_items = []
            for _, row in order_items_df.iterrows():
                order_items.append(
                    OrderItem(
                        order_id=row['order_id'],
                        item_id=row['item_id'],
                        quantity=row['quantity']
                    )
                )
                if len(order_items) >= 1000:
                    db.bulk_save_objects(order_items)
                    db.commit()
                    order_items = []
            if order_items:
                db.bulk_save_objects(order_items)
                db.commit()
            print(f"Loaded {len(order_items_df)} order items.")

    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_data()
