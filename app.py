"""
Resume Screening — Premium AI-Powered Hiring Platform
Light theme · Sora font · Industry-grade UI
"""

import json
import streamlit as st
import pandas as pd

from database import (
    init_db, save_job, update_job, get_all_jobs, get_job, get_job_skills,
    delete_job, save_candidate, get_candidates_for_job, get_candidate, save_score,
    delete_candidates_for_job, audit
)
from auth import (
    require_auth, logout, seed_default_users,
    is_authenticated, current_role, login
)
from resume_parser import parse_resume
from scoring_engine import score_candidate, recommendation_label
from ai_summary import generate_ai_summary
from bias_detector import detect_bias, format_category
from report_generator import generate_excel_report, generate_candidate_pdf_report
from encryption import sanitize_filename

# ── Bootstrap ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Screening",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)
init_db()
seed_default_users()

# ── Design System ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ───────────────────────────────── */
:root {
    --bg:          #F5F7FA;
    --surface:     #FFFFFF;
    --surface2:    #F8FAFC;
    --border:      #E4E8F0;
    --border2:     #CBD5E1;
    --accent:      #4F8EF7;
    --accent2:     #7B5CF0;
    --accent3:     #059669;
    --danger:      #DC2626;
    --warn:        #D97706;
    --text:        #0F172A;
    --text2:       #475569;
    --text3:       #94A3B8;
    --radius:      10px;
    --radius-lg:   16px;
    --shadow-sm:   0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow:      0 4px 16px rgba(0,0,0,0.07);
    --shadow-lg:   0 8px 32px rgba(0,0,0,0.1);
    --font:        'Sora', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono:        'JetBrains Mono', monospace;
}

/* ── Global Reset ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

.main .block-container {
    padding: 2.5rem 3rem 5rem !important;
    max-width: 1340px !important;
    background: transparent !important;
}

/* ── Sidebar ──────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E4E8F0 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.75rem 1.25rem !important;
}
section[data-testid="stSidebar"] * { color: #475569 !important; }

/* ── Sidebar Radio Nav ────────────────────────────── */
section[data-testid="stSidebar"] .stRadio > label { display: none !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 2px !important;
}
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center;
    padding: 0.58rem 0.85rem !important;
    border-radius: 8px !important;
    font-size: 0.875rem !important; font-weight: 500 !important;
    color: #475569 !important;
    transition: background 0.15s, color 0.15s !important;
    cursor: pointer !important; width: 100%;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #F1F5F9 !important;
    color: #0F172A !important;
}
section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: #EFF6FF !important;
    color: #2563EB !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #E4E8F0 !important;
    margin: 1rem 0 !important;
}

/* ── Page typography ──────────────────────────────── */
.page-eyebrow {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #4F8EF7;
    margin-bottom: 0.3rem;
}
.page-title {
    font-size: 1.75rem; font-weight: 800; letter-spacing: -0.035em;
    color: #0F172A; line-height: 1.15; margin-bottom: 0.35rem;
}
.page-meta {
    font-size: 0.83rem; color: #64748B; font-weight: 400;
    margin-bottom: 2rem; line-height: 1.55;
}

