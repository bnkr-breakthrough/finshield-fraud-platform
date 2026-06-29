"""FinShield — Top Bar Header"""

from __future__ import annotations
from datetime import datetime
import streamlit as st


def render_header() -> None:
    now = datetime.now()
    date_str = now.strftime("%d %b %Y")
    time_str = now.strftime("%I:%M %p")

    st.markdown(f"""
    <div class="fs-topbar">
        <div class="fs-topbar-left">
            <div class="fs-topbar-icon">🛡️</div>
            <div class="fs-topbar-title">
                <h1>Fraud Operations Center</h1>
                <p>Real-Time Financial Risk Monitoring &amp; Fraud Detection</p>
            </div>
        </div>
        <div class="fs-topbar-right">
            <div class="fs-live-badge">
                <div class="fs-live-dot"></div>
                LIVE<br><span style="font-size:10px;font-weight:400">Streaming...</span>
            </div>
            <div class="fs-topbar-chip">
                📅 &nbsp;<span>{date_str}<br><small style="font-size:11px">{time_str}</small></span>
            </div>
            <div class="fs-topbar-chip">
                🔄 &nbsp;<span>Auto Refresh<br><small style="font-size:11px">10 sec</small></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
