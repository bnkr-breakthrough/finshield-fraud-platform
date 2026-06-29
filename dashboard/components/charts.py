"""FinShield — All Chart Components"""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta


# ── shared config ─────────────────────────────────────────────────────────────
CHART_BG = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.05)"
TEXT_COLOR = "#8892a4"
FONT_FAMILY = "Inter, sans-serif"

BLUE = "#4299e1"
RED = "#e53e3e"
PURPLE = "#805ad5"
ORANGE = "#dd6b20"
GREEN = "#38a169"
AMBER = "#d69e2e"
TEAL = "#319795"
COLORS = [BLUE, PURPLE, GREEN, ORANGE, TEAL, AMBER, RED, "#ed64a6"]


def _base_layout(**kwargs) -> dict:
    return dict(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        **kwargs,
    )


def _card(title: str, icon: str, icon_bg: str = "#1a2035") -> None:
    st.markdown(f"""
    <div class="fs-card-title">
        <div class="fs-card-title-icon" style="background:{icon_bg}">{icon}</div>
        {title}
    </div>
    """, unsafe_allow_html=True)


# ── Row 1: Donut + Bar City + Bar Merchant ────────────────────────────────────

def render_severity_donut(fraud_df: pd.DataFrame) -> None:
    _card("Fraud Severity Distribution", "🛡️", "#1a2035")

    if fraud_df.empty or "fraud_severity" not in fraud_df.columns:
        st.info("No fraud data yet.")
        return

    counts = fraud_df["fraud_severity"].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()
    total = sum(values)

    color_map = {"CRITICAL": RED, "HIGH": ORANGE,
                 "MEDIUM": AMBER, "LOW": GREEN}
    colors = [color_map.get(l, BLUE) for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{total}</b><br><span style='font-size:10px'>Total</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, color="#f0f4ff", family=FONT_FAMILY),
        xanchor="center", yanchor="middle",
    )

    fig.update_layout(**_base_layout(height=220))
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

    # Legend
    for label, val in zip(labels, values):
        pct = val / total * 100 if total else 0
        dot_color = color_map.get(label, BLUE)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:12px">
            <span style="width:10px;height:10px;border-radius:50%;background:{dot_color};flex-shrink:0"></span>
            <span style="color:#8892a4">{label}</span>
            <span style="margin-left:auto;color:#f0f4ff;font-weight:600">{val:,} ({pct:.2f}%)</span>
        </div>
        """, unsafe_allow_html=True)


def render_city_bar(fraud_df: pd.DataFrame) -> None:
    _card("Fraud by City (Top 10)", "📍", "#1a1a3e")

    if fraud_df.empty or "city" not in fraud_df.columns:
        st.info("No data.")
        return

    top = fraud_df["city"].value_counts().head(10)

    fig = go.Figure(go.Bar(
        x=top.index.tolist(), y=top.values.tolist(),
        marker=dict(
            color=BLUE,
            line=dict(width=0),
        ),
        text=top.values.tolist(),
        textposition="outside",
        textfont=dict(color="#f0f4ff", size=10),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    ))

    fig.update_layout(
        **_base_layout(height=220),
        xaxis=dict(tickfont=dict(size=10, color=TEXT_COLOR),
                   gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(
            size=9, color=TEXT_COLOR)),
    )
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})


def render_merchant_bar(fraud_df: pd.DataFrame) -> None:
    _card("Fraud by Merchant (Top 5)", "🏪", "#2d1a3e")

    if fraud_df.empty or "merchant" not in fraud_df.columns:
        st.info("No data.")
        return

    top = fraud_df["merchant"].value_counts().head(5)

    fig = go.Figure(go.Bar(
        x=top.index.tolist(), y=top.values.tolist(),
        marker=dict(color=PURPLE, line=dict(width=0)),
        text=top.values.tolist(),
        textposition="outside",
        textfont=dict(color="#f0f4ff", size=10),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    ))
    fig.update_layout(
        **_base_layout(height=220),
        xaxis=dict(tickfont=dict(size=9, color=TEXT_COLOR),
                   gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(
            size=9, color=TEXT_COLOR)),
    )
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})


# ── Row 2: Table + Risk Customers ─────────────────────────────────────────────

def render_fraud_table(fraud_df: pd.DataFrame) -> None:
    _card("Latest Fraud Alerts", "🚨", "#2d1a1a")

    if fraud_df.empty:
        st.info("No fraud alerts.")
        return

    cols = ["event_timestamp", "customer_name", "city", "amount",
            "fraud_score", "fraud_severity", "fraud_reason"]
    available = [c for c in cols if c in fraud_df.columns]
    df = fraud_df[available].head(7).copy()

    # format
    if "amount" in df.columns:
        df["amount"] = df["amount"].apply(lambda x: f"₹ {float(x):,.2f}")
    if "event_timestamp" in df.columns:
        df["event_timestamp"] = df["event_timestamp"].apply(
            lambda x: str(x)[:16].replace("T", " ")
        )

    headers_map = {
        "event_timestamp": "Time", "customer_name": "Customer",
        "city": "City", "amount": "Amount (₹)", "fraud_score": "Score",
        "fraud_severity": "Severity", "fraud_reason": "Reason",
    }

    header_html = "".join(
        f"<th>{headers_map.get(c, c)}</th>" for c in available)

    color_map = {"CRITICAL": "#e53e3e", "HIGH": "#dd6b20",
                 "MEDIUM": "#d69e2e", "LOW": "#38a169"}

    rows_html = ""
    for _, row in df.iterrows():
        cells = ""
        for c in available:
            val = row.get(c, "")
            if c == "fraud_severity":
                col = color_map.get(str(val), "#8892a4")
                cells += f'<td><span class="fs-severity-badge" style="background:{col}22;color:{col};border:1px solid {col}44;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700">● {val}</span></td>'
            else:
                cells += f"<td>{val}</td>"
        rows_html += f"<tr>{cells}</tr>"

    st.markdown(f"""
    <div class="fs-table-wrap">
      <table class="fs-table">
        <thead><tr>{header_html}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    <div style="text-align:right;padding-top:8px">
        <a class="fs-view-all" href="#">View all alerts →</a>
    </div>
    """, unsafe_allow_html=True)


def render_risk_customers(fraud_df: pd.DataFrame) -> None:
    col1, col2 = st.columns([2, 1])
    with col1:
        _card("Top Risk Customers", "👥", "#1a2035")
    with col2:
        st.markdown(
            '<div style="text-align:right;padding-top:2px"><a class="fs-view-all" href="#">View All</a></div>', unsafe_allow_html=True)

    if fraud_df.empty or "customer_name" not in fraud_df.columns:
        st.info("No data.")
        return

    if "fraud_score" in fraud_df.columns:
        risk = (
            fraud_df.groupby("customer_name")["fraud_score"]
            .sum().sort_values(ascending=True).tail(10)
        )
    else:
        risk = fraud_df["customer_name"].value_counts().tail(10)

    fig = go.Figure(go.Bar(
        y=risk.index.tolist(),
        x=risk.values.tolist(),
        orientation="h",
        marker=dict(
            color=BLUE,
            line=dict(width=0),
        ),
        text=risk.values.tolist(),
        textposition="outside",
        textfont=dict(color="#f0f4ff", size=10),
        hovertemplate="<b>%{y}</b><br>Risk Score: %{x}<extra></extra>",
    ))
    fig.update_layout(
        **_base_layout(height=270),
        xaxis=dict(
            title="Risk Score", gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_COLOR),
        ),
        yaxis=dict(tickfont=dict(size=10, color="#f0f4ff")),
    )
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})


# ── Row 3: Reason Donut + 24h Trend + Severity Summary ───────────────────────

def render_reason_donut(fraud_df: pd.DataFrame) -> None:
    _card("Fraud Reason Analysis (Top 5)", "📊", "#1a2035")

    if fraud_df.empty or "fraud_reason" not in fraud_df.columns:
        st.info("No data.")
        return

    reasons = fraud_df["fraud_reason"].replace("", "OTHER_RULES")
    top5 = reasons.value_counts().head(5)
    total = top5.sum()

    fig = go.Figure(go.Pie(
        labels=top5.index.tolist(), values=top5.values.tolist(),
        hole=0.55,
        marker=dict(colors=COLORS[:5], line=dict(color="#0a0e1a", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value} (%{percent})<extra></extra>",
    ))
    fig.update_layout(**_base_layout(height=180))
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

    for i, (reason, val) in enumerate(top5.items()):
        pct = val / total * 100 if total else 0
        col = COLORS[i % len(COLORS)]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;font-size:11px">
            <span style="width:8px;height:8px;border-radius:2px;background:{col};flex-shrink:0"></span>
            <span style="color:#8892a4;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{reason}</span>
            <span style="color:#f0f4ff;font-weight:600;white-space:nowrap">{val} ({pct:.1f}%)</span>
        </div>
        """, unsafe_allow_html=True)


