"""FinShield — Live Fraud Alert Banner"""

from __future__ import annotations
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


def render_live_alert(fraud_df: pd.DataFrame) -> None:
    if fraud_df.empty:
        customer = "No Fraud Detected"
        amount = "₹ 0"
        city = "—"
        severity = "—"
        sev_cls = "low"
        alert_time = datetime.now().strftime("%H:%M:%S")
    else:
        latest = (
            fraud_df
            .sort_values("event_timestamp", ascending=True)
            .iloc[-1]
        )
        customer = latest.get("customer_name", "Unknown")
        amount = f"₹ {float(latest.get('amount', 0)):,.0f}"
        city = latest.get("city", "—")
        severity = latest.get("fraud_severity", "HIGH")
        sev_cls = severity.lower() if severity.lower() in (
            "critical", "high", "medium", "low") else "high"
        ts = latest.get("event_timestamp", "")
        try:
            alert_time = str(ts).split(" ")[1].split(".")[0]
        except Exception:
            alert_time = datetime.now().strftime("%H:%M:%S")

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:transparent; font-family:'Inter',sans-serif; }}
    .banner {{
        display:flex; align-items:center; gap:20px;
        background:linear-gradient(135deg,rgba(197,48,48,0.15),rgba(229,62,62,0.06));
        border:1px solid rgba(229,62,62,0.5);
        border-left:4px solid #e53e3e;
        border-radius:12px; padding:14px 20px;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%,100% {{ border-color:rgba(229,62,62,0.4); }}
        50%      {{ border-color:rgba(229,62,62,1); }}
    }}
    .left {{ min-width:160px; }}
    .title {{
        display:flex; align-items:center; gap:8px;
        font-size:15px; font-weight:800; color:#e53e3e;
        letter-spacing:.5px;
    }}
    .bell {{ animation: shake 1s infinite; display:inline-block; }}
    @keyframes shake {{
        0%,100%{{transform:rotate(0)}} 15%{{transform:rotate(12deg)}}
        30%{{transform:rotate(-10deg)}} 45%{{transform:rotate(6deg)}}
    }}
    .sub {{ font-size:11px; color:rgba(229,62,62,0.7); margin-top:2px; }}
    .fields {{ display:flex; gap:24px; flex:1; }}
    .field label {{
        display:block; font-size:10px; letter-spacing:.8px;
        color:#4a5568; text-transform:uppercase; margin-bottom:3px;
    }}
    .field span {{
        font-size:13px; font-weight:700; color:#f0f4ff;
    }}
    .badge {{
        display:inline-flex; align-items:center; gap:4px;
        font-size:12px; font-weight:700;
        padding:2px 10px; border-radius:20px;
    }}
    .critical {{ background:rgba(229,62,62,0.2); color:#e53e3e; border:1px solid rgba(229,62,62,0.4); }}
    .high     {{ background:rgba(221,107,32,0.2); color:#dd6b20; border:1px solid rgba(221,107,32,0.4); }}
    .medium   {{ background:rgba(214,158,46,0.2); color:#d69e2e; border:1px solid rgba(214,158,46,0.4); }}
    .low      {{ background:rgba(56,161,105,0.2); color:#38a169; border:1px solid rgba(56,161,105,0.4); }}
    .btn {{
        background:rgba(229,62,62,0.15); border:1px solid rgba(229,62,62,0.4);
        color:#e53e3e; font-size:13px; font-weight:600;
        padding:8px 16px; border-radius:8px; cursor:pointer;
        white-space:nowrap;
    }}
    .btn:hover {{ background:#e53e3e; color:#fff; }}
    </style>
    </head>
    <body>
    <div class="banner">
        <div class="left">
            <div class="title"><span class="bell">🔔</span> LIVE FRAUD ALERT</div>
            <div class="sub">High Priority Fraud Detected</div>
        </div>
        <div class="fields">
            <div class="field"><label>Customer</label><span>👤 {customer}</span></div>
            <div class="field"><label>Amount</label><span>💰 {amount}</span></div>
            <div class="field"><label>City</label><span>📍 {city}</span></div>
            <div class="field"><label>Severity</label><span><span class="badge {sev_cls}">● {severity}</span></span></div>
            <div class="field"><label>Time</label><span>🕐 {alert_time}</span></div>
        </div>
        <button class="btn">View Alert →</button>
    </div>
    </body>
    </html>
    """, height=80, scrolling=False)
