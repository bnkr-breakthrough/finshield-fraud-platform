"""FinShield — Glassmorphism SOC Styles"""

import streamlit as st


def load_css() -> None:
    st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root Variables ───────────────────────────────────── */
:root {
  --bg-primary:   #0a0e1a;
  --bg-secondary: #0d1225;
  --bg-card:      rgba(13, 18, 37, 0.85);
  --bg-glass:     rgba(255,255,255,0.04);
  --border:       rgba(255,255,255,0.08);
  --border-glow:  rgba(99,179,237,0.3);

  --red:     #e53e3e;
  --red-dim: rgba(229,62,62,0.15);
  --blue:    #4299e1;
  --blue-dim:rgba(66,153,225,0.15);
  --purple:  #805ad5;
  --purple-dim:rgba(128,90,213,0.15);
  --orange:  #dd6b20;
  --orange-dim:rgba(221,107,32,0.15);
  --green:   #38a169;
  --amber:   #d69e2e;
  --teal:    #319795;

  --text-primary:   #f0f4ff;
  --text-secondary: #8892a4;
  --text-muted:     #4a5568;

  --font-main: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

/* ── Global Reset ─────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: var(--bg-primary) !important;
  font-family: var(--font-main) !important;
  color: var(--text-primary) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, .stDeployButton,
header[data-testid="stHeader"] { display: none !important; }

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: #080c18 !important;
  border-right: 1px solid var(--border) !important;
  width: 220px !important;
  min-width: 220px !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}

/* ── Logo Block ───────────────────────────────────────── */
.fs-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 16px 16px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 8px;
}
.fs-logo-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, #2b6cb0, #4299e1);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.fs-logo-text h3 {
  margin: 0; font-size: 15px; font-weight: 700;
  color: var(--text-primary); line-height: 1.2;
}
.fs-logo-text p {
  margin: 0; font-size: 10px; color: var(--text-secondary);
}

/* ── Nav Items ────────────────────────────────────────── */
.fs-nav { padding: 0 8px; }
.fs-nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  font-size: 13px; font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer; margin-bottom: 2px;
  transition: all 0.15s;
  position: relative;
}
.fs-nav-item:hover { background: var(--bg-glass); color: var(--text-primary); }
.fs-nav-item.active {
  background: var(--blue-dim);
  color: var(--blue);
  border: 1px solid rgba(66,153,225,0.2);
}
.fs-nav-badge {
  margin-left: auto;
  background: var(--red);
  color: #fff; font-size: 10px; font-weight: 700;
  padding: 2px 6px; border-radius: 10px;
}

/* ── Sidebar Section Labels ───────────────────────────── */
.fs-section-label {
  font-size: 10px; font-weight: 600; letter-spacing: 1px;
  color: var(--text-muted); text-transform: uppercase;
  padding: 12px 20px 4px;
}

/* ── System Status ────────────────────────────────────── */
.fs-status-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 20px; font-size: 12px; color: var(--text-secondary);
}
.fs-status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  flex-shrink: 0;
}
.fs-status-dot.healthy { background: var(--green); box-shadow: 0 0 6px var(--green); }
.fs-status-dot.warning { background: var(--amber); }
.fs-status-dot.error   { background: var(--red); }
.fs-status-label { color: var(--green); font-size: 11px; font-weight: 600; }

/* ── Main Content Wrapper ─────────────────────────────── */
.fs-main {
  display: flex; flex-direction: column;
  padding: 0; min-height: 100vh;
}

/* ── Top Bar ──────────────────────────────────────────── */
.fs-topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 28px;
  background: rgba(8,12,24,0.95);
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
  backdrop-filter: blur(12px);
}
.fs-topbar-left { display: flex; align-items: center; gap: 14px; }
.fs-topbar-icon {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, #c53030, #e53e3e);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
}
.fs-topbar-title h1 {
  margin: 0; font-size: 22px; font-weight: 800;
  color: var(--text-primary); line-height: 1.1;
}
.fs-topbar-title p {
  margin: 0; font-size: 12px; color: var(--text-secondary);
}
.fs-topbar-right { display: flex; align-items: center; gap: 20px; }