def render_trend_chart(all_df: pd.DataFrame, fraud_df: pd.DataFrame) -> None:
    _card("Fraud Trend (Last 24 Hours)", "📈", "#1a2a1a")

    if fraud_df.empty or "event_timestamp" not in fraud_df.columns:
        st.info("No trend data.")
        return

    df = fraud_df.copy()
    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"], errors="coerce")
    df = df.dropna(subset=["event_timestamp"])

    now = datetime.now()
    start = now - timedelta(hours=24)
    df = df[df["event_timestamp"] >= pd.Timestamp(start)]

    if df.empty:
        st.info("No data in last 24h.")
        return

    df["hour"] = df["event_timestamp"].dt.floor("h")
    hourly = df.groupby("hour").size().reset_index(name="count")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly["hour"], y=hourly["count"],
        mode="lines", fill="tozeroy",
        line=dict(color=TEAL, width=2, shape="spline"),
        fillcolor="rgba(49,151,149,0.12)",
        hovertemplate="%{x|%H:%M}<br>Frauds: %{y}<extra></extra>",
    ))
    fig.update_layout(
        **_base_layout(height=200),
        xaxis=dict(
            gridcolor=GRID_COLOR, tickformat="%H:%M",
            tickfont=dict(size=9, color=TEXT_COLOR),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_COLOR),
        ),
    )
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})


def render_severity_summary(metrics: dict) -> None:
    _card("Severity Summary", "🛡️", "#2d1a1a")

    crit = metrics.get("critical_alerts", 0)
    high = metrics.get("high_alerts",     0)
    med = metrics.get("medium_alerts",   0)
    low = metrics.get("low_alerts",      0)
    total = crit + high + med + low or 1

    items = [
        ("CRITICAL", crit,  "#e53e3e"),
        ("HIGH",     high,  "#dd6b20"),
        ("MEDIUM",   med,   "#d69e2e"),
        ("LOW",      low,   "#38a169"),
    ]

    for label, val, color in items:
        pct = val / total * 100
        st.markdown(f"""
        <div style="
            background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.06);
            border-radius:10px; padding:12px 14px;
            margin-bottom:8px; text-align:center;
            border-top:3px solid {color};
        ">
            <div style="font-size:11px;color:#8892a4;font-weight:600;letter-spacing:.5px">{label}</div>
            <div style="font-size:28px;font-weight:800;color:{color};line-height:1.1">{val:,}</div>
            <div style="font-size:12px;color:{color};font-weight:600">{pct:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
