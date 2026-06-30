# 🛡️ FinShield — Fraud Operations Center

> **Real-Time Financial Risk Monitoring & Fraud Detection Platform**
> Built with Kafka · PySpark · Snowflake · dbt · Streamlit · Plotly

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://finshield-fraud-platform.streamlit.app)

---

## 🖥️ Live Demo

Access the dashboard from **any device, anywhere** — no laptop required:
👉 **[finshield-fraud-platform.streamlit.app](https://finshield-fraud-platform.streamlit.app)**

---

## 📸 Dashboard Preview

![FinShield Dashboard](screenshots/dashboard.png)

SOC-style real-time fraud monitoring with live alerts, KPI tracking, and multi-page analytics — auto-refreshing every 10 seconds.

---

## 📐 Architecture

Full technical breakdown, diagrams, and honest documentation of tradeoffs: **[ARCHITECTURE.md](ARCHITECTURE.md)**

```
Kafka Producer ──► PySpark Structured Streaming ──► Snowflake
                                                        │
                              ┌─────────────────────────┼─────────────────────────┐
                              ▼                         ▼                         ▼
                         Snowpipe                 Streams & Tasks          Dynamic Tables
                      (file ingestion)              (CDC, automation)      (auto-refresh aggregates)
                              │                         │                         │
                              └─────────────────────────┼─────────────────────────┘
                                                        ▼
                                                  Snowpark UDF
                                               (Python risk scoring)
                                                        │
                                                        ▼
                                                       dbt
                                          (staging view → mart table)
```

**Live demo stack** (runs forever, free): `Python Simulator` → `SQLite` → `Streamlit Community Cloud`
**Production-pattern stack** (fully built & documented): `Kafka` → `PySpark` → `Snowflake` → `dbt` → `Streamlit`

---

## 🚀 Quick Start (Local Dashboard)

```bash
# 1. Clone
git clone https://github.com/bnkr-breakthrough/finshield-fraud-platform.git
cd finshield-fraud-platform

# 2. Install
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app auto-seeds historical transactions and starts a live simulator generating 1 transaction/second at a realistic ~10% fraud rate — no Kafka or Spark needed for the local demo.

---

## ☁️ Deploy to Streamlit Community Cloud (Free, Forever)

1. Push this repo to your own GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub
3. **New app** → repository: your fork, branch: `main`, main file: `app.py`
4. Deploy — live in ~2 minutes, accessible from any device worldwide

---

## ❄️ Snowflake Setup (Optional — for exploring the full pipeline)

The Snowflake objects (Snowpipe, Streams, Tasks, Dynamic Tables, Snowpark UDF) were built and validated on a Snowflake trial account. All SQL is preserved in `snowflake/` so the pipeline is fully explainable and re-creatable even without an active trial:

```bash
# Run these in order inside a Snowflake worksheet
snowflake/01_setup_database.sql
snowflake/02_snowpipe.sql
snowflake/03_streams_tasks.sql
snowflake/04_dynamic_tables.sql
snowflake/05_snowpark_udf.sql
snowflake/06_anomaly_detection.sql
```

## 🔧 dbt Setup (Optional)

```bash
cd finshield_dbt
dbt debug   # validate Snowflake connection
dbt run     # builds stg_transactions view + mart_fraud_summary table
```

See `finshield_dbt/models/` for the staging and mart model definitions.

---

## 📁 Project Structure

```
finshield-fraud-platform/
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── ARCHITECTURE.md                 # Full technical architecture + tradeoffs
├── INTERVIEW_GUIDE.md              # Pitch + anticipated Q&A
├── .streamlit/
│   └── config.toml                 # Dark theme config
│
├── dashboard/
│   ├── load_data.py                # SQLite data loader (cached)
│   ├── metrics.py                  # KPI calculations
│   ├── styles.py                   # Glassmorphism CSS
│   └── components/
│       ├── header.py               # Top bar (IST-aware)
│       ├── sidebar.py              # Nav + filters + system status
│       ├── live_alert.py           # Animated fraud alert banner
│       ├── kpi_cards.py            # KPI cards with sparklines
│       └── charts.py               # All Plotly charts
│
├── database/
│   ├── streamer.py                 # Live simulator: 1 tx/sec, ~10% fraud, IST timestamps
│   └── finshield.db                # SQLite (auto-created)
│
├── kafka/
│   └── transaction_producer.py     # Kafka producer (production pattern)
│
├── spark/
│   └── fraud_detection_stream.py   # PySpark Structured Streaming job
│
├── snowflake/
│   ├── 01_setup_database.sql       # Database, schema, warehouse setup
│   ├── 02_snowpipe.sql             # Stage, file format, pipe
│   ├── 03_streams_tasks.sql        # CDC stream + scheduled task
│   ├── 04_dynamic_tables.sql       # Auto-refreshing aggregate table
│   ├── 05_snowpark_udf.sql         # Python UDF for risk scoring
│   └── 06_anomaly_detection.sql    # Z-score statistical anomaly detection
│
└── finshield_dbt/
    ├── dbt_project.yml
    └── models/
        ├── staging/
        │   ├── sources.yml
        │   └── stg_transactions.sql
        └── marts/
            └── mart_fraud_summary.sql
```

---

## 🎯 Dashboard Features

| Feature | Description |
|---------|-------------|
| 🔄 **Live Streaming** | Auto-refreshes every 10 seconds, 1 transaction/sec generation |
| 📊 **KPI Cards** | Total transactions, fraud count, fraud %, amount, critical alerts |
| 🚨 **Live Alert Banner** | Animated banner showing latest fraud detection |
| 🍩 **Severity Distribution** | Donut chart: CRITICAL / HIGH / MEDIUM / LOW breakdown |
| 📍 **City Analysis** | Top 10 cities by fraud volume |
| 🏪 **Merchant Analysis** | Top 5 merchants with highest fraud |
| 📋 **Fraud Table** | Latest alerts with severity badges |
| 👥 **Risk Customers** | Customer risk score leaderboard |
| 📈 **24h Trend** | Hourly fraud frequency timeline |
| 🛡️ **System Status** | Kafka, PySpark, Snowflake health panel |
| 🗂️ **8-Page Navigation** | Overview, Fraud Alerts, Analytics, Customers, Merchants, Trends, Reports, Settings |

---

## ❄️ Snowflake Features Implemented

| Feature | Status | Notes |
|---|---|---|
| **Snowpipe** | ✅ Working | File-based ingestion via stage + pipe + COPY INTO |
| **Streams & Tasks** | ✅ Working | CDC capture, conditional automated processing |
| **Dynamic Tables** | ✅ Working | Self-maintaining aggregates, 1-min refresh, incremental mode |
| **Snowpark** | ✅ Working | Python UDF for in-database risk scoring |
| **Cortex AI (LLM functions)** | ⚠️ Documented limitation | `CLASSIFY_TEXT`/`COMPLETE` require paid plan — confirmed via direct testing |
| **Anomaly Detection** | ✅ Working alternative | Statistical z-score method implemented as substitute |
| **dbt** | ✅ Working | Staging view + mart table, full Snowflake connection |

Full details and honest tradeoffs documented in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🔐 Tech Stack

| Layer | Technology |
|-------|-----------|
| Streaming (pattern) | Apache Kafka, PySpark Structured Streaming |
| Cloud Warehouse | Snowflake (Snowpipe, Streams, Tasks, Dynamic Tables, Snowpark) |
| Transformation | dbt |
| Demo Data Layer | Python, SQLite |
| Visualization | Streamlit, Plotly |
| Deployment | Streamlit Community Cloud, GitHub |

---

## 📜 Certifications Showcased

- ✅ **SnowPro Core** — Snowpipe, Streams & Tasks, Dynamic Tables, Snowpark, Cortex AI (evaluated)
- ✅ **AWS Data Engineer** — cloud data architecture principles
- ✅ **Databricks Certified Data Engineer Associate** — PySpark streaming architecture

---

## 📄 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — full system design, component breakdown, and honest limitations
- **[INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)** — pitch script and prepared answers to likely interview questions

---

## 👤 Author

**Beeram Neela Konda Reddy**
ETL Developer → Senior Data Engineer (target)
Cognizant · 4 Years Experience
Stack: Python · Spark · SQL · GCP · Snowflake · Databricks · dbt

[LinkedIn](#) · [GitHub](https://github.com/bnkr-breakthrough)