/* ── Stat cards ───────────────────────────────────── */
.stat-card {
    background: #FFFFFF; border: 1px solid #E4E8F0;
    border-radius: var(--radius-lg); padding: 1.375rem 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.18s, transform 0.18s;
    position: relative; overflow: hidden;
}
.stat-card::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.stat-card.blue::after  { background: linear-gradient(90deg, #4F8EF7, #7B5CF0); }
.stat-card.green::after { background: linear-gradient(90deg, #059669, #10B981); }
.stat-card.purple::after{ background: linear-gradient(90deg, #7B5CF0, #A78BFA); }
.stat-card.dark::after  { background: linear-gradient(90deg, #0F172A, #334155); }
.stat-card:hover { box-shadow: var(--shadow); transform: translateY(-2px); }
.stat-val {
    font-family: var(--mono); font-size: 1.9rem; font-weight: 700;
    letter-spacing: -0.04em; line-height: 1; margin-bottom: 0.3rem;
    color: #0F172A;
}
.stat-val.blue   { color: #2563EB; }
.stat-val.green  { color: #059669; }
.stat-val.purple { color: #7C3AED; }
.stat-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #94A3B8;
}

/* ── Section label ────────────────────────────────── */
.section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #94A3B8;
    border-bottom: 1px solid #F1F5F9; padding-bottom: 0.55rem;
    margin: 1.75rem 0 1.1rem;
}

/* ── Cards ────────────────────────────────────────── */
.rs-card {
    background: #FFFFFF; border: 1px solid #E4E8F0;
    border-radius: var(--radius-lg); padding: 1.5rem 1.75rem;
    box-shadow: var(--shadow-sm);
}

/* ── Badge system ─────────────────────────────────── */
.badge {
    display: inline-flex; align-items: center;
    padding: 0.18rem 0.65rem; border-radius: 999px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; font-family: var(--mono);
}
.badge-green  { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.badge-blue   { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
.badge-amber  { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }
.badge-red    { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }

/* ── Skill tags ───────────────────────────────────── */
.tag-match {
    display: inline-flex; align-items: center;
    background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE;
    border-radius: 5px; padding: 0.18rem 0.55rem;
    font-size: 0.76rem; font-weight: 500; margin: 0.15rem;
}
.tag-miss {
    display: inline-flex; align-items: center;
    background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA;
    border-radius: 5px; padding: 0.18rem 0.55rem;
    font-size: 0.76rem; font-weight: 500; margin: 0.15rem;
}

/* ── Candidate row ────────────────────────────────── */
.cand-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #FFFFFF; border: 1px solid #E4E8F0; border-radius: 10px;
    padding: 0.9rem 1.25rem; margin-bottom: 0.45rem;
    transition: box-shadow 0.15s, border-color 0.15s;
}
.cand-row:hover { box-shadow: var(--shadow); border-color: #CBD5E1; }
.cand-name { font-weight: 600; color: #0F172A; font-size: 0.88rem; }
.cand-score {
    font-family: var(--mono); font-size: 1.05rem; font-weight: 700;
    letter-spacing: -0.02em;
}

/* ── Hero profile card ────────────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border-radius: var(--radius-lg); padding: 1.75rem 2rem;
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 1.5rem; box-shadow: var(--shadow-lg);
}
.hero-name {
    font-size: 1.25rem; font-weight: 800; color: #F8FAFC;
    letter-spacing: -0.025em; margin-bottom: 0.3rem;
}
.hero-sub { font-size: 0.78rem; color: #64748B; }
.hero-score-val {
    font-family: var(--mono); font-size: 3.4rem; font-weight: 700;
    line-height: 1; letter-spacing: -0.05em;
}
.hero-score-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #64748B; margin-top: 0.35rem;
    text-align: right;
}

/* ── Score mini grid ──────────────────────────────── */
.score-mini-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.875rem; margin-bottom: 1.75rem; }
.score-mini {
    background: #FFFFFF; border: 1px solid #E4E8F0; border-radius: 10px;
    padding: 1rem 1.125rem; box-shadow: var(--shadow-sm);
}
.score-mini-val {
    font-family: var(--mono); font-size: 1.6rem; font-weight: 700;
    letter-spacing: -0.04em; line-height: 1;
}
.score-mini-label {
    font-size: 0.67rem; font-weight: 700; color: #94A3B8;
    letter-spacing: 0.07em; text-transform: uppercase; margin-top: 0.2rem;
}
.bar-track { background: #F1F5F9; border-radius: 3px; height: 4px; margin-top: 8px; }
.bar-fill  { height: 100%; border-radius: 3px; }

/* ── Bias flag ────────────────────────────────────── */
.bias-wrap {
    background: #FFFBEB; border: 1px solid #FDE68A;
    border-left: 3px solid #F59E0B; border-radius: 8px;
    padding: 0.7rem 1rem; margin-bottom: 0.5rem;
}
.bias-cat  { font-size: 0.66rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #92400E; }
.bias-text { font-size: 0.82rem; font-weight: 600; color: #B45309; margin-top: 0.1rem; }
.bias-ctx  { font-size: 0.78rem; color: #78716C; margin-top: 0.2rem; line-height: 1.5; }

/* ── Summary box ──────────────────────────────────── */
.summary-wrap {
    background: #F8FAFC; border: 1px solid #E4E8F0; border-radius: 10px;
    padding: 1.25rem 1.5rem; font-size: 0.85rem; line-height: 1.8;
    color: #334155; white-space: pre-wrap; font-family: var(--font);
}

/* ── Tabs (underline style) ───────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #E4E8F0 !important;
    border-radius: 0 !important; padding: 0 !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 0 !important;
    color: #64748B !important; font-weight: 500 !important;
    font-size: 0.84rem !important; padding: 0.65rem 1.25rem !important;
    border-bottom: 2px solid transparent !important; margin-bottom: -1px !important;
    font-family: var(--font) !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important; color: #2563EB !important;
    border-bottom-color: #2563EB !important; font-weight: 600 !important;
}

/* ── Inputs ───────────────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: #FFFFFF !important; border: 1px solid #D1D5DB !important;
    border-radius: 8px !important; color: #0F172A !important;
    font-family: var(--font) !important; font-size: 0.875rem !important;
    padding: 0.6rem 0.875rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #4F8EF7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.12) !important;
    outline: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #9CA3AF !important; }

/* ── Selectbox ────────────────────────────────────── */
.stSelectbox > div > div {
    background: #FFFFFF !important; border: 1px solid #D1D5DB !important;
    border-radius: 8px !important; color: #0F172A !important;
    font-family: var(--font) !important; font-size: 0.875rem !important;
}
.stSelectbox > div > div:focus-within { border-color: #4F8EF7 !important; }

/* ── Slider ───────────────────────────────────────── */
.stSlider [data-baseweb="slider"] [role="slider"] { background: #4F8EF7 !important; }

/* ── Buttons ──────────────────────────────────────── */
.stButton > button {
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.855rem !important; font-family: var(--font) !important;
    transition: all 0.15s !important; letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"] {
    background: #2563EB !important; border-color: #2563EB !important; color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1D4ED8 !important; border-color: #1D4ED8 !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.28) !important; transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important; border: 1px solid #D1D5DB !important; color: #374151 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #F9FAFB !important; border-color: #9CA3AF !important;
}

/* ── Download button ──────────────────────────────── */
.stDownloadButton > button {
    background: #FFFFFF !important; border: 1px solid #059669 !important;
    color: #059669 !important; border-radius: 8px !important;
    font-weight: 600 !important; font-family: var(--font) !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: #ECFDF5 !important; transform: translateY(-1px) !important;
}

/* ── Progress bar ─────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4F8EF7, #7B5CF0) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    background: #E4E8F0 !important; border-radius: 100px !important;
}

/* ── File uploader ────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 2px dashed #CBD5E1 !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.75rem 2rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #4F8EF7 !important;
    background: #F8FBFF !important;
}

/* ── Alerts ───────────────────────────────────────── */
[data-testid="stSuccessMessage"] {
    background: #ECFDF5 !important; border: 1px solid #A7F3D0 !important;
    border-radius: var(--radius) !important; color: #065F46 !important;
}
[data-testid="stWarningMessage"] {
    background: #FFFBEB !important; border: 1px solid #FDE68A !important;
    border-radius: var(--radius) !important; color: #92400E !important;
}
[data-testid="stErrorMessage"] {
    background: #FEF2F2 !important; border: 1px solid #FECACA !important;
    border-radius: var(--radius) !important; color: #991B1B !important;
}
[data-testid="stInfoMessage"] {
    background: #EFF6FF !important; border: 1px solid #BFDBFE !important;
    border-radius: var(--radius) !important; color: #1D4ED8 !important;
}

/* ── Dataframe ────────────────────────────────────── */
.stDataFrame {
    border: 1px solid #E4E8F0 !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important; box-shadow: var(--shadow-sm) !important;
}

/* ── Expander ─────────────────────────────────────── */
.stExpander {
    background: #FFFFFF !important; border: 1px solid #E4E8F0 !important;
    border-radius: var(--radius) !important; margin-bottom: 0.6rem !important;
    box-shadow: var(--shadow-sm) !important;
}
.stExpander header { color: #0F172A !important; font-weight: 600 !important; }
.stExpander:hover { border-color: #CBD5E1 !important; }

/* ── Form ─────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #FFFFFF !important; border: 1px solid #E4E8F0 !important;
    border-radius: var(--radius-lg) !important; padding: 1.5rem !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Divider ──────────────────────────────────────── */
hr { border-color: #F1F5F9 !important; margin: 1.75rem 0 !important; }

/* ── Scrollbar ────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #F8FAFC; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* ── Caption ──────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] { color: #94A3B8 !important; font-size: 0.77rem !important; }

/* ── Sidebar brand ────────────────────────────────── */
.sb-brand {
    display: flex; align-items: center; gap: 0.65rem;
    margin-bottom: 0.3rem;
}
.sb-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #4F8EF7 0%, #7B5CF0 100%);
    border-radius: 9px; display: flex; align-items: center;
    justify-content: center; font-size: 0.95rem; color: white;
    box-shadow: 0 4px 12px rgba(79,142,247,0.3); flex-shrink: 0;
}
.sb-name {
    font-size: 0.95rem; font-weight: 800; color: #0F172A !important;
    letter-spacing: -0.02em; line-height: 1.2;
}
.sb-name span { color: #4F8EF7 !important; }
.sb-user {
    font-size: 0.7rem; font-weight: 600; color: #94A3B8 !important;
    letter-spacing: 0.06em; text-transform: uppercase; padding-left: 0.1rem;
    margin-bottom: 1.25rem;
}
.sb-nav-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #CBD5E1 !important; padding: 0 0.2rem;
    margin-bottom: 0.4rem; margin-top: 0.25rem;
}

/* ── Login page ───────────────────────────────────── */
.login-hero {
    text-align: center; padding: 3rem 0 0.75rem;
}
.login-logo {
    font-size: 2rem; font-weight: 800; letter-spacing: -0.04em;
    color: #0F172A; display: inline-flex; align-items: center; gap: 0.4rem;
}
.login-logo-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: linear-gradient(135deg, #4F8EF7, #7B5CF0);
    display: inline-block; margin-bottom: 6px;
}
.login-logo em { color: #4F8EF7; font-style: normal; }
.login-tagline { font-size: 0.85rem; color: #94A3B8; margin-top: 0.4rem; }
.login-card {
    background: #FFFFFF; border: 1px solid #E4E8F0;
    border-radius: 18px; padding: 2.25rem 2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.04);
}
.login-card-title {
    font-size: 1rem; font-weight: 700; color: #0F172A; margin-bottom: 1.25rem;
}
.login-security {
    font-size: 0.7rem; color: #CBD5E1; text-align: center;
    margin-top: 1rem; letter-spacing: 0.04em;
    display: flex; align-items: center; justify-content: center; gap: 0.4rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────
def score_color(s):
    if s >= 75: return "#059669"
    if s >= 60: return "#2563EB"
    if s >= 45: return "#D97706"
    return "#DC2626"

def rec_badge(score):
    rec = recommendation_label(score)
    cls = {"Strongly Recommended": "badge-green", "Recommended": "badge-blue",
           "Consider": "badge-amber", "Not Recommended": "badge-red"}.get(rec, "badge-amber")
    return f'<span class="badge {cls}">{rec}</span>'

def mini_bar(val, color):
    pct = max(0, min(100, val or 0))
    return (f'<div class="bar-track"><div class="bar-fill" '
            f'style="width:{pct}%;background:{color};"></div></div>')

def job_selector(label="Select position"):
    jobs = get_all_jobs()
    if not jobs:
        st.info("No positions configured yet. Go to Job Configuration to add one.")
        st.stop()
    opts = {f"{j['title']}  ·  #{j['id']}": j["id"] for j in jobs}
    return opts[st.selectbox(label, list(opts.keys()))]


# ═══════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════
if not is_authenticated():
    st.markdown("""
    <div class="login-hero">
        <div class="login-logo">
            Resume<em>Screening</em><span class="login-logo-dot"></span>
        </div>
        <div class="login-tagline">AI-powered candidate screening &amp; ranking platform</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-card-title">Sign in to your workspace</div>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            sub = st.form_submit_button("Continue", use_container_width=True, type="primary")

        if sub:
            result = login(username, password)
            if result == "locked":
                st.error("Account locked — too many failed attempts. Try again in 5 minutes.")
            elif result is True:
                st.rerun()
            else:
                st.error("Incorrect username or password.")

        st.markdown("""
        <div class="login-security">
            <span>&#128274;</span>
            bcrypt &nbsp;·&nbsp; AES-256 Fernet &nbsp;·&nbsp; HMAC-SHA256 sessions
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
        <div class="sb-icon">◈</div>
        <div>
            <div class="sb-name">Resume<span>Screening</span></div>
        </div>
    </div>
    <div class="sb-user">{st.session_state["username"]} &nbsp;·&nbsp; {current_role()}</div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["Dashboard", "Job Configuration", "Upload Resumes", "Candidate Detail"],
        label_visibility="collapsed",
    )

    st.divider()
    if st.button("Sign Out", use_container_width=True, type="secondary"):
        audit(st.session_state.get("user_id"), "LOGOUT", st.session_state.get("username", ""))
        logout()
        st.rerun()


# ═══════════════════════════════════════════════════════════════════
# PAGE — DASHBOARD
# ═══════════════════════════════════════════════════════════════════
if page == "Dashboard":
    require_auth()

    st.markdown('<div class="page-eyebrow">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Candidate Rankings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-meta">Ranked results for the selected position. Filter by score, review candidates, and export reports.</div>', unsafe_allow_html=True)

    job_id = job_selector("Position")
    job = get_job(job_id)
    if not job:
        st.stop()

    candidates = get_candidates_for_job(job_id)
    scored = [c for c in candidates if c.get("final_score") is not None]

    if not scored:
        st.markdown('<div class="rs-card" style="text-align:center;padding:3rem;color:#94A3B8;">No scored candidates yet — upload and process resumes first.</div>', unsafe_allow_html=True)
        st.stop()

    scores = [c["final_score"] for c in scored]
    shortlisted = sum(1 for s in scores if s >= 60)

    col1, col2, col3, col4 = st.columns(4)
    for col, label, val, cls in [
        (col1, "Total Applicants", str(len(scored)), "dark"),
        (col2, "Average Score",    f"{sum(scores)/len(scores):.1f}", "blue"),
        (col3, "Top Score",        f"{max(scores):.1f}", "green"),
        (col4, "Shortlisted",      str(shortlisted), "purple"),
    ]:
        with col:
            st.markdown(f"""<div class="stat-card {cls}">
                <div class="stat-val {cls}">{val}</div>
                <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    col_f, _ = st.columns([1, 3])
    with col_f:
        min_score = st.slider("Minimum score", 0, 100, 0, step=5)

    filtered = sorted(
        [c for c in scored if c["final_score"] >= min_score],
        key=lambda x: x["final_score"], reverse=True
    )

    st.markdown(f'<div class="section-label">Results — {len(filtered)} of {len(scored)} candidates</div>', unsafe_allow_html=True)

    if filtered:
        display_rows = []
        cand_id_map = {}
        for rank, c in enumerate(filtered, 1):
            display_rows.append({
                "Rank": rank,
                "Name": c["filename"],
                "Score": round(c["final_score"], 1),
                "Skills": round(c.get("skill_score") or 0, 1),
                "Experience": round(c.get("experience_score") or 0, 1),
                "Semantic": round(c.get("semantic_score") or 0, 1),
                "Exp (yrs)": round(c.get("experience_years") or 0, 1),
                "Verdict": recommendation_label(c["final_score"]),
            })
            cand_id_map[c["filename"]] = c["id"]

        df = pd.DataFrame(display_rows)
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100),
                         "Skills": st.column_config.ProgressColumn("Skills", min_value=0, max_value=100),
                     })

        st.markdown('<div class="section-label">Open Profile</div>', unsafe_allow_html=True)
        cs, cb = st.columns([4, 1])
        with cs:
            sel = st.selectbox("Candidate", list(cand_id_map.keys()), label_visibility="collapsed")
        with cb:
            if st.button("View Profile", type="primary", use_container_width=True):
                st.session_state["view_candidate_id"] = cand_id_map[sel]
                st.session_state["view_job_id"] = job_id
                st.rerun()

    st.divider()
    cex, _ = st.columns([1, 5])
    with cex:
        if st.button("Export to Excel", use_container_width=True):
            try:
                data = generate_excel_report(filtered, job["title"])
                st.download_button("Download",
                    data=data,
                    file_name=f"{job['title'].replace(' ','_')}_rankings.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except Exception as e:
                st.error(str(e))


# ═══════════════════════════════════════════════════════════════════
# PAGE — JOB CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
elif page == "Job Configuration":
    require_auth()

    st.markdown('<div class="page-eyebrow">Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Job Positions</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-meta">Define job requirements, required skills, and scoring parameters for each open position.</div>', unsafe_allow_html=True)

    tab_new, tab_edit, tab_all = st.tabs(["New Position", "Edit Position", "All Positions"])

    with tab_new:
        col_left, col_right = st.columns([2, 1], gap="large")

        with col_left:
            st.markdown('<div class="section-label">Position Details</div>', unsafe_allow_html=True)
            with st.form("new_job"):
                title = st.text_input("Job Title", placeholder="e.g. Senior Backend Engineer")
                description = st.text_area("Job Description", height=175,
                                           placeholder="Paste the full job description here…")
                required_exp = st.number_input("Required Experience (years)", min_value=0.0, step=0.5, value=2.0)

                st.markdown('<div class="section-label">Required Skills</div>', unsafe_allow_html=True)
                if "new_skills" not in st.session_state:
                    st.session_state["new_skills"] = [{"name": "", "weight": 1.0}]

                collected = []
                for i, sk in enumerate(st.session_state["new_skills"]):
                    r1, r2 = st.columns([3, 1])
                    sn = r1.text_input(f"Skill {i+1}", value=sk["name"], key=f"ns_{i}", placeholder="e.g. Python")
                    sw = r2.number_input("Wt", min_value=0.1, max_value=5.0, value=sk["weight"], step=0.1, key=f"nw_{i}")
                    collected.append({"name": sn, "weight": sw})

                save_btn = st.form_submit_button("Save Position", type="primary", use_container_width=True)

            ca, cr = st.columns(2)
            if ca.button("+ Add Skill", use_container_width=True):
                st.session_state["new_skills"].append({"name": "", "weight": 1.0})
                st.rerun()
            if cr.button("− Remove Last", use_container_width=True) and len(st.session_state["new_skills"]) > 1:
                st.session_state["new_skills"].pop()
                st.rerun()

        with col_right:
            st.markdown('<div class="section-label">Scoring Weights</div>', unsafe_allow_html=True)
            st.caption("Controls how each dimension contributes to the final score. Normalized automatically.")
            w_sk = st.slider("Skill Match",     0.0, 1.0, 0.4, 0.05)
            w_ex = st.slider("Experience",      0.0, 1.0, 0.2, 0.05)
            w_se = st.slider("Semantic Fit",    0.0, 1.0, 0.3, 0.05)
            w_qu = st.slider("Resume Quality",  0.0, 1.0, 0.1, 0.05)
            tw = w_sk + w_ex + w_se + w_qu
            c = "#059669" if 0.9 <= tw <= 1.1 else "#DC2626"
            st.markdown(f'<div style="font-size:0.78rem;font-weight:700;color:{c};margin-top:0.3rem;font-family:var(--mono);">Sum: {tw:.2f}</div>', unsafe_allow_html=True)

        if save_btn:
            if not title.strip() or not description.strip():
                st.error("Title and description are required.")
            else:
                skills_dict = {s["name"]: s["weight"] for s in collected if s["name"].strip()}
                flags = detect_bias(description)
                if flags:
                    st.warning(f"Bias detected in job description — {len(flags)} flag(s).")
                    for f in flags:
                        st.markdown(f'<div class="bias-wrap"><div class="bias-cat">{format_category(f["category"])}</div><div class="bias-text">"{f["phrase"]}"</div><div class="bias-ctx">{f["context"]}</div></div>', unsafe_allow_html=True)

                jid = save_job(title, description, required_exp, w_sk, w_ex, w_se, w_qu,
                               skills_dict, st.session_state.get("user_id"))
                audit(st.session_state.get("user_id"), "CREATE_JOB", f"id={jid}")
                st.session_state["new_skills"] = [{"name": "", "weight": 1.0}]
                st.success(f"Position saved (#{jid}).")
                st.rerun()

    with tab_edit:
        jobs = get_all_jobs()
        if not jobs:
            st.info("No positions yet.")
        else:
            opts = {f"{j['title']}  ·  #{j['id']}": j["id"] for j in jobs}
            ek = st.selectbox("Select position to edit", list(opts.keys()))
            eid = opts[ek]
            ejob = get_job(eid)
            eskills = get_job_skills(eid)

            cl, cr = st.columns([2, 1], gap="large")
            with cl:
                with st.form("edit_job"):
                    et = st.text_input("Job Title", value=ejob["title"])
                    ed = st.text_area("Job Description", value=ejob["description"], height=175)
                    ee = st.number_input("Required Experience", value=ejob["required_experience"], step=0.5)
                    st.markdown('<div class="section-label">Skills</div>', unsafe_allow_html=True)
                    upd = []
                    for i, (sn, sw) in enumerate(eskills.items()):
                        r1, r2 = st.columns([3, 1])
                        n = r1.text_input(f"Skill {i+1}", value=sn, key=f"es_{eid}_{i}")
                        w = r2.number_input("Wt", value=sw, step=0.1, min_value=0.1, key=f"ew_{eid}_{i}")
                        upd.append((n, w))
                    esub = st.form_submit_button("Update Position", type="primary")
            with cr:
                st.markdown('<div class="section-label">Score Weights</div>', unsafe_allow_html=True)
                ewsk = st.slider("Skill Match",    0.0, 1.0, ejob["skill_weight"],       0.05, key="ewsk")
                ewex = st.slider("Experience",     0.0, 1.0, ejob["experience_weight"],  0.05, key="ewex")
                ewse = st.slider("Semantic Fit",   0.0, 1.0, ejob["semantic_weight"],    0.05, key="ewse")
                ewqu = st.slider("Resume Quality", 0.0, 1.0, ejob["quality_weight"],     0.05, key="ewqu")

            if esub:
                update_job(eid, et, ed, ee, ewsk, ewex, ewse, ewqu,
                           {n: w for n, w in upd if n.strip()})
                audit(st.session_state.get("user_id"), "UPDATE_JOB", f"id={eid}")
                st.success("Position updated.")
                st.rerun()

            st.divider()
            if st.button("Delete Position", type="secondary"):
                delete_job(eid)
                audit(st.session_state.get("user_id"), "DELETE_JOB", f"id={eid}")
                st.success("Deleted.")
                st.rerun()

    with tab_all:
        jobs = get_all_jobs()
        if not jobs:
            st.info("No positions configured yet.")
        else:
            for j in jobs:
                with st.expander(f"{j['title']}  ·  #{j['id']}  ·  {j['required_experience']} yrs exp"):
                    g1, g2, g3, g4 = st.columns(4)
                    g1.metric("Skill Wt",    j["skill_weight"])
                    g2.metric("Exp Wt",      j["experience_weight"])
                    g3.metric("Semantic Wt", j["semantic_weight"])
                    g4.metric("Quality Wt",  j["quality_weight"])
                    sk = get_job_skills(j["id"])
                    if sk:
                        st.markdown(" ".join(f'<span class="tag-match">{k} ({v})</span>' for k, v in sk.items()), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE — UPLOAD RESUMES
# ═══════════════════════════════════════════════════════════════════
elif page == "Upload Resumes":
    require_auth()

    st.markdown('<div class="page-eyebrow">Processing</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Upload Resumes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-meta">Upload PDF or DOCX files. Each resume is parsed, scored across all dimensions, and ranked automatically. Resume text is encrypted at rest.</div>', unsafe_allow_html=True)

    job_id = job_selector("Position")
    job = get_job(job_id)
    skills = get_job_skills(job_id)

    if not skills:
        st.warning("This position has no skills defined. Edit the position to add required skills before uploading.")

    col_up, col_act = st.columns([4, 1], gap="medium")
    with col_up:
        uploaded_files = st.file_uploader(
            "Upload resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
    with col_act:
        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
        if st.button("Clear All", use_container_width=True, type="secondary"):
            delete_candidates_for_job(job_id)
            audit(st.session_state.get("user_id"), "CLEAR_CANDIDATES", f"job_id={job_id}")
            st.success("Candidates cleared.")
            st.rerun()

    if uploaded_files:
        st.markdown(f'<div style="font-size:0.78rem;color:#94A3B8;margin:0.3rem 0 0.75rem;">{len(uploaded_files)} file(s) ready to process</div>', unsafe_allow_html=True)

        if st.button("Process All Resumes", type="primary"):
            bar = st.progress(0, text="Preparing…")
            results = []
            total = len(uploaded_files)

            for i, f in enumerate(uploaded_files):
                bar.progress(i / total, text=f"Parsing {f.name}  ({i+1}/{total})…")
                raw = f.read()
                clean_name = sanitize_filename(f.name)
                text = parse_resume(clean_name, raw)
                if text.startswith("["):
                    st.warning(f"Skipped {clean_name}: {text}")
                    continue

                cid = save_candidate(job_id, clean_name, text)
                bd = score_candidate(text, job, skills)
                summary = generate_ai_summary(
                    text, job["description"],
                    bd["matched_skills"], bd["missing_skills"],
                    bd["experience_years"], job["required_experience"], bd["final_score"]
                )
                bflags = detect_bias(text)
                save_score(cid, bd["skill_score"], bd["experience_score"], bd["semantic_score"],
                           bd["quality_score"], bd["final_score"], bd["matched_skills"],
                           bd["missing_skills"], bd["experience_years"], summary, bflags)
                results.append((clean_name, bd["final_score"]))

            bar.progress(1.0, text="Complete")
            audit(st.session_state.get("user_id"), "UPLOAD_RESUMES", f"job_id={job_id} count={len(results)}")
            st.success(f"{len(results)} resume(s) processed and scored.")

            st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
            for name, score in sorted(results, key=lambda x: -x[1]):
                clr = score_color(score)
                st.markdown(f"""
                <div class="cand-row">
                    <div class="cand-name">{name}</div>
                    <div style="display:flex;align-items:center;gap:0.875rem;">
                        <div class="cand-score" style="color:{clr};">{score:.1f}</div>
                        {rec_badge(score)}
                    </div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE — CANDIDATE DETAIL
# ═══════════════════════════════════════════════════════════════════
elif page == "Candidate Detail":
    require_auth()

    st.markdown('<div class="page-eyebrow">Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Candidate Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-meta">Full scoring breakdown, skill gap analysis, AI-generated summary, and exportable report.</div>', unsafe_allow_html=True)

    jobs = get_all_jobs()
    if not jobs:
        st.info("No positions configured yet.")
        st.stop()

    job_opts = {f"{j['title']}  ·  #{j['id']}": j["id"] for j in jobs}
    pre_jid = st.session_state.get("view_job_id")
    def_jkey = next((k for k, v in job_opts.items() if v == pre_jid), list(job_opts.keys())[0])
    job_id = job_opts[st.selectbox("Position", list(job_opts.keys()),
                                    index=list(job_opts.keys()).index(def_jkey))]
    job = get_job(job_id)

    candidates = get_candidates_for_job(job_id)
    scored = sorted([c for c in candidates if c.get("final_score") is not None],
                    key=lambda x: x["final_score"], reverse=True)
    if not scored:
        st.info("No scored candidates. Upload and process resumes first.")
        st.stop()

    cand_opts = {c["filename"]: c["id"] for c in scored}
    pre_cid = st.session_state.pop("view_candidate_id", None)
    all_names = list(cand_opts.keys())
    def_name = next((k for k, v in cand_opts.items() if v == pre_cid), all_names[0])
    selected = st.selectbox("Candidate", all_names, index=all_names.index(def_name))
    cid = cand_opts[selected]

    c = get_candidate(cid)
    if not c:
        st.error("Candidate record not found.")
        st.stop()

    matched = json.loads(c.get("matched_skills") or "[]")
    missing = json.loads(c.get("missing_skills") or "[]")
    bflags  = json.loads(c.get("bias_flags")     or "[]")
    fs  = c.get("final_score") or 0
    fsc = score_color(fs)

    # ── Hero card ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-wrap">
        <div>
            <div class="hero-name">{c['filename']}</div>
            <div class="hero-sub">{c.get('experience_years') or 0:.1f} years experience detected &nbsp;·&nbsp; {job['title']}</div>
            <div style="margin-top:0.9rem;">{rec_badge(fs)}</div>
        </div>
        <div>
            <div class="hero-score-val" style="color:{fsc};">{fs:.1f}</div>
            <div class="hero-score-label">Final Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Mini score cards ───────────────────────────────────────
    st.markdown(f"""
    <div class="score-mini-grid">
        <div class="score-mini">
            <div class="score-mini-val" style="color:#2563EB;">{(c.get('skill_score') or 0):.1f}</div>
            <div class="score-mini-label">Skill Match</div>
            {mini_bar(c.get('skill_score') or 0, '#2563EB')}
        </div>
        <div class="score-mini">
            <div class="score-mini-val" style="color:#059669;">{(c.get('experience_score') or 0):.1f}</div>
            <div class="score-mini-label">Experience</div>
            {mini_bar(c.get('experience_score') or 0, '#059669')}
        </div>
        <div class="score-mini">
            <div class="score-mini-val" style="color:#D97706;">{(c.get('semantic_score') or 0):.1f}</div>
            <div class="score-mini-label">Semantic Fit</div>
            {mini_bar(c.get('semantic_score') or 0, '#D97706')}
        </div>
        <div class="score-mini">
            <div class="score-mini-val" style="color:#7C3AED;">{(c.get('quality_score') or 0):.1f}</div>
            <div class="score-mini-label">Resume Quality</div>
            {mini_bar(c.get('quality_score') or 0, '#7C3AED')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────
    t1, t2, t3, t4, t5 = st.tabs(["Breakdown", "Skills", "AI Summary", "Resume", "Bias"])

    with t1:
        try:
            import plotly.graph_objects as go
            vals = [c.get("skill_score") or 0, c.get("experience_score") or 0,
                    c.get("semantic_score") or 0, c.get("quality_score") or 0]
            fig = go.Figure(go.Bar(
                x=["Skill Match", "Experience", "Semantic Fit", "Quality"],
                y=vals,
                marker_color=["#2563EB", "#059669", "#D97706", "#7C3AED"],
                text=[f"{v:.1f}" for v in vals],
                textposition="outside", width=0.4,
            ))
            fig.update_layout(
                yaxis_range=[0, 118], plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                height=290, margin=dict(t=20, b=10, l=10, r=10),
                xaxis=dict(showgrid=False, tickfont=dict(family="Sora", size=12, color="#374151")),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(family="Sora", color="#94A3B8")),
                font=dict(family="Sora", color="#374151"),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Install plotly for chart visualization.")

        st.dataframe(pd.DataFrame({
            "Metric": ["Skill Match", "Experience", "Semantic Fit", "Quality", "Final Score"],
            "Score": [round(c.get("skill_score") or 0, 1), round(c.get("experience_score") or 0, 1),
                      round(c.get("semantic_score") or 0, 1), round(c.get("quality_score") or 0, 1),
                      round(fs, 1)]
        }), use_container_width=True, hide_index=True)

    with t2:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<div class="section-label">Matched Skills</div>', unsafe_allow_html=True)
            if matched:
                st.markdown(" ".join(f'<span class="tag-match">{s}</span>' for s in matched), unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.75rem;color:#94A3B8;margin-top:0.75rem;">{len(matched)} of {len(matched)+len(missing)} skills present</div>', unsafe_allow_html=True)
            else:
                st.caption("None of the required skills were found.")
        with right:
            st.markdown('<div class="section-label">Missing Skills</div>', unsafe_allow_html=True)
            if missing:
                st.markdown(" ".join(f'<span class="tag-miss">{s}</span>' for s in missing), unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#059669;font-weight:600;font-size:0.84rem;">All required skills present.</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="section-label">AI-Generated Analysis</div>', unsafe_allow_html=True)
        summary = c.get("ai_summary", "")
        if summary:
            st.markdown(f'<div class="summary-wrap">{summary}</div>', unsafe_allow_html=True)
        else:
            st.caption("No summary available. Re-process this candidate to generate one.")

    with t4:
        st.markdown('<div class="section-label">Parsed Resume Content</div>', unsafe_allow_html=True)
        st.text_area("", value=c.get("raw_text", ""), height=420,
                     disabled=True, label_visibility="collapsed")

    with t5:
        st.markdown('<div class="section-label">Bias Detection</div>', unsafe_allow_html=True)
        if bflags:
            st.warning(f"{len(bflags)} potential indicator(s) detected.")
            for f in bflags:
                st.markdown(f'<div class="bias-wrap"><div class="bias-cat">{format_category(f["category"])}</div><div class="bias-text">"{f["phrase"]}"</div><div class="bias-ctx">{f["context"]}</div></div>', unsafe_allow_html=True)
        else:
            st.success("No bias indicators detected in this resume.")

    # ── Export ─────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="section-label">Export Report</div>', unsafe_allow_html=True)
    ex1, ex2, _ = st.columns([1, 1, 4])
    with ex1:
        try:
            pdf = generate_candidate_pdf_report(c, job["title"])
            st.download_button("Download PDF", data=pdf,
                               file_name=f"{c['filename'].rsplit('.',1)[0]}_report.pdf",
                               mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(str(e))
    with ex2:
        try:
            xl = generate_excel_report([c], job["title"])
            st.download_button("Download Excel", data=xl,
                               file_name=f"{c['filename'].rsplit('.',1)[0]}_report.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        except Exception as e:
            st.error(str(e))
