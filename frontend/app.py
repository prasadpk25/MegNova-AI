import streamlit as st

from utils.auth import logout
from utils.session import initialize_session

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
    initial_sidebar_state="expanded",
)

# ==========================================================
# SESSION
# ==========================================================

initialize_session()

# ==========================================================
# LOGIN CHECK
# ==========================================================

if not st.session_state.logged_in:
    login_page()
    st.stop()
# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

/* Hide Streamlit Default */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main Container */

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Buttons */

.stButton>button{
    width:100%;
    height:45px;
    border-radius:10px;
    font-weight:600;
}

/* Metrics */

div[data-testid="metric-container"]{
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:14px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

/* Dataframes */

[data-testid="stDataFrame"]{
    border-radius:12px;
}

hr{
    margin-top:0.8rem;
    margin-bottom:0.8rem;
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:10px;">
            <h1 style="margin-bottom:0;">🏥</h1>
            <h2 style="margin-top:0;margin-bottom:5px;font-weight:700;">
                MegNova AI
            </h2>
            <p style="font-size:13px;color:#CBD5E1;">
                AI Hospital Digital Twin
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.success(
        f"🟢 {st.session_state.get('user_name', 'User')}"
    )

    st.caption(
        st.session_state.get("user_role", "Doctor")
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Patients",
            "📋 Patient Details",
            "👨‍⚕️ Doctors",
            "📄 Reports",
            "📤 Upload Reports",
            "📊 Analytics",
            "📚 Clinical Guidelines",
            "🤖 AI Assistant",
            "👤 Profile",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        type="secondary",
    ):
        logout()    
# ==========================================================
# PAGE ROUTING
# ==========================================================

PAGES = {
    "🏠 Dashboard": dashboard_page,
    "👤 Patients": patients_page,
    "📋 Patient Details": patient_detail_page,
    "👨‍⚕️ Doctors": doctors_page,
    "📄 Reports": reports_page,
    "📤 Upload Reports": upload_page,
    "📊 Analytics": analytics_page,
    "📚 Clinical Guidelines": clinical_guidelines_page,
    "🤖 AI Assistant": chatbot_page,
    "👤 Profile": profile_page,
    "⚙️ Settings": settings_page,
}

# ==========================================================
# LOAD SELECTED PAGE
# ==========================================================

try:

    page_function = PAGES.get(page)

    if page_function is None:
        st.warning("Selected page is unavailable.")
    else:
        page_function()

except Exception as e:

    st.error("⚠️ An unexpected error occurred.")

    with st.expander("Show Technical Details"):
        st.exception(e)

    st.info(
        """
If this problem persists, please verify:

• FastAPI backend is running
• PostgreSQL database is connected
• API endpoints are available
• Required Python packages are installed
• Selected page implementation has no syntax errors
"""
    )        
# ==========================================================
# FOOTER
# ==========================================================

st.divider()

left, center, right = st.columns([4, 2, 3])

with left:
    st.caption("🏥 MegNova AI • AI-Powered Hospital Digital Twin")

with center:
    st.caption("Version 1.0")

with right:
    st.caption("Powered by FastAPI • Streamlit • PostgreSQL")