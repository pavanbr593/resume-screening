def inject_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ─────────────────────────────────── */
:root {
    --bg:         #0A0C10;
    --surface:    #111318;
    --surface2:   #181C24;
    --border:     #1E2330;
    --border2:    #252D3D;
    --accent:     #4F8EF7;
    --accent2:    #7B5CF0;
    --accent3:    #00D4AA;
    --danger:     #F05454;
    --warn:       #F5A623;
    --text:       #E8ECF4;
    --text2:      #8892A4;
    --text3:      #4A5568;
    --radius:     12px;
    --radius-lg:  20px;
    --shadow:     0 4px 24px rgba(0,0,0,0.4);
    --shadow-lg:  0 8px 48px rgba(0,0,0,0.6);
    --font:       'Sora', sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

/* ── Global Reset ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit Branding ────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.viewerBadge_container__1QSob { display: none !important; }

/* ── Main App Container ─────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
    background: transparent !important;
}

/* ── Sidebar ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text2) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    display: block !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--border) !important;
    color: var(--text) !important;
}
section[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    background: rgba(79,142,247,0.15) !important;
    color: var(--accent) !important;
}

/* ── Headers ────────────────────────────────────────── */
h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, var(--text) 0%, var(--text2) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0.25rem !important;
}
h2 {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
}
h3 {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text2) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── Metric Cards ───────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.2s, transform 0.2s !important;
}
[data-testid="metric-container"]:hover {
    border-color: var(--accent) !important;
    transform: translateY(-2px) !important;
}
[data-testid="metric-container"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    right: 0 !important; height: 2px !important;
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--text2) !important;
}
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(79,142,247,0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(79,142,247,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text2) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--danger) !important;
    color: var(--danger) !important;
    background: rgba(240,84,84,0.08) !important;
}

/* ── Download Button ────────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--accent3) !important;
    color: var(--accent3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,212,170,0.1) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs & Text Areas ────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text3) !important;
}

/* ── Selectbox ──────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--accent) !important;
}

/* ── Slider ─────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {
    padding-top: 0.5rem !important;
}
.stSlider [data-testid="stThumbValue"] {
    background: var(--accent) !important;
    color: white !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
}
[data-baseweb="slider"] [data-testid="stSliderTrack"] {
    background: var(--border2) !important;
}

/* ── Tabs ───────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text2) !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* ── Dataframe / Table ──────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}
[data-testid="stDataFrameResizable"] {
    background: var(--surface) !important;
}

/* ── Expander ───────────────────────────────────────── */
.stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    margin-bottom: 0.75rem !important;
}
.stExpander header {
    background: var(--surface) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
}
.stExpander:hover {
    border-color: var(--border2) !important;
}

/* ── Alert / Info boxes ─────────────────────────────── */
.stSuccess, [data-testid="stSuccessMessage"] {
    background: rgba(0,212,170,0.1) !important;
    border: 1px solid rgba(0,212,170,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--accent3) !important;
}
.stWarning, [data-testid="stWarningMessage"] {
    background: rgba(245,166,35,0.1) !important;
    border: 1px solid rgba(245,166,35,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--warn) !important;
}
.stError, [data-testid="stErrorMessage"] {
    background: rgba(240,84,84,0.1) !important;
    border: 1px solid rgba(240,84,84,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--danger) !important;
}
.stInfo, [data-testid="stInfoMessage"] {
    background: rgba(79,142,247,0.08) !important;
    border: 1px solid rgba(79,142,247,0.25) !important;
    border-radius: var(--radius) !important;
    color: var(--accent) !important;
}

/* ── Progress Bar ───────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent3)) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 100px !important;
}

/* ── File Uploader ──────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border2) !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    background: rgba(79,142,247,0.05) !important;
}

/* ── Divider ────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text3); }

/* ── Caption / Small Text ───────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text3) !important;
    font-size: 0.78rem !important;
}

/* ── Form ───────────────────────────────────────────── */
[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
}

/* ── Checkbox ───────────────────────────────────────── */
.stCheckbox label {
    color: var(--text2) !important;
    font-size: 0.9rem !important;
}

