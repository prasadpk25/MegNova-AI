import streamlit as st

from utils.session import initialize_session
from components.sidebar import sidebar

from views.login import login_page
from views.dashboard import dashboard_page
from views.patients import patients_page
from views.patients_details import patient_detail_page
from views.doctors import doctors_page
from views.reports import reports_page
from views.upload import upload_page
from views.analytics import analytics_page
from views.chatbot import chatbot_page
from views.clinical_guidelines import clinical_guidelines_page
from views.profile import profile_page
from views.settings import settings_page

st.set_page_config(
    page_title="MegNova AI | Hospital Digital Twin",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
  --mn-ink: #15263b;
  --mn-muted: #718096;
  --mn-teal: #0e9384;
  --mn-teal-dark: #08796f;
  --mn-line: #e6edf2;
  --mn-bg: #f4f7fa;
  --mn-card: #ffffff;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  color: var(--mn-ink);
}
.stApp { background: var(--mn-bg); }
header[data-testid="stHeader"] { background: rgba(244,247,250,.88); }
#MainMenu, footer { visibility: hidden; }
.block-container {
  max-width: 1500px;
  padding-top: 2rem;
  padding-bottom: 3rem;
  padding-left: 2.4rem;
  padding-right: 2.4rem;
}
h1, h2, h3, h4 {
  font-family: 'Manrope', sans-serif !important;
  color: var(--mn-ink) !important;
  letter-spacing: -0.035em;
}
h1 { font-size: clamp(1.8rem, 2.5vw, 2.35rem) !important; font-weight: 800 !important; }
h2 { font-size: 1.45rem !important; font-weight: 750 !important; }
h3 { font-size: 1.12rem !important; font-weight: 750 !important; }
p, label, .stCaption { color: #5f7083; }
[data-testid="stSidebar"] {
  background: #10253a;
  border-right: 1px solid #1d3850;
}
[data-testid="stSidebar"] > div:first-child { background: #10253a; }
[data-testid="stSidebar"] * { color: #e9f2f7; }
[data-testid="stSidebar"] hr { border-color: #294258; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #a9bdcb; }
[data-testid="stSidebar"] .stButton button {
  background: #18364d; color: #f5fbff; border: 1px solid #31536b;
}
[data-testid="stSidebar"] .stButton button:hover { background: #214963; border-color: #4b7993; }
[data-testid="stSidebar"] [data-testid="stAlert"] {
  background: #17374a; border: 1px solid #2c5968; color: #d9f7ef;
}
[data-testid="stSidebar"] [data-testid="stAlert"] p { color: #d9f7ef; }
[data-testid="stSidebar"] .nav-link {
  border-radius: 10px !important; margin: 3px 0; color: #c3d2dc !important;
  font-weight: 600; transition: all .18s ease;
}
[data-testid="stSidebar"] .nav-link:hover { background: #1b3b52 !important; color: white !important; }
[data-testid="stSidebar"] .nav-link.active {
  background: linear-gradient(100deg, #0e9384, #08796f) !important;
  color: #ffffff !important; box-shadow: 0 7px 18px rgba(5, 130, 117, .22);
}
[data-testid="stSidebar"] .nav-link i { color: inherit !important; }
[data-testid="stMetric"] {
  background: var(--mn-card); border: 1px solid var(--mn-line);
  border-radius: 16px; padding: 18px 20px; box-shadow: 0 5px 18px rgba(25,48,70,.035);
}
[data-testid="stMetricLabel"] { color: #718096 !important; font-size: .83rem; font-weight: 700; }
[data-testid="stMetricValue"] { color: var(--mn-ink) !important; font-family: 'Manrope',sans-serif; font-weight: 800; }
[data-testid="stVerticalBlockBorderWrapper"] {
  border-radius: 16px; border-color: var(--mn-line); background: white;
}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: 10px; min-height: 2.65rem; font-weight: 700;
  border: 1px solid #d8e3e9; transition: all .18s ease;
}
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
  background: var(--mn-teal); border-color: var(--mn-teal); color: white;
}
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
  background: var(--mn-teal-dark); border-color: var(--mn-teal-dark); color: white;
  box-shadow: 0 6px 16px rgba(14,147,132,.18);
}
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"],
.stMultiSelect [data-baseweb="select"], .stDateInput input, .stNumberInput input {
  border-radius: 10px; border-color: #dce6ec; background: #fff;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--mn-teal); }
[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--mn-line); border-radius: 13px; overflow: hidden;
}
[data-testid="stTabs"] button { font-weight: 700; }
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--mn-teal) !important; }
[data-testid="stExpander"] { border: 1px solid var(--mn-line); border-radius: 12px; background: white; }
[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: var(--mn-line); }
.mn-topbar {
  display:flex; align-items:center; justify-content:space-between; gap:16px;
  padding: 13px 18px; margin: 0 0 25px 0; background:#fff;
  border:1px solid var(--mn-line); border-radius:15px;
  box-shadow:0 4px 15px rgba(25,48,70,.025);
}
.mn-brand { display:flex; align-items:center; gap:11px; }
.mn-brand-mark {
  display:grid; place-items:center; width:39px; height:39px; border-radius:12px;
  background:linear-gradient(145deg,#12a594,#08796f); color:white; font-size:20px;
}
.mn-brand-name { font:800 15px 'Manrope',sans-serif; color:#15263b; }
.mn-brand-sub { color:#8292a2; font-size:11px; margin-top:1px; }
.mn-live { color:#168575; font-size:12px; font-weight:700; background:#e9f7f3; padding:7px 11px; border-radius:30px; }
.mn-eyebrow { color:#0e9384; font-size:11px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.mn-login-card { background:white; border:1px solid var(--mn-line); border-radius:20px; padding:30px; box-shadow:0 15px 45px rgba(21,38,59,.08); }
@media (max-width: 800px) {
  .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
  .mn-topbar { padding: 10px 12px; }
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)
initialize_session()

if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()

user_name = st.session_state.get("user_name", "Care Team")
st.markdown(
    f"""
    <div class="mn-topbar">
      <div class="mn-brand">
        <div class="mn-brand-mark">✚</div>
        <div>
          <div class="mn-brand-name">MegNova AI</div>
          <div class="mn-brand-sub">Hospital Digital Twin</div>
        </div>
      </div>
      <div class="mn-live">● Workspace active&nbsp;&nbsp; · &nbsp;&nbsp;{user_name}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES = {
    "Dashboard": dashboard_page,
    "Patients": patients_page,
    "Patient Details": patient_detail_page,
    "Doctors": doctors_page,
    "Reports": reports_page,
    "Upload Reports": upload_page,
    "Analytics": analytics_page,
    "Clinical Guidelines": clinical_guidelines_page,
    "AI Assistant": chatbot_page,
    "Profile": profile_page,
    "Settings": settings_page,
}

try:
    page = sidebar()
except Exception as error:
    st.error(f"Navigation could not be loaded: {error}")
    page = "Dashboard"

try:
    if page not in PAGES:
        st.warning(f"'{page}' page is not available.")
    else:
        PAGES[page]()
except Exception as error:
    st.error("This page could not be loaded. Please refresh and try again.")
    st.exception(error)

st.markdown(
    """
    <div style="margin-top:34px;padding-top:16px;border-top:1px solid #e4ebf0;
      display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;
      color:#8795a3;font-size:11px;">
      <span>© 2026 MegNova AI · Clinical Decision Support Workspace</span>
      <span>FastAPI&nbsp; · &nbsp;PostgreSQL&nbsp; · &nbsp;Qdrant</span>
    </div>
    """,
    unsafe_allow_html=True,
)
