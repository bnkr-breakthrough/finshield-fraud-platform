"""FinShield — KPI Cards with Sparklines"""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go


def _sparkline_fig(data: list, color: str) -> go.Figure:
    # Convert hex color to rgba for fill
    hex_to_rgba = {
        "#4299e1": "rgba(66,153,225,0.12)",
        "#e53e3e": "rgba(229,62,62,0.12)",
        "#805ad5": "rgba(128,90,213,0.12)",
        "#dd6b20": "rgba(221,107,32,0.12)",
    }
    fill_color = hex_to_rgba.get(color, "rgba(66,153,225,0.12)")

    fig = go.Figure(go.Scatter(
        y=data, mode="lines",
        line=dict(color=color, width=1.5, shape="spline"),
        fill="tozeroy",
        fillcolor=fill_color,
    ))
    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=0),
        height=30, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def render_kpi_cards(metrics: dict) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)

    total  = metrics.get("total_transactions", 0)
    frauds = metrics.get("fraud_transactions",  0)
    pct    = metrics.get("fraud_percentage",     0)
    amt    = metrics.get("fraud_amount",         0)
    crit   = metrics.get("critical_alerts",      0)

    sp_total  = metrics.get("sparkline_total",  [0]*20)
    sp_fraud  = metrics.get("sparkline_fraud",  [0]*20)
    sp_amount = metrics.get("sparkline_amount", [0]*20)

    cards = [
        (c1, "Total Transactions", f"{total:,}",        "All Time",            "📊", "blue",   "#4299e1", sp_total),
        (c2, "Fraud Transactions", f"{frauds:,}",       "All Time",            "⚠️", "red",    "#e53e3e", sp_fraud),
        (c3, "Fraud Percentage",   f"{pct:.2f}%",       "Of Total Transactions","📉","purple", "#805ad5", sp_fraud),
        (c4, "Fraud Amount",       f"₹ {amt:,.0f}",    "Total Fraud Amount",  "💰", "orange", "#dd6b20", sp_amount),
        (c5, "Critical Alerts",    f"{crit:,}",         "High Priority",       "🚨", "crimson","#e53e3e", sp_fraud),
    ]

    for col, label, value, sub, icon, cls, color, spark in cards:
        with col:
            st.markdown(f"""
            <div class="fs-kpi-card {cls}">
                <div class="fs-kpi-header">
                    <div>
                        <div class="fs-kpi-label">{label}</div>
                        <div class="fs-kpi-value">{value}</div>
                        <div class="fs-kpi-sub">{sub}</div>
                    </div>
                    <div class="fs-kpi-icon {cls}">{icon}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(
                _sparkline_fig(spark, color),
                use_container_width=True,
                config={"displayModeBar": False},
                key=f"spark_{cls}",
            )
