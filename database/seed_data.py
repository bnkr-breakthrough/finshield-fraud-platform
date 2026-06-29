"""
FinShield — Seed / Live Data Simulator
Generates realistic fraud transaction data for demo/cloud deployment.
Run once to create finshield.db, then dashboard reads from it.
"""

import sqlite3
import random
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

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
    "Hyderabad","Mumbai","Bangalore","Pune","Delhi",
    "Chennai","Ahmedabad","Jaipur","Kochi","Other",
]

MERCHANTS = [
    "Suspicious Merchant","Blocked Merchant",
    "Unknown Merchant","High Risk Merchant","Other Merchants",
    "Amazon","Flipkart","BigBasket","Swiggy","Zomato",
]

PAYMENT_TYPES   = ["UPI", "Card", "NetBanking", "Wallet"]
ACCOUNT_STATUSES = ["Active", "Blocked", "Suspended"]

FRAUD_REASONS = [
    "AMOUNT_RULE + MERCHANT_RULE",
    "AMOUNT_RULE + BLOCKED_ACCOUNT",
    "AMOUNT_RULE + HIGH_RISK_CITY",
    "AMOUNT_RULE + HIGH_RISK_CUSTOMER",
    "OTHER_RULES",
]


def _create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id    TEXT PRIMARY KEY,
            customer_id       TEXT,
            customer_name     TEXT,
            city              TEXT,
            amount            REAL,
            merchant          TEXT,
            payment_type      TEXT,
            transaction_status TEXT,
            fraud_decision    TEXT,
            fraud_flag        TEXT,
            fraud_severity    TEXT,
            fraud_score       INTEGER,
            fraud_reason      TEXT,
            risk_level        TEXT,
            account_status    TEXT,
            event_timestamp   TEXT
        )
    """)
    conn.commit()


def _generate_transaction(ts: datetime) -> dict:
    cid, cname, home_city = random.choice(CUSTOMERS)
    city   = random.choice(CITIES)
    amount = round(random.uniform(500, 120_000), 2)
    merchant = random.choice(MERCHANTS)
    acct   = random.choice(ACCOUNT_STATUSES)

    # fraud logic
    is_fraud = False
    reasons  = []
    if amount > 50_000:
        reasons.append("AMOUNT_RULE")
    if merchant in ("Suspicious Merchant", "Blocked Merchant", "Unknown Merchant"):
        reasons.append("MERCHANT_RULE")
    if acct == "Blocked":
        reasons.append("BLOCKED_ACCOUNT")
    if city in ("Hyderabad", "Mumbai", "Delhi") and amount > 40_000:
        reasons.append("HIGH_RISK_CITY")

    if len(reasons) >= 2:
        is_fraud = True
    elif len(reasons) == 1 and random.random() < 0.3:
        is_fraud = True

    fraud_decision = "FRAUD" if is_fraud else "CLEAN"
    fraud_flag     = "Y"     if is_fraud else "N"
    fraud_score    = random.randint(65, 99) if is_fraud else random.randint(5, 45)
    risk_level     = "HIGH"  if is_fraud else "LOW"

    if is_fraud:
        fraud_severity = "CRITICAL" if fraud_score >= 85 else "HIGH"
        fraud_reason   = " + ".join(reasons) if reasons else random.choice(FRAUD_REASONS)
    else:
        fraud_severity = "LOW"
        fraud_reason   = ""

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
        "fraud_flag":         fraud_flag,
        "fraud_severity":     fraud_severity,
        "fraud_score":        fraud_score,
        "fraud_reason":       fraud_reason,
        "risk_level":         risk_level,
        "account_status":     acct,
        "event_timestamp":    ts.strftime("%Y-%m-%d %H:%M:%S"),
    }


def seed_historical(conn, n: int = 1500):
    """Insert n historical records spread over the last 24 hours."""
    now   = datetime.now()
    start = now - timedelta(hours=24)
    rows  = []
    for i in range(n):
        ts = start + timedelta(seconds=i * (86400 / n))
        rows.append(_generate_transaction(ts))

    conn.executemany("""
        INSERT OR IGNORE INTO transactions VALUES (
            :transaction_id, :customer_id, :customer_name, :city, :amount,
            :merchant, :payment_type, :transaction_status, :fraud_decision,
            :fraud_flag, :fraud_severity, :fraud_score, :fraud_reason,
            :risk_level, :account_status, :event_timestamp
        )
    """, rows)
    conn.commit()
    print(f"✅ Seeded {n} historical transactions.")


def stream_live(conn, interval: float = 3.0):
    """Continuously insert new transactions (simulates live Kafka stream)."""
    print("🚀 Live streaming started… (Ctrl+C to stop)")
    while True:
        tx = _generate_transaction(datetime.now())
        try:
            conn.execute("""
                INSERT OR IGNORE INTO transactions VALUES (
                    :transaction_id, :customer_id, :customer_name, :city, :amount,
                    :merchant, :payment_type, :transaction_status, :fraud_decision,
                    :fraud_flag, :fraud_severity, :fraud_score, :fraud_reason,
                    :risk_level, :account_status, :event_timestamp
                )
            """, tx)
            conn.commit()
            label = "🚨 FRAUD" if tx["fraud_decision"] == "FRAUD" else "✅ CLEAN"
            print(f"[{tx['event_timestamp']}] {label} | {tx['customer_name']} | ₹{tx['amount']:,.0f} | {tx['city']}")
        except Exception as e:
            print(f"DB error: {e}")
        time.sleep(interval)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    _create_tables(conn)

    # check if already seeded
    count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if count == 0:
        seed_historical(conn, 1500)
    else:
        print(f"ℹ️  DB already has {count} records. Skipping historical seed.")

    stream_live(conn, interval=3.0)
