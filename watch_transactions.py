from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import pandas as pd

from app.database import SessionLocal
from app.db_models import TransactionDB


CSV_PATH = "data/Brigade_Bangalore_10_April_26 (1)bc6219c.csv"


class TransactionHandler(FileSystemEventHandler):

    def on_modified(self, event):

        if event.src_path.endswith(".csv"):

            print("CSV updated!")

            load_new_transactions()


def load_new_transactions():

    db = SessionLocal()

    df = pd.read_csv(CSV_PATH)

    for _, row in df.iterrows():

        existing = db.query(TransactionDB).filter(
            TransactionDB.order_id == str(row["order_id"])
        ).first()

        if existing:
            continue

        txn = TransactionDB(
            order_id=str(row["order_id"]),
            store_id="ST1008",
            total_amount=float(row["total_amount"])
        )

        db.add(txn)

        print(
            f"New transaction added: {row['order_id']}"
        )

    db.commit()

    db.close()


if __name__ == "__main__":

    event_handler = TransactionHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        path="data",
        recursive=False
    )

    observer.start()

    print("Watching transaction CSV...")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()