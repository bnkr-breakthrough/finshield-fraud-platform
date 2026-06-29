"""FinShield — Sidebar with Navigation"""

from __future__ import annotations
import streamlit as st


def render_sidebar(metrics: dict, fraud_df) -> dict:
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="fs-logo">
            <div class="fs-logo-icon">🛡️</div>
            <div class="fs-logo-text">
                <h3>FinShield</h3>
                <p>Fraud Detection Platform</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation using session state
        if "active_page" not in st.session_state:
            st.session_state.active_page = "Overview"

        critical = metrics.get("critical_alerts", 0)

        pages = [
            ("📊", "Overview",     None),
            ("🚨", "Fraud Alerts", critical),
            ("📈", "Analytics",    None),
            ("👥", "Customers",    None),
            ("🏪", "Merchants",    None),
            ("📉", "Trends",       None),
            ("📋", "Reports",      None),
            ("⚙️", "Settings",     None),
        ]

        for icon, page, badge in pages:
            active = st.session_state.active_page == page
            badge_html = f'<span class="fs-nav-badge">{badge}</span>' if badge else ""
            cls = "active" if active else ""

            clicked = st.button(
                f"{icon}  {page}",
                key=f"nav_{page}",
                use_container_width=True,
            )
            if clicked:
                st.session_state.active_page = page
                st.rerun()

        st.markdown('<div class="fs-section-label">Filters</div>',
                    unsafe_allow_html=True)

        cities = ["All Cities"]
        if not fraud_df.empty and "city" in fraud_df.columns:
            cities += sorted(fraud_df["city"].dropna().unique().tolist())
        selected_city = st.selectbox(
            "City", cities, label_visibility="collapsed")

        severities = ["All Severities", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
        selected_sev = st.selectbox(
            "Fraud Severity", severities, label_visibility="collapsed")

        st.button("🔄 Clear Filters", use_container_width=True,
                  key="clear_filters")

        # System Status
        st.markdown(
            '<div class="fs-section-label">System Status</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="fs-status-item"><span><span class="fs-status-dot healthy"></span> &nbsp;Kafka</span><span class="fs-status-label">Healthy</span></div>
        <div class="fs-status-item"><span><span class="fs-status-dot healthy"></span> &nbsp;PySpark</span><span class="fs-status-label">Healthy</span></div>
        <div class="fs-status-item"><span><span class="fs-status-dot healthy"></span> &nbsp;Streamlit</span><span class="fs-status-label">Healthy</span></div>
        <div class="fs-status-item"><span><span class="fs-status-dot healthy"></span> &nbsp;Data Pipeline</span><span class="fs-status-label">Healthy</span></div>
        <div class="fs-status-item"><span><span class="fs-status-dot healthy"></span> &nbsp;Snowflake</span><span class="fs-status-label">Healthy</span></div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="padding:16px 20px;font-size:10px;color:#4a5568;border-top:1px solid rgba(255,255,255,0.05);margin-top:24px;">
            v2.0.0 &nbsp;|&nbsp; FinShield © 2026<br>All rights reserved.
        </div>
        """, unsafe_allow_html=True)

    return {
        "city":     selected_city,
        "severity": selected_sev,
        "page":     st.session_state.active_page,
    }