/* ── Radio ──────────────────────────────────────────── */
.stRadio label {
    color: var(--text2) !important;
}

/* ── Page Title Accent ──────────────────────────────── */
.page-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.page-title-dot {
    width: 10px;
    height: 10px;
    background: var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 12px var(--accent);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
}

/* ── Score Badge ─────────────────────────────────────── */
.score-badge {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 100px;
    font-family: var(--mono);
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-green { background: rgba(0,212,170,0.15); color: var(--accent3); border: 1px solid rgba(0,212,170,0.3); }
.badge-blue  { background: rgba(79,142,247,0.15); color: var(--accent); border: 1px solid rgba(79,142,247,0.3); }
.badge-yellow{ background: rgba(245,166,35,0.15); color: var(--warn); border: 1px solid rgba(245,166,35,0.3); }
.badge-red   { background: rgba(240,84,84,0.15); color: var(--danger); border: 1px solid rgba(240,84,84,0.3); }

/* ── Sidebar Brand ───────────────────────────────────── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.25rem;
}
.sidebar-brand-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.sidebar-brand-name {
    font-size: 1rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
}
</style>
"""


LOGIN_PAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }

body {
    font-family: 'Sora', sans-serif;
    background: #0A0C10;
    color: #E8ECF4;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-wrapper {
    display: flex;
    width: 100%;
    min-height: 100vh;
}

/* Left Panel */
.login-left {
    flex: 1;
    background: #0A0C10;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: 5rem 6rem;
    position: relative;
    overflow: hidden;
}
.login-left::before {
    content: '';
    position: absolute;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.login-left::after {
    content: '';
    position: absolute;
    bottom: -150px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(123,92,240,0.1) 0%, transparent 70%);
    pointer-events: none;
}

.brand-mark {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 4rem;
}
.brand-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #4F8EF7, #7B5CF0);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 8px 24px rgba(79,142,247,0.4);
}
.brand-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #E8ECF4;
    letter-spacing: -0.02em;
}

.login-headline {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.04em;
    margin-bottom: 1.25rem;
}
.login-headline span {
    background: linear-gradient(135deg, #4F8EF7 0%, #00D4AA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.login-sub {
    color: #8892A4;
    font-size: 1.05rem;
    line-height: 1.6;
    max-width: 420px;
    margin-bottom: 3rem;
}

.feature-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.feature-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #8892A4;
    font-size: 0.9rem;
}
.feature-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F8EF7, #00D4AA);
    flex-shrink: 0;
}

/* Right Panel */
.login-right {
    width: 480px;
    background: #111318;
    border-left: 1px solid #1E2330;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem 3.5rem;
}

.login-form-title {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}
.login-form-sub {
    color: #8892A4;
    font-size: 0.9rem;
    margin-bottom: 2.5rem;
}

.input-group {
    margin-bottom: 1.25rem;
}
.input-label {
    display: block;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8892A4;
    margin-bottom: 0.5rem;
}
.login-input {
    width: 100%;
    background: #181C24;
    border: 1px solid #252D3D;
    border-radius: 10px;
    color: #E8ECF4;
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
    padding: 0.85rem 1.1rem;
    transition: all 0.2s;
    outline: none;
    -webkit-appearance: none;
}
.login-input:focus {
    border-color: #4F8EF7;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15);
}
.login-input::placeholder { color: #4A5568; }

.login-btn {
    width: 100%;
    background: linear-gradient(135deg, #4F8EF7 0%, #7B5CF0 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.9rem;
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 20px rgba(79,142,247,0.35);
    margin-top: 0.5rem;
}
.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(79,142,247,0.45);
}
.login-btn:active { transform: translateY(0); }

.login-error {
    background: rgba(240,84,84,0.1);
    border: 1px solid rgba(240,84,84,0.3);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #F05454;
    font-size: 0.875rem;
    margin-top: 1rem;
    font-weight: 500;
}
.login-hint {
    color: #4A5568;
    font-size: 0.78rem;
    text-align: center;
    margin-top: 2rem;
}

/* Grid decoration */
.grid-bg {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(79,142,247,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(79,142,247,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
}
</style>
"""
