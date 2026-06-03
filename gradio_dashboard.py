from pipeline.track import run_tracking
import gradio as gr
import requests
import plotly.graph_objects as go
from app.database import SessionLocal
from app.db_models import EventDB
from transaction_loader import load_transaction_csv

API_URL = "http://127.0.0.1:8000"


# -------------------------
# CHARTS
# -------------------------

def create_conversion_chart(visitors, transactions):

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Visitors", "Transactions"],
                values=[visitors, transactions],
                hole=0.65
            )
        ]
    )

    fig.update_layout(
        title={
            "text": "Conversion Overview",
            "font": {"size": 20}
        },
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=420,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig


def create_revenue_chart(revenue):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=["Week 1", "Week 2", "Week 3", "Week 4", "Current"],
            y=[
                revenue * 0.4,
                revenue * 0.6,
                revenue * 0.75,
                revenue * 0.9,
                revenue
            ],
            mode="lines+markers",
            name="Revenue"
        )
    )

    fig.update_layout(
        title={
            "text": "Revenue Trend",
            "font": {"size": 20}
        },
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=420,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig


# -------------------------
# FETCH DATA
# -------------------------

def get_store_data():

    store_id = "ST1008"

    metrics = requests.get(
        f"{API_URL}/stores/{store_id}/metrics"
    ).json()

    conversion = requests.get(
        f"{API_URL}/stores/{store_id}/conversion"
    ).json()

    revenue = requests.get(
        f"{API_URL}/stores/{store_id}/revenue"
    ).json()

    anomalies = requests.get(
        f"{API_URL}/stores/{store_id}/anomalies"
    ).json()

    insights = requests.get(
        f"{API_URL}/stores/{store_id}/insights"
    ).json()

    anomaly_text = "✅ No anomalies detected"

    if anomalies["anomalies"]:
        anomaly_text = "\n".join(
            anomalies["anomalies"]
        )

    insight_text = "\n".join(
        insights["insights"]
    )

    pie_chart = create_conversion_chart(
        metrics["unique_visitors"],
        conversion["transactions"]
    )

    revenue_chart = create_revenue_chart(
        revenue["revenue"]
    )

    return (
        metrics["unique_visitors"],
        conversion["transactions"],
        revenue["revenue"],
        conversion["conversion_rate"],
        revenue["avg_order_value"],
        pie_chart,
        revenue_chart,
        anomaly_text,
        insight_text
    )

def process_video(video):

    print("Uploaded video:", video)

    # Clear old CCTV events

    db = SessionLocal()

    db.query(EventDB).delete()

    db.commit()

    db.close()

    print("Old events cleared")

    run_tracking(video)

    return "✅ Video processed successfully"

# -------------------------
# STYLING
# -------------------------

custom_css = """
body {
    background: #edf4ff !important;
}

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
    padding-left: 50px !important;
    padding-right: 50px !important;
    padding-top: 20px !important;
    background: #edf4ff !important;
}

footer {
    display: none !important;
}

.main-title {
    text-align: center;
    margin-bottom: 20px;
}

.main-title h1 {
    font-size: 38px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 5px;
}

.main-title p {
    font-size: 16px;
    color: #64748b;
    font-weight: 500;
}

label {
    font-size: 14px !important;
    font-weight: 600 !important;
}

input {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #1e293b !important;
}

textarea {
    font-size: 16px !important;
    font-weight: 500 !important;
}

button {
    font-size: 16px !important;
    font-weight: 600 !important;
}
"""


# -------------------------
# DASHBOARD
# -------------------------


with gr.Blocks(
    css=custom_css,
    theme=gr.themes.Soft(),
    title="AI Store Intelligence Dashboard"
) as demo:

    gr.HTML("""
    <div class="main-title">
        <h1>🏪 AI Store Intelligence Dashboard</h1>
        <p>Real-Time Retail Analytics powered by YOLOv8 + FastAPI + SQLite</p>
    </div>
    """)
    # CCTV Upload Section

    gr.Markdown("## 🎥 Upload CCTV Footage")

    video_input = gr.Video(
        label="Upload CCTV Video"
    )

    analyze_btn = gr.Button(
        "Analyze Video",
        variant="primary"
    )

    status_box = gr.Textbox(
        label="Processing Status",
        interactive=False
    )

    analyze_btn.click(
        fn=process_video,
        inputs=[video_input],
        outputs=[status_box]
    )

    # KPI ROW

    with gr.Row():

        visitors = gr.Number(
            label="👥 Visitors",
            precision=0,
            interactive=False
        )

        transactions = gr.Number(
            label="🧾 Transactions",
            precision=0,
            interactive=False
        )

        revenue = gr.Number(
            label="💰 Revenue (₹)",
            interactive=False
        )

        conversion_rate = gr.Number(
            label="📈 Conversion Rate (%)",
            interactive=False
        )

        avg_order_value = gr.Number(
            label="🛒 Avg Order Value (₹)",
            interactive=False
        )

    gr.HTML("<br>")

    # CHARTS

    with gr.Row():

        conversion_chart = gr.Plot(
            label="Conversion Overview"
        )

        revenue_chart = gr.Plot(
            label="Revenue Trend"
        )

    gr.HTML("<br>")

    # ALERTS

    anomalies_box = gr.Textbox(
        label="🚨 Alerts & Anomalies",
        lines=4,
        interactive=False
    )

    gr.HTML("<br>")

    # AI INSIGHTS

    insights_box = gr.Textbox(
        label="🤖 AI Insights",
        lines=6,
        interactive=False
    )

    gr.HTML("<br>")

    gr.Markdown("## 📂 POS Transaction Upload")

    csv_input = gr.File(
        label="Upload Transaction CSV",
        file_types=[".csv"]
    )

    csv_status = gr.Textbox(
        label="CSV Upload Status",
        interactive=False
    )

    upload_csv_btn = gr.Button(
        "Upload Transactions",
        variant="secondary"
    )

    upload_csv_btn.click(
        fn=load_transaction_csv,
        inputs=[csv_input],
        outputs=[csv_status]
    )

    refresh = gr.Button(
        "🔄 Refresh Dashboard",
        variant="primary",
        size="lg"
    )

    refresh.click(
        fn=get_store_data,
        outputs=[
            visitors,
            transactions,
            revenue,
            conversion_rate,
            avg_order_value,
            conversion_chart,
            revenue_chart,
            anomalies_box,
            insights_box
        ]
    )

    demo.load(
        fn=get_store_data,
        outputs=[
            visitors,
            transactions,
            revenue,
            conversion_rate,
            avg_order_value,
            conversion_chart,
            revenue_chart,
            anomalies_box,
            insights_box
        ]
    )

demo.launch()