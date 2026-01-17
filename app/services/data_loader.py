import pandas as pd

class DataLoader:

    file_name_to_path = {
        "items": "Dataset/items.csv",
        "visitation": "Dataset/customer_visitation_logs.csv",
        "orders": "Dataset/orders.csv",
        "customers": "Dataset/customers.csv",
        "order_items": "Dataset/order_items.csv",
    }

    def __init__(self, file_name: str):
        self.file_name = file_name

    def load_data(self):
        try:
            path = self.file_name_to_path[self.file_name]
            data = pd.read_csv(path)
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None