from sqlalchemy import Column, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EventDB(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    store_id = Column(String)
    camera_id = Column(String)
    visitor_id = Column(String)
    event_type = Column(String)
    timestamp = Column(String)
    confidence = Column(Float)

class TransactionDB(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    order_id = Column(String)
    invoice_number = Column(String)
    order_date = Column(String)
    order_time = Column(String)
    store_id = Column(String)
    store_name = Column(String)
    customer_number = Column(String)
    total_amount = Column(Float)