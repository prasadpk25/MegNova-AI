import streamlit as st

from utils.session import initialize_session

# ==========================================================
# IMPORT COMPONENTS
# ==========================================================

from components.sidebar import sidebar

# ==========================================================
# IMPORT VIEWS
# ==========================================================

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

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="MegNova AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto",
)
st.sidebar.empty()

# ==========================================================
# SESSION
# ==========================================================

initialize_session()

# ==========================================================
# LOGIN
# ==========================================================

if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: visible;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    div[data-testid="metric-container"] {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# SIDEBAR
# ==========================================================

try:
    page = sidebar()
except Exception as e:
    st.error(e)
    page = "Dashboard"

# ==========================================================
# ROUTING
# ==========================================================

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

# ==========================================================
# LOAD PAGE
# ==========================================================

try:

    if page not in PAGES:
        st.warning(f"'{page}' page is not available.")
    else:
        PAGES[page]()

except Exception:
    st.error("⚠️ Something went wrong. Please refresh or try again later.")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

col1, col2, col3 = st.columns([4, 2, 3])

with col1:
    st.caption("🏥 MegNova AI • AI Hospital Digital Twin")

with col2:
    st.caption("Version 1.0")

with col3:
    st.caption("FastAPI • Streamlit • PostgreSQL")