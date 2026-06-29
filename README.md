# 🛡️ FinShield — Fraud Operations Center

> **Real-Time Financial Risk Monitoring & Fraud Detection Platform**  
> Built with PySpark · Kafka · Snowflake · Streamlit · Plotly

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## 🖥️ Live Demo

Access the dashboard from **any device, anywhere** — no laptop required:  
👉 [finshield.streamlit.app](https://your-app-url.streamlit.app)

---

## 📸 Dashboard Preview

![FinShield Dashboard](screenshots/dashboard.png)

---

## 🏗️ Architecture

```
Kafka Producer ──► PySpark Streaming ──► SQLite/Snowflake
                                              │
                                    Streamlit Dashboard
                                    (SOC-style, live refresh)
```

**Production Stack:**  
`Kafka` → `PySpark Structured Streaming` → `AWS S3` → `Snowflake` → `Streamlit`

**Demo/Cloud Stack (no infra needed):**  
`Python Simulator` → `SQLite` → `Streamlit`

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/finshield-fraud-platform.git
cd finshield-fraud-platform

# 2. Install
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app auto-seeds 1,500 historical transactions and starts a live simulator
on first launch — no Kafka or Spark needed for local demo.

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

> Access your dashboard from phone, tablet, or any browser worldwide.

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "feat: FinShield v2 SOC dashboard"
git remote add origin https://github.com/YOUR_USERNAME/finshield-fraud-platform.git
git push -u origin main
```

### Step 2 — Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Set:
   - **Repository:** `YOUR_USERNAME/finshield-fraud-platform`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy**

Done! Your dashboard is live in ~2 minutes. 🎉

---

## 📁 Project Structure

```
finshield-fraud-platform/
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── .streamlit/
│   └── config.toml                 # Dark theme config
│
├── dashboard/
│   ├── load_data.py                # SQLite data loader (cached)
│   ├── metrics.py                  # KPI calculations
│   ├── styles.py                   # Glassmorphism CSS
│   └── components/
│       ├── header.py               # Top bar
│       ├── sidebar.py              # Nav + filters + system status
│       ├── live_alert.py           # Animated fraud alert banner
│       ├── kpi_cards.py            # 5 KPI cards with sparklines
│       └── charts.py               # All Plotly charts
│
├── database/
│   ├── streamer.py                 # Background live data simulator
│   ├── seed_data.py                # Standalone seeder script
│   └── finshield.db               # SQLite (auto-created)
│
├── kafka/
│   ├── transaction_producer.py     # Kafka producer (production)
│   └── docker/docker-compose.yml  # Kafka + Zookeeper
│
└── spark/
    ├── fraud_detection_stream.py   # PySpark streaming job
    └── database_writer.py          # Spark → SQLite writer
```

---

## 🎯 Dashboard Features

| Feature | Description |
|---------|-------------|
| 🔄 **Live Streaming** | Auto-refreshes every 10 seconds |
| 📊 **KPI Cards** | Total transactions, fraud count, fraud %, amount, critical alerts |
| 🚨 **Live Alert Banner** | Animated banner showing latest fraud detection |
| 🍩 **Severity Distribution** | Donut chart: CRITICAL vs HIGH breakdown |
| 📍 **City Heatmap** | Top 10 cities by fraud volume |
| 🏪 **Merchant Analysis** | Top 5 merchants with highest fraud |
| 📋 **Fraud Table** | Latest alerts with severity badges |
| 👥 **Risk Customers** | Customer risk score leaderboard |
| 📈 **24h Trend** | Hourly fraud frequency timeline |
| 🛡️ **Severity Summary** | CRITICAL / HIGH / MEDIUM / LOW breakdown |
| ✅ **System Status** | Kafka, PySpark, Snowflake health panel |

---

## 🔐 Tech Stack

| Layer | Technology |
|-------|-----------|
| Streaming | Apache Kafka + PySpark Structured Streaming |
| Storage | SQLite (demo) / AWS S3 + Snowflake (production) |
| Transformation | dbt (staging + mart models) |
| Orchestration | Apache Airflow |
| Visualization | Streamlit + Plotly |
| Deployment | Streamlit Community Cloud |

---

## 📜 Certifications Showcased

- ✅ **SnowPro Core** — Snowpipe, Streams & Tasks, Dynamic Tables, Cortex AI
- ✅ **AWS Data Engineer** — S3, Glue, Lambda integration
- ✅ **Databricks DE Associate** — PySpark streaming architecture

---

## 👤 Author

**Beeram Neela Konda Reddy**  
ETL Developer → Senior Data Engineer  
Cognizant · 4 Years Experience  
Stack: Python · Spark · SQL · GCP · Snowflake · Databricks
