"""
FinShield — In-App Live Streamer
Runs inside Streamlit as a background thread so the DB stays fresh
even on Streamlit Community Cloud (no separate process needed).

Rules:
- 1 transaction generated per second
- ~10% of all transactions are fraud (realistic ratio)
- All timestamps stored in IST
"""

from __future__ import annotations

import random
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))

DB_PATH = Path(__file__).resolve().parent / "finshield.db"

CUSTOMERS = [
    ("C001", "Ravi Kumar",    "Hyderabad"),
    ("C002", "Anjali Gupta", "Mumbai"),
    ("C003", "Rahul Singh",  "Delhi"),
    ("C004", "Amit Verma",   "Jaipur"),
    ("C005", "Arjun Mehta",  "Pune"),
    ("C006", "Meera Nair",   "Bangalore"),
    ("C007", "Priya Sharma", "Chennai"),
    ("C008", "Deepak Patel", "Ahmedabad"),
    ("C009", "Kiran Rao",    "Hyderabad"),
    ("C010", "Sneha Reddy",  "Mumbai"),
]

CITIES = [
    "Hyderabad", "Mumbai", "Bangalore", "Pune", "Delhi",
    "Chennai", "Ahmedabad", "Jaipur", "Kochi", "Other",
]

MERCHANTS_CLEAN = ["Amazon", "Flipkart", "BigBasket",
                   "Swiggy", "Zomato", "Myntra", "Other Merchants"]
MERCHANTS_RISKY = ["Suspicious Merchant", "Blocked Merchant",
                   "Unknown Merchant", "High Risk Merchant"]

PAYMENT_TYPES = ["UPI", "Card", "NetBanking", "Wallet"]

ACCOUNT_STATUSES = ["Active"] * 90 + ["Blocked"] * 5 + ["Suspended"] * 5

TARGET_FRAUD_RATE = 0.10


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id     TEXT PRIMARY KEY,
            customer_id        TEXT,
            customer_name      TEXT,
            city               TEXT,
            amount             REAL,
            merchant            TEXT,
            payment_type       TEXT,
            transaction_status TEXT,
            fraud_decision     TEXT,
            fraud_flag         TEXT,
            fraud_severity     TEXT,
            fraud_score        INTEGER,
            fraud_reason       TEXT,
            risk_level         TEXT,
            account_status     TEXT,
            event_timestamp    TEXT
        )
    """)
    conn.commit()


def _gen_tx(ts: datetime) -> dict:
    cid, cname, _ = random.choice(CUSTOMERS)
    city = random.choice(CITIES)

    make_risky = random.random() < TARGET_FRAUD_RATE

    if make_risky:
        amount = round(random.uniform(45_000, 150_000), 2)
        merchant = random.choice(MERCHANTS_RISKY + MERCHANTS_CLEAN[:2])
        acct = random.choices(
            ["Active", "Blocked", "Suspended"], weights=[40, 35, 25]
        )[0]
    else:
        amount = round(random.uniform(100, 35_000), 2)
        merchant = random.choice(MERCHANTS_CLEAN)
        acct = random.choice(ACCOUNT_STATUSES)

    reasons: list[str] = []
    if amount > 50_000:
        reasons.append("AMOUNT_RULE")
    if merchant in MERCHANTS_RISKY:
        reasons.append("MERCHANT_RULE")
    if acct == "Blocked":
        reasons.append("BLOCKED_ACCOUNT")
    if city in ("Hyderabad", "Mumbai", "Delhi") and amount > 40_000:
        reasons.append("HIGH_RISK_CITY")

    is_fraud = len(reasons) >= 2 or (
        len(reasons) == 1 and random.random() < 0.15)

    fraud_decision = "FRAUD" if is_fraud else "CLEAN"
    fraud_score = random.randint(65, 99) if is_fraud else random.randint(5, 45)

    if is_fraud:
        fraud_severity = "CRITICAL" if fraud_score >= 85 else "HIGH"
        fraud_reason = " + ".join(reasons) if reasons else "OTHER_RULES"
    else:
        fraud_severity = "LOW"
        fraud_reason = ""

    return {
        "transaction_id":     str(uuid.uuid4()),
        "customer_id":        cid,
        "customer_name":      cname,
        "city":               city,
        "amount":             amount,
        "merchant":           merchant,
        "payment_type":       random.choice(PAYMENT_TYPES),
        "transaction_status": "SUCCESS",
        "fraud_decision":     fraud_decision,
        "fraud_flag":         "Y" if is_fraud else "N",
        "fraud_severity":     fraud_severity,
        "fraud_score":        fraud_score,
        "fraud_reason":       fraud_reason,
        "risk_level":         "HIGH" if is_fraud else "LOW",
        "account_status":     acct,
        "event_timestamp":    ts.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S"),
    }


def _insert(conn: sqlite3.Connection, tx: dict) -> None:
    conn.execute("""
        INSERT OR IGNORE INTO transactions VALUES (
            :transaction_id, :customer_id, :customer_name, :city, :amount,
            :merchant, :payment_type, :transaction_status, :fraud_decision,
            :fraud_flag, :fraud_severity, :fraud_score, :fraud_reason,
            :risk_level, :account_status, :event_timestamp
        )
    """, tx)
    conn.commit()


def _reset_if_stale(conn: sqlite3.Connection) -> None:
    row = conn.execute(
        "SELECT COUNT(*), SUM(CASE WHEN fraud_decision='FRAUD' THEN 1 ELSE 0 END) FROM transactions"
    ).fetchone()
    total, frauds = row[0] or 0, row[1] or 0
    if total > 0:
        fraud_pct = frauds / total
        if fraud_pct > 0.20:
            conn.execute("DELETE FROM transactions")
            conn.commit()


def ensure_seeded(min_rows: int = 1500) -> None:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    _create_tables(conn)
    _reset_if_stale(conn)

    count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if count < min_rows:
        now = datetime.now(tz=IST)
        start = now - timedelta(seconds=min_rows)
        rows = []
        for i in range(min_rows - count):
            ts = start + timedelta(seconds=i)
            rows.append(_gen_tx(ts))
        conn.executemany("""
            INSERT OR IGNORE INTO transactions VALUES (
                :transaction_id, :customer_id, :customer_name, :city, :amount,
                :merchant, :payment_type, :transaction_status, :fraud_decision,
                :fraud_flag, :fraud_severity, :fraud_score, :fraud_reason,
                :risk_level, :account_status, :event_timestamp
            )
        """, rows)
        conn.commit()
    conn.close()


_stream_started = False
_lock = threading.Lock()


def _stream_worker(interval: float) -> None:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    _create_tables(conn)
    while True:
        _insert(conn, _gen_tx(datetime.now(tz=IST)))
        time.sleep(interval)


def start_streaming(interval: float = 1.0) -> None:
    global _stream_started
    with _lock:
        if not _stream_started:
            t = threading.Thread(
                target=_stream_worker,
                args=(interval,),
                daemon=True,
            )
            t.start()
            _stream_started = True
