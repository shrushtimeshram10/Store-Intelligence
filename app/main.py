from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.database import engine
from app.database import SessionLocal
from app.db_models import EventDB, TransactionDB
import requests
from datetime import datetime

app = FastAPI()

events_db = []

class Event(BaseModel):
    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: str
    confidence: float


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/events/ingest")
def ingest(events: List[Event]):

    db = SessionLocal()

    for event in events:

        existing = db.query(EventDB).filter(
            EventDB.event_id == event.event_id
        ).first()

        if existing:
            continue

        db_event = EventDB(
            event_id=event.event_id,
            store_id=event.store_id,
            camera_id=event.camera_id,
            visitor_id=event.visitor_id,
            event_type=event.event_type,
            timestamp=event.timestamp,
            confidence=event.confidence
        )

        db.add(db_event)

    db.commit()
    db.close()

    return {
        "received": len(events)
    }


@app.get("/stores/{store_id}/metrics")
def metrics(store_id: str):

    db = SessionLocal()

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    visitors = set()

    for event in events:
        visitors.add(event.visitor_id)

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    transaction_count = len(transactions)

    revenue = sum(
        txn.total_amount for txn in transactions
        if txn.total_amount is not None
    )

    db.close()

    return {
        "store_id": store_id,
        "unique_visitors": len(visitors),
        "transactions": transaction_count,
        "revenue": round(revenue, 2)
    }

@app.get("/stores/{store_id}/conversion")
def conversion(store_id: str):

    db = SessionLocal()

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    visitors = set()

    for event in events:
        visitors.add(event.visitor_id)

    visitor_count = len(visitors)

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    unique_orders = set()

    for txn in transactions:
        unique_orders.add(txn.order_id)

    transaction_count = len(unique_orders)

    conversion_rate = 0

    if visitor_count > 0:
        conversion_rate = (
            transaction_count / visitor_count
        ) * 100

    db.close()

    return {
        "store_id": store_id,
        "visitors": visitor_count,
        "transactions": transaction_count,
        "conversion_rate": round(conversion_rate, 2)
    }


@app.get("/stores/{store_id}/funnel")
def funnel(store_id: str):

    db = SessionLocal()

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    visitors = set()

    for event in events:
        visitors.add(event.visitor_id)

    entry_count = len(visitors)

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    purchase_count = len(
        set(txn.order_id for txn in transactions)
    )

    conversion_rate = 0

    if entry_count > 0:
        conversion_rate = (
            purchase_count / entry_count
        ) * 100

    db.close()

    return {
        "store_id": store_id,
        "entry": entry_count,
        "purchase": purchase_count,
        "conversion_rate": round(
            conversion_rate, 2
        )
    }

@app.get("/stores/{store_id}/revenue")
def revenue(store_id: str):

    db = SessionLocal()

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    transaction_count = len(
        set(txn.order_id for txn in transactions)
    )

    revenue = sum(
        txn.total_amount
        for txn in transactions
        if txn.total_amount is not None
    )

    avg_order_value = 0

    if transaction_count > 0:
        avg_order_value = revenue / transaction_count

    db.close()

    return {
        "store_id": store_id,
        "transactions": transaction_count,
        "revenue": round(revenue, 2),
        "avg_order_value": round(avg_order_value, 2)
    }

@app.get("/stores/{store_id}/heatmap")
def heatmap(store_id: str):
    return {
        "SKINCARE": 80,
        "MAKEUP": 50
    }


@app.get("/stores/{store_id}/anomalies")
def anomalies(store_id: str):

    db = SessionLocal()

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    visitors = len(
        set(event.visitor_id for event in events)
    )

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    purchase_count = len(
        set(txn.order_id for txn in transactions)
    )

    revenue = sum(
        txn.total_amount
        for txn in transactions
        if txn.total_amount is not None
    )

    anomalies = []

    if visitors < 5:
        anomalies.append(
            "Low visitor traffic detected"
        )

    if revenue < 5000:
        anomalies.append(
            "Revenue below expected threshold"
        )

    if visitors > 0:

        conversion_rate = (
            purchase_count / visitors
        ) * 100

        if conversion_rate < 10:
            anomalies.append(
                "Low conversion rate detected"
            )

    db.close()

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }

@app.get("/stores/{store_id}/insights")
def insights(store_id: str):

    db = SessionLocal()

    events = db.query(EventDB).filter(
        EventDB.store_id == store_id
    ).all()

    visitors = len(
        set(event.visitor_id for event in events)
    )

    transactions = db.query(TransactionDB).filter(
        TransactionDB.store_id == store_id
    ).all()

    revenue = sum(
        txn.total_amount for txn in transactions
        if txn.total_amount is not None
    )

    transaction_count = len(
        set(txn.order_id for txn in transactions)
    )

    db.close()

    insights = []

    if visitors > 20:
        insights.append(
            "🔥 High visitor traffic detected."
        )

    if visitors > 0:

        conversion_rate = (
            transaction_count / visitors
        ) * 100

        if conversion_rate < 30:
            insights.append(
                "⚠️ Conversion rate is below target."
            )
        else:
            insights.append(
                "✅ Conversion rate is healthy."
            )

    avg_order = 0

    if transaction_count > 0:
        avg_order = revenue / transaction_count

    if avg_order > 500:
        insights.append(
            "💰 Customers are spending well per order."
        )

    if not insights:
        insights.append(
            "Store performance appears normal."
        )

    return {
        "store_id": store_id,
        "insights": insights
    }