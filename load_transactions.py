import pandas as pd
import uuid

from app.database import SessionLocal
from app.db_models import TransactionDB

df = pd.read_csv("data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv")

db = SessionLocal()

for _, row in df.iterrows():

    txn = TransactionDB(
        id=str(uuid.uuid4()),
        order_id=str(row["order_id"]),
        invoice_number=str(row["invoice_number"]),
        order_date=str(row["order_date"]),
        order_time=str(row["order_time"]),
        store_id=str(row["store_id"]),
        store_name=str(row["store_name"]),
        customer_number=str(row["customer_number"]),
        total_amount=float(row["total_amount"])
    )

    db.merge(txn)

db.commit()
db.close()

print("Transactions imported successfully!")