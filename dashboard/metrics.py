"""FinShield — Metrics Calculator"""

from __future__ import annotations

import pandas as pd


def calculate_metrics(all_df: pd.DataFrame, fraud_df: pd.DataFrame) -> dict:
    total  = len(all_df)
    frauds = len(fraud_df)

    metrics: dict = {
        "total_transactions": total,
        "fraud_transactions":  frauds,
        "fraud_percentage":    round((frauds / total * 100), 2) if total else 0,
        "fraud_amount":        float(fraud_df["amount"].sum()) if "amount" in fraud_df.columns else 0,
        "critical_alerts":     0,
        "high_alerts":         0,
        "medium_alerts":       0,
        "low_alerts":          0,
    }

    if "fraud_severity" in fraud_df.columns:
        sev = fraud_df["fraud_severity"].value_counts()
        metrics["critical_alerts"] = int(sev.get("CRITICAL", 0))
        metrics["high_alerts"]     = int(sev.get("HIGH",     0))
        metrics["medium_alerts"]   = int(sev.get("MEDIUM",   0))
        metrics["low_alerts"]      = int(sev.get("LOW",      0))

    # sparkline data (last 20 points bucketed)
    if not all_df.empty and "event_timestamp" in all_df.columns:
        all_df = all_df.copy()
        all_df["event_timestamp"] = pd.to_datetime(all_df["event_timestamp"], errors="coerce")
        fraud_df = fraud_df.copy()
        fraud_df["event_timestamp"] = pd.to_datetime(fraud_df["event_timestamp"], errors="coerce")

        metrics["sparkline_total"]  = _sparkline(all_df, 20)
        metrics["sparkline_fraud"]  = _sparkline(fraud_df, 20)
        metrics["sparkline_amount"] = _sparkline_amount(fraud_df, 20)
    else:
        metrics["sparkline_total"]  = []
        metrics["sparkline_fraud"]  = []
        metrics["sparkline_amount"] = []

    return metrics


def _sparkline(df: pd.DataFrame, n: int) -> list[int]:
    if df.empty:
        return [0] * n
    df = df.dropna(subset=["event_timestamp"])
    df = df.sort_values("event_timestamp")
    df["bucket"] = pd.cut(df["event_timestamp"], bins=n, labels=False)
    counts = df.groupby("bucket").size().reindex(range(n), fill_value=0)
    return counts.tolist()


def _sparkline_amount(df: pd.DataFrame, n: int) -> list[float]:
    if df.empty or "amount" not in df.columns:
        return [0.0] * n
    df = df.dropna(subset=["event_timestamp"])
    df = df.sort_values("event_timestamp")
    df["bucket"] = pd.cut(df["event_timestamp"], bins=n, labels=False)
    sums = df.groupby("bucket")["amount"].sum().reindex(range(n), fill_value=0)
    return sums.tolist()
