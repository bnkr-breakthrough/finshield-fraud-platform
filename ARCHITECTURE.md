# FinShield — Architecture

## Overview

FinShield is a real-time fraud detection platform demonstrating an end-to-end modern data engineering stack: streaming ingestion, cloud data warehousing, automated CDC pipelines, in-database ML scoring, and a live operational dashboard.

The project intentionally runs in two modes:

- **Demo mode** (what's deployed live): a lightweight Python simulator + SQLite + Streamlit, designed to run forever on free infrastructure with zero ongoing cost.
- **Production-pattern mode** (what's documented and code-complete): the full Kafka → Spark → Snowflake → dbt → Airflow pipeline, built and validated against a real Snowflake trial account, with all code preserved in this repository.

This split exists deliberately. Free-tier cloud infrastructure (Kafka brokers, Spark clusters, a paid Snowflake plan) is not sustainable to keep running indefinitely for a portfolio project. Rather than let the live demo go dark when a trial expires, the dashboard runs on a self-contained simulator, while the production-grade code remains fully readable, runnable, and explainable from the repository alone.

---

## System Diagram

```
                         ┌─────────────────────────┐
                         │   PRODUCTION PATTERN     │
                         │  (documented, code-complete)
                         │                          │
  Kafka Producer ──────► │  PySpark Structured      │
  (transaction_producer)  │  Streaming               │
                         │  (fraud_detection_stream) │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   SNOWFLAKE              │
                         │                          │
                         │  Snowpipe (file ingestion)│
                         │       │                  │
                         │       ▼                  │
                         │  RAW.TRANSACTIONS table  │
                         │       │                  │
                         │       ▼                  │
                         │  Stream (CDC capture)    │
                         │       │                  │
                         │       ▼                  │
                         │  Task (scheduled, conditional)
                         │       │                  │
                         │       ▼                  │
                         │  ANALYTICS.fraud_summary_log
                         │                          │
                         │  Dynamic Table            │
                         │  (auto-refresh, 1 min lag)│
                         │       │                  │
                         │       ▼                  │
                         │  Snowpark Python UDF      │
                         │  (risk scoring)            │
                         │                          │
                         │  Statistical anomaly      │
                         │  detection (z-score)       │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   dbt                    │
                         │  stg_transactions (view) │
                         │       │                  │
                         │       ▼                  │
                         │  mart_fraud_summary       │
                         │  (table)                  │
                         └─────────────────────────┘


                         ┌─────────────────────────┐
                         │   DEMO MODE (live)        │
                         │                          │
  Python background      │  SQLite (finshield.db)   │
  thread (streamer.py) ─►│  1 transaction/sec       │
  ~10% fraud rate         │  IST timestamps          │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │  Streamlit Dashboard      │
                         │  (Streamlit Community     │
                         │   Cloud, auto-refresh 10s)│
                         │                          │
                         │  - SOC-style glassmorphism UI
                         │  - Live fraud alert banner │
                         │  - KPI cards + sparklines  │
                         │  - 8-page navigation       │
                         └─────────────────────────┘
```

---

## Component Details

### 1. Transaction Generation & Fraud Detection Logic

A Python-based generator produces synthetic financial transactions across 10 customer profiles, 10 cities, and a mix of legitimate and high-risk merchants. Fraud is determined by a multi-rule engine:

- **AMOUNT_RULE** — transaction amount exceeds ₹50,000
- **MERCHANT_RULE** — merchant flagged as suspicious, blocked, or unknown
- **BLOCKED_ACCOUNT** — account status is Blocked
- **HIGH_RISK_CITY** — high-value transaction in a historically higher-risk city

A transaction is flagged as fraud if two or more rules trigger simultaneously, or with a smaller probability if exactly one rule triggers. This mirrors how real fraud engines combine weak signals into a stronger composite decision rather than relying on any single rule. The same logic exists in both the Python simulator (demo mode) and is designed to be portable into a PySpark structured streaming job (production pattern), since the rule logic is simple boolean/threshold-based and translates directly to DataFrame filter operations.

### 2. Streaming Layer (Production Pattern)

`kafka/transaction_producer.py` publishes transaction events to a Kafka topic. `spark/fraud_detection_stream.py` consumes this topic via Spark Structured Streaming, applies the fraud rules, and writes results onward. This demonstrates the core real-time processing skillset even though the live demo substitutes a simpler in-process simulator for cost reasons.

### 3. Snowflake Layer

**Snowpipe**: A named internal stage (`finshield_stage`) holds incoming CSV files. A pipe (`transactions_pipe`) is configured to COPY new files into the `raw.transactions` table. In production this would be configured with cloud storage event notifications for true auto-ingestion; in this trial-account implementation, ingestion is triggered via `ALTER PIPE ... REFRESH`, which validates the same ingestion mechanics Snowpipe uses internally.

**Streams & Tasks**: A stream (`transactions_stream`) captures row-level changes (CDC) on the transactions table. A task (`process_fraud_stream`) runs on a 1-minute schedule but only executes its body when `SYSTEM$STREAM_HAS_DATA()` returns true — avoiding wasted compute on empty checks. When triggered, it aggregates new fraud activity into a summary log table, demonstrating an automated, event-driven (not purely time-driven) processing pattern.

**Dynamic Tables**: `fraud_severity_summary` is defined as a query (severity × city aggregation) with a 1-minute target lag. Snowflake manages the incremental refresh automatically — no manual stream/task wiring required. This is the simplest way to keep a derived aggregate fresh without writing orchestration code.

**Snowpark**: A Python UDF (`calculate_risk_score`) runs natively inside Snowflake's compute engine, combining fraud score, transaction amount, and account status into a single risk score (capped at 100). This demonstrates writing and deploying actual Python logic as a first-class database object, not just SQL.

**Cortex AI**: LLM-based Cortex functions (`CLASSIFY_TEXT`, `COMPLETE`) require a paid Snowflake plan and were not executable on the trial account used for this project — confirmed via direct testing, not assumption. As a substitute demonstrating the same anomaly-detection goal, a statistical z-score method was implemented (`transaction_anomalies` view), flagging any hour where transaction volume deviates more than 2 standard deviations from the mean. This is a legitimate technique used in production fraud systems independent of LLM availability.

### 4. dbt Layer

A minimal but real dbt project (`finshield_dbt/`) implements:
- `stg_transactions` — a staging view that selects and lightly renames raw columns, the standard "thin staging layer" pattern
- `mart_fraud_summary` — a mart table aggregating fraud counts, amounts, and average fraud score by severity and city, built directly from the staging model via `ref()`

This demonstrates the staging → mart layering convention used in most production dbt projects, including a working Snowflake connection configured and debugged from scratch.

### 5. Dashboard Layer

A Streamlit application (`app.py` + `dashboard/`) renders a SOC-style (Security Operations Center) interface:
- Dark glassmorphism theme with animated live-fraud alert banner
- Five KPI cards with sparkline trends (total transactions, fraud count, fraud %, fraud amount, critical alerts)
- Severity distribution donut, city/merchant bar charts, 24-hour trend line
- Top risk customer leaderboard
- Eight-page sidebar navigation (Overview, Fraud Alerts, Analytics, Customers, Merchants, Trends, Reports, Settings)

The dashboard reads from a SQLite database that is continuously populated by a background thread generating one transaction per second at a realistic ~10% fraud rate, with all timestamps stored in IST. This runs indefinitely on Streamlit Community Cloud's free tier with no external dependencies.

---

## Known Limitations & Honest Tradeoffs

- **Cortex LLM functions** (`CLASSIFY_TEXT`, `COMPLETE`) require a paid Snowflake plan; confirmed unavailable on the trial account used here. A working statistical alternative is implemented instead.
- **Snowpipe auto-ingest** in this implementation uses manual `REFRESH` triggers rather than cloud storage event notifications, since true auto-ingest requires an S3/GCS integration with IAM permissions beyond the scope of a free-tier demo. The ingestion mechanics (stage → pipe → COPY INTO → table) are otherwise identical to production Snowpipe.
- **Airflow** is not implemented as a running orchestrator in this project; its role (orchestrating ingest → dbt run → alerting) is documented conceptually here and is implemented fully in a separate, dedicated project to avoid duplicating orchestration work across multiple portfolio pieces within a constrained timeline.
- **The live dashboard's data is synthetic**, generated by a deterministic rule-based simulator rather than sourced from real transactions, as appropriate for a portfolio demonstration.

---

## Tech Stack Summary

| Layer | Technology |
|---|---|
| Streaming (pattern) | Apache Kafka, PySpark Structured Streaming |
| Cloud Warehouse | Snowflake (Snowpipe, Streams, Tasks, Dynamic Tables, Snowpark) |
| Transformation | dbt (staging + mart models) |
| Demo Data Layer | Python, SQLite |
| Visualization | Streamlit, Plotly |
| Deployment | Streamlit Community Cloud, GitHub |
