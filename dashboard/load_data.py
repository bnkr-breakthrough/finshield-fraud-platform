"""
FinShield — Data Loader
Reads from SQLite with short TTL cache so Streamlit auto-refresh
picks up new transactions without hammering the DB.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "finshield.db"
MAX_RECORDS = 5000


@st.cache_data(ttl=3)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    conn = sqlite3.connect(DB_PATH)

    all_df = pd.read_sql_query(
        f"""
        SELECT *
        FROM transactions
        ORDER BY event_timestamp DESC
        LIMIT {MAX_RECORDS}
        """,
        conn,
    )

    fraud_df = pd.read_sql_query(
        f"""
        SELECT *
        FROM transactions
        WHERE fraud_decision = 'FRAUD'
        ORDER BY event_timestamp DESC
        LIMIT {MAX_RECORDS}
        """,
        conn,
    )

    conn.close()
    return all_df, fraud_df
