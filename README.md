# 🏪 AI-Powered Retail Store Intelligence System

An AI-driven retail analytics platform that combines CCTV-based visitor tracking and POS transaction analytics to generate actionable business insights for retailers.

---

## 📌 Overview

Retail stores generate valuable data through CCTV cameras and Point-of-Sale (POS) systems. However, these systems often operate independently, making it difficult to derive meaningful business intelligence.

This project integrates Computer Vision and Transaction Analytics to provide a unified dashboard for monitoring store performance, customer footfall, conversion rates, and revenue metrics.

---

## 🚀 Features

### 🎥 CCTV Visitor Analytics
- Visitor detection using YOLOv8
- Person tracking across video frames
- Unique visitor counting
- Footfall analysis

### 💳 POS Transaction Analytics
- CSV-based transaction ingestion
- Revenue calculation
- Average Order Value (AOV) analysis
- Transaction monitoring

### 📊 Business Intelligence Dashboard
- Interactive Gradio dashboard
- Revenue analytics
- Conversion analytics
- KPI visualization
- AI-generated insights

### 🚨 Anomaly Detection
- Detection of unusual visitor-to-sales patterns
- Operational alerts and business insights

---

## 🏗️ System Architecture

CCTV Footage  
↓  
YOLOv8 Detection  
↓  
Visitor Tracking  
↓  
FastAPI Backend  
↓  
SQLite Database  
↑  
│  
Transaction CSV  
↓  
Data Ingestion Layer  
↓  
Analytics Engine  
↓  
Gradio Dashboard

---

## 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| Computer Vision | YOLOv8 |
| Backend | FastAPI |
| Database | SQLite |
| Dashboard | Gradio |
| Visualization | Plotly |
| Data Processing | Pandas |
| ORM | SQLAlchemy |

---

## 📂 Project Structure

store-intelligence/

├── app/

│ ├── main.py

│ ├── database.py

│ └── db_models.py

│

├── pipeline/

│ └── track.py

│

├── data/

│

├── videos/

│

├── transaction_loader.py

├── watch_transactions.py

├── gradio_dashboard.py

├── requirements.txt

└── README.md

---

## 📈 Key Metrics

### Visitor Count
Total unique visitors detected from CCTV footage.

### Transactions
Total purchases imported from POS transaction data.

### Revenue
Total sales generated from all transactions.

### Conversion Rate

Conversion Rate = Transactions / Visitors × 100

### Average Order Value (AOV)

AOV = Revenue / Transactions

---

## 🔌 API Endpoints

### Health Check

GET /health

### Store Metrics

GET /stores/{store_id}/metrics

### Conversion Analytics

GET /stores/{store_id}/conversion

### Revenue Analytics

GET /stores/{store_id}/revenue

### Insights

GET /stores/{store_id}/insights

### Anomalies

GET /stores/{store_id}/anomalies

---

## ▶️ Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/store-intelligence.git
cd store-intelligence
2. Install Dependencies
pip install -r requirements.txt
3. Start FastAPI Backend
python -m uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000
4. Launch Dashboard
python gradio_dashboard.py

Dashboard runs at:

http://127.0.0.1:7860
📊 Workflow
Upload CCTV footage
Detect and track visitors using YOLOv8
Upload transaction CSV data
Store analytics data in SQLite
Generate revenue and conversion metrics
Visualize results on the Gradio dashboard
🔮 Future Enhancements
Real-time CCTV stream processing
Multi-camera support
Customer movement heatmaps
Daily/Weekly/Monthly analytics filters
Cloud deployment
PostgreSQL integration
Live POS synchronization
Advanced AI-based anomaly detection
🎯 Business Impact

This solution enables retailers to:

Understand customer footfall trends
Measure conversion rates effectively
Monitor revenue performance
Detect operational anomalies
Make data-driven business decisions
👩‍💻 Author

Shrushti Meshram

B.Tech Electronics & Telecommunication Engineering

Interests: Artificial Intelligence, Computer Vision, Data Analytics, and Full-Stack Development

📜 License

This project is developed for academic and educational purposes.
