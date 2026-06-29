"""
FinShield Enterprise — Fraud Operations Center
===============================================
SOC-style real-time fraud detection dashboard.
Runs on Streamlit Community Cloud without Kafka/Spark
by using a built-in background data simulator.
"""

from __future__ import annotations
from datetime import datetime
from dashboard.components.charts import (
    render_severity_donut,
    render_city_bar,
    render_merchant_bar,
    render_fraud_table,
    render_risk_customers,
    render_reason_donut,
    render_trend_chart,
    render_severity_summary,
)
from dashboard.components.kpi_cards import render_kpi_cards
from dashboard.components.live_alert import render_live_alert
from dashboard.components.header import render_header
from dashboard.components.sidebar import render_sidebar
from dashboard.metrics import calculate_metrics
from dashboard.load_data import load_data
from dashboard.styles import load_css
from streamlit_autorefresh import st_autorefresh
import streamlit as st

import sys
from pathlib import Path

# ── path setup ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_DIR = ROOT / "database"
DASH_DIR = ROOT / "dashboard"

for p in [str(ROOT), str(DASH_DIR), str(DB_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── boot streamer before any st calls ──────────────────────────────────────
from database.streamer import ensure_seeded, start_streaming  # noqa: E402

ensure_seeded(min_rows=1500)
start_streaming(interval=4.0)

# ── streamlit ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="FinShield — Fraud Operations Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── local imports ──────────────────────────────────────────────────────────

# ── CSS ────────────────────────────────────────────────────────────────────
load_css()

# ── auto refresh every 10 s ────────────────────────────────────────────────
st_autorefresh(interval=10_000, key="fs_refresh")

# ── data ───────────────────────────────────────────────────────────────────
try:
    all_df, fraud_df = load_data()
except Exception as e:
    st.error(f"Data load error: {e}")
    st.stop()

# ── metrics ────────────────────────────────────────────────────────────────
try:
    metrics = calculate_metrics(all_df, fraud_df)
except Exception as e:
    st.error(f"Metrics error: {e}")
    st.stop()

# ── sidebar ────────────────────────────────────────────────────────────────
filters = render_sidebar(metrics, fraud_df)

# apply filters
_fdf = fraud_df.copy()
_adf = all_df.copy()
if filters["city"] != "All Cities":
    _fdf = _fdf[_fdf["city"] == filters["city"]]
    _adf = _adf[_adf["city"] == filters["city"]]
if filters["severity"] != "All Severities" and "fraud_severity" in _fdf.columns:
    _fdf = _fdf[_fdf["fraud_severity"] == filters["severity"]]

_metrics = calculate_metrics(_adf, _fdf)

# ── header (top bar) ───────────────────────────────────────────────────────
render_header()

# ── page routing ───────────────────────────────────────────────────────────
page = filters.get("page", "Overview")

if page == "Overview":
    render_kpi_cards(_metrics)
    render_live_alert(_fdf)

    st.markdown('<div style="padding:14px 28px 0">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1.5])
    with col1:
        render_severity_donut(_fdf)
    with col2:
        render_city_bar(_fdf)
    with col3:
        render_merchant_bar(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:14px 28px 0">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        render_fraud_table(_fdf)
    with col_right:
        render_risk_customers(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:14px 28px 0">', unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 1.5, 1])
    with col_r1:
        render_reason_donut(_fdf)
    with col_r2:
        render_trend_chart(_adf, _fdf)
    with col_r3:
        render_severity_summary(_metrics)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Fraud Alerts":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    render_live_alert(_fdf)
    st.markdown("### 🚨 All Fraud Transactions")
    render_fraud_table(_fdf)
    col1, col2 = st.columns(2)
    with col1:
        render_severity_donut(_fdf)
    with col2:
        render_reason_donut(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    render_kpi_cards(_metrics)
    col1, col2 = st.columns(2)
    with col1:
        render_city_bar(_fdf)
    with col2:
        render_merchant_bar(_fdf)
    render_trend_chart(_adf, _fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Customers":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    st.markdown("### 👥 Customer Risk Analysis")
    render_risk_customers(_fdf)
    render_fraud_table(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Merchants":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    st.markdown("### 🏪 Merchant Analysis")
    render_merchant_bar(_fdf)
    render_fraud_table(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Trends":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    st.markdown("### 📉 Fraud Trends")
    render_trend_chart(_adf, _fdf)
    col1, col2 = st.columns(2)
    with col1:
        render_city_bar(_fdf)
    with col2:
        render_reason_donut(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Reports":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    st.markdown("### 📋 Reports")
    render_kpi_cards(_metrics)
    render_severity_summary(_metrics)
    render_fraud_table(_fdf)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Settings":
    st.markdown('<div style="padding:18px 28px 0">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    st.info("🔧 Settings panel — configure Kafka, Snowflake, and alert thresholds here.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="fs-footer">
    <div class="fs-footer-chips">
        <div class="fs-footer-chip">📡 <span>Data Source: Kafka + PySpark Streaming</span></div>
        <div class="fs-footer-chip">🗄️ <span>Storage: AWS S3 / Snowflake</span></div>
        <div class="fs-footer-chip">⚡ <span>Processing: PySpark Structured Streaming</span></div>
        <div class="fs-footer-chip">📊 <span>Visualization: Streamlit + Plotly</span></div>
    </div>
    <div>🕐 Last Updated: {datetime.now().strftime("%d %b %Y %H:%M:%S")}</div>
</div>
""", unsafe_allow_html=True)
