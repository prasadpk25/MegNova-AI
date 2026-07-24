import streamlit as st

# =====================================
# Import Pages
# =====================================
from views.login import login_page
from views.dashboard import dashboard_page
from views.patients import patients_page
from views.reports import reports_page
from views.chatbot import chatbot_page
from views.clinical_guidelines import clinical_guidelines_page
from views.analytics import analytics_page
from views.doctors import doctors_page
from components.sidebar import sidebar

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="MegNova AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================
# Session State
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================================
# Login Screen
# =====================================

if not st.session_state.logged_in:
    login_page()
    st.stop()

# =====================================
# Sidebar
# =====================================

menu = sidebar()

# =====================================
# Routing
# =====================================

if menu == "Dashboard":
    dashboard_page()

elif menu == "Patients":
    patients_page()
elif menu == "Doctors":
    doctors_page()
elif menu == "Reports":
    reports_page()

elif menu == "AI Assistant":
    chatbot_page()

elif menu == "Clinical Guidelines":
    clinical_guidelines_page()

elif menu == "Analytics":
    analytics_page()

elif menu == "Upload Reports":
    st.title("📤 Upload Medical Reports")
    st.info("Upload module coming soon.")

elif menu == "Drug Interaction":
    st.title("💊 Drug Interaction Checker")
    st.info("Drug Interaction module coming soon.")

elif menu == "Patient Timeline":
    st.title("🕒 Patient Timeline")
    st.info("Timeline module coming soon.")

elif menu == "Medical Search":
    st.title("🔍 Medical Literature Search")
    st.info("Medical Search module coming soon.")

elif menu == "Settings":
    st.title("⚙️ Settings")
    st.info("Settings module coming soon.")

elif menu == "Profile":
    st.title("👤 User Profile")
    st.info("Profile module coming soon.")   

else:
    st.error("❌ Page not found.")