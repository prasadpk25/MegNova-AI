import streamlit as st

# -----------------------------
# Import Pages
# -----------------------------
from views.login import login_page
from views.dashboard import dashboard_page
from views.patients import patients_page
from views.reports import reports_page
from views.chatbot import chatbot_page

from components.sidebar import sidebar

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Hospital Digital Twin",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# Login Page
# -----------------------------
if not st.session_state.logged_in:
    login_page()

# -----------------------------
# Main Application
# -----------------------------
else:

    menu = sidebar()

    if menu == "Dashboard":
        dashboard_page()

    elif menu == "Patients":
        patients_page()

    elif menu == "Reports":
        reports_page()

    elif menu == "Upload":
        st.title("📤 Upload")
        st.info("Upload module is under development.")

    elif menu == "AI Assistant":
        chatbot_page()

    elif menu == "Drug Checker":
        st.title("💊 Drug Checker")
        st.info("Drug Checker module is under development.")

    elif menu == "Medical Search":
        st.title("🔍 Medical Search")
        st.info("Medical Search (RAG) module is under development.")

    elif menu == "Analytics":
        st.title("📊 Analytics")
        st.info("Analytics module is under development.")

    elif menu == "Settings":
        st.title("⚙️ Settings")
        st.info("Settings module is under development.")

    elif menu == "Profile":
        st.title("👤 Profile")
        st.info("Profile module is under development.")

    else:
        st.warning("Page not found.")