/* Live indicator */
.fs-live-badge {
  display: flex; align-items: center; gap: 6px;
  background: rgba(56,161,105,0.12);
  border: 1px solid rgba(56,161,105,0.3);
  border-radius: 20px; padding: 5px 12px;
  font-size: 12px; font-weight: 600; color: var(--green);
}
.fs-live-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green);
  animation: pulse-green 1.5s infinite;
}
@keyframes pulse-green {
  0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(56,161,105,0.6); }
  50%      { opacity:.7; box-shadow:0 0 0 5px rgba(56,161,105,0); }
}

.fs-topbar-chip {
  display: flex; align-items: center; gap: 6px;
  background: var(--bg-glass); border: 1px solid var(--border);
  border-radius: 8px; padding: 5px 12px;
  font-size: 12px; color: var(--text-secondary);
}
.fs-topbar-chip span { color: var(--text-primary); font-weight: 600; }

/* ── KPI Cards ────────────────────────────────────────── */
.fs-kpi-row {
  display: flex; gap: 14px;
  padding: 18px 28px 0;
}
.fs-kpi-card {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 18px;
  position: relative; overflow: hidden;
  backdrop-filter: blur(8px);
  transition: border-color .2s, transform .2s;
}
.fs-kpi-card:hover {
  border-color: var(--border-glow);
  transform: translateY(-1px);
}
.fs-kpi-card::before {
  content: '';
  position: absolute; top:0; left:0; right:0; height:2px;
}
.fs-kpi-card.blue::before   { background: linear-gradient(90deg,#4299e1,transparent); }
.fs-kpi-card.red::before    { background: linear-gradient(90deg,#e53e3e,transparent); }
.fs-kpi-card.purple::before { background: linear-gradient(90deg,#805ad5,transparent); }
.fs-kpi-card.orange::before { background: linear-gradient(90deg,#dd6b20,transparent); }
.fs-kpi-card.crimson::before{ background: linear-gradient(90deg,#c53030,transparent); }

.fs-kpi-header { display:flex; align-items:flex-start; justify-content:space-between; }
.fs-kpi-icon {
  width:36px; height:36px; border-radius:8px;
  display:flex; align-items:center; justify-content:center;
  font-size:16px;
}
.fs-kpi-icon.blue   { background:var(--blue-dim);   color:var(--blue);   }
.fs-kpi-icon.red    { background:var(--red-dim);    color:var(--red);    }
.fs-kpi-icon.purple { background:var(--purple-dim); color:var(--purple); }
.fs-kpi-icon.orange { background:var(--orange-dim); color:var(--orange); }
.fs-kpi-icon.crimson{ background:rgba(197,48,48,.15);color:#fc8181;       }

.fs-kpi-label {
  font-size:11px; color:var(--text-secondary);
  font-weight:500; letter-spacing:.3px; margin-bottom:4px;
}
.fs-kpi-value {
  font-size:26px; font-weight:800;
  color:var(--text-primary); line-height:1; margin-bottom:2px;
  font-family:var(--font-main);
}
.fs-kpi-sub {
  font-size:10px; color:var(--text-secondary);
  margin-bottom:8px;
}

/* sparkline placeholder */
.fs-sparkline {
  height:28px; width:100%;
  border-radius:4px; overflow:hidden;
  opacity:.7;
}

/* ── Live Alert Banner ────────────────────────────────── */
.fs-alert-banner {
  margin: 14px 28px 0;
  background: linear-gradient(135deg, rgba(197,48,48,0.12), rgba(229,62,62,0.06));
  border: 1px solid rgba(229,62,62,0.4);
  border-left: 4px solid var(--red);
  border-radius: 12px;
  padding: 14px 20px;
  display: flex; align-items: center; gap: 24px;
  position: relative; overflow: hidden;
  animation: border-pulse 2s infinite;
}
@keyframes border-pulse {
  0%,100% { border-color: rgba(229,62,62,0.4); }
  50%      { border-color: rgba(229,62,62,0.9); }
}
.fs-alert-left { display:flex; flex-direction:column; gap:2px; min-width:170px; }
.fs-alert-title {
  display:flex; align-items:center; gap:8px;
  font-size:15px; font-weight:800; color:var(--red); letter-spacing:.5px;
}
.fs-alert-bell { font-size:18px; animation: bell-shake 1s infinite; }
@keyframes bell-shake {
  0%,100%{transform:rotate(0)} 15%{transform:rotate(12deg)}
  30%{transform:rotate(-10deg)} 45%{transform:rotate(6deg)}
  60%{transform:rotate(-4deg)}
}
.fs-alert-sub { font-size:11px; color:rgba(229,62,62,0.7); }

.fs-alert-fields { display:flex; gap:28px; flex:1; }
.fs-alert-field label {
  display:block; font-size:10px; letter-spacing:.8px;
  color:var(--text-muted); text-transform:uppercase; margin-bottom:3px;
}
.fs-alert-field span {
  font-size:14px; font-weight:700; color:var(--text-primary);
  display:flex; align-items:center; gap:5px;
}

.fs-severity-badge {
  display:inline-flex; align-items:center; gap:5px;
  font-size:12px; font-weight:700; padding:2px 10px; border-radius:20px;
}
.fs-severity-badge.critical {
  background:rgba(229,62,62,0.2); color:var(--red);
  border:1px solid rgba(229,62,62,0.4);
}
.fs-severity-badge.high {
  background:rgba(221,107,32,0.2); color:var(--orange);
  border:1px solid rgba(221,107,32,0.4);
}
.fs-severity-badge.medium {
  background:rgba(214,158,46,0.2); color:var(--amber);
  border:1px solid rgba(214,158,46,0.4);
}
.fs-severity-badge.low {
  background:rgba(56,161,105,0.2); color:var(--green);
  border:1px solid rgba(56,161,105,0.4);
}

.fs-alert-btn {
  background: rgba(229,62,62,0.15);
  border: 1px solid rgba(229,62,62,0.4);
  color: var(--red); font-size:13px; font-weight:600;
  padding:8px 18px; border-radius:8px; cursor:pointer;
  transition: all .2s; white-space:nowrap;
  display:flex; align-items:center; gap:6px;
}
.fs-alert-btn:hover {
  background: var(--red); color:#fff;
}

/* ── Chart Grid ───────────────────────────────────────── */
.fs-charts-row {
  display:flex; gap:14px;
  padding: 14px 28px 0;
}
.fs-chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius:12px; padding:16px 18px;
  backdrop-filter:blur(8px);
  overflow:hidden;
}
.fs-chart-card.flex-1   { flex:1; }
.fs-chart-card.flex-1-5 { flex:1.5; }
.fs-chart-card.flex-2   { flex:2; }

.fs-card-title {
  display:flex; align-items:center; gap:8px;
  font-size:13px; font-weight:700; color:var(--text-primary);
  margin-bottom:12px;
}
.fs-card-title-icon {
  width:24px; height:24px; border-radius:6px;
  display:flex; align-items:center; justify-content:center;
  font-size:12px;
}

/* ── Table ────────────────────────────────────────────── */
.fs-table-wrap { overflow-x:auto; }
.fs-table {
  width:100%; border-collapse:collapse;
  font-size:12px;
}
.fs-table th {
  color:var(--text-muted); font-weight:600; font-size:11px;
  text-transform:uppercase; letter-spacing:.5px;
  padding:6px 10px; border-bottom:1px solid var(--border);
  text-align:left; white-space:nowrap;
}
.fs-table td {
  padding:8px 10px; border-bottom:1px solid rgba(255,255,255,0.03);
  color:var(--text-secondary); white-space:nowrap;
}
.fs-table tr:hover td { background:var(--bg-glass); color:var(--text-primary); }
.fs-table td:first-child { color:var(--text-primary); }

/* ── Footer ───────────────────────────────────────────── */
.fs-footer {
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 28px;
  border-top:1px solid var(--border);
  background:rgba(8,12,24,0.8);
  font-size:11px; color:var(--text-muted);
  margin-top:14px;
}
.fs-footer-chips { display:flex; gap:20px; flex-wrap:wrap; }
.fs-footer-chip  { display:flex; align-items:center; gap:5px; }
.fs-footer-chip span { color:var(--text-secondary); }

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.1); border-radius:2px; }

/* ── Plotly chart tweaks ──────────────────────────────── */
.js-plotly-plot .plotly { background:transparent !important; }
.stPlotlyChart { border-radius:8px; overflow:hidden; }

/* ── Streamlit element resets ─────────────────────────── */
.stMarkdown p { margin:0; }
div[data-testid="stHorizontalBlock"] { gap:0 !important; }

/* View All link style */
.fs-view-all {
  font-size:12px; color:var(--blue);
  text-decoration:none; font-weight:600;
  display:flex; align-items:center; gap:4px;
}
.fs-view-all:hover { color:#90cdf4; }
</style>
""", unsafe_allow_html=True)
