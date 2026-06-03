import pandas as pd

from app.database import SessionLocal
from app.db_models import TransactionDB


def load_transaction_csv(csv_file):

    db = SessionLocal()

    df = pd.read_csv(csv_file)

    added = 0

    for _, row in df.iterrows():

        order_id = str(row["order_id"])

        existing = db.query(TransactionDB).filter(
            TransactionDB.order_id == order_id
        ).first()

        if existing:
            continue

        txn = TransactionDB(
            order_id=order_id,
            store_id="ST1008",
            total_amount=float(row["total_amount"])
        )

        db.add(txn)

        added += 1

    db.commit()

    db.close()

    return f"✅ {added} new transactions added"