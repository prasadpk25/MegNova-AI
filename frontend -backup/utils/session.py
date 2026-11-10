import streamlit as st

DEFAULT_SESSION = {
    "logged_in": False,
    "access_token": None,
    "user": None,
    "selected_patient": None,
    "selected_report": None,
}

def initialize_session():
    for key, value in DEFAULT_SESSION.items():
        if key not in st.session_state:
            st.session_state[key] = value