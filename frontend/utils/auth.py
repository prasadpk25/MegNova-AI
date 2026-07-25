import streamlit as st


def is_logged_in():
    return st.session_state.get("logged_in", False)


def get_token():
    return st.session_state.get("access_token")


import streamlit as st

def logout():
    keys = [
        "logged_in",
        "access_token",
        "user",
        "user_name",
        "user_role",
        "selected_patient",
        "selected_report",
        "remember_me",
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.rerun()
