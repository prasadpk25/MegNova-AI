import streamlit as st


def handle_response(response):

    if response.status_code in (200, 201):
        return response.json()

    if response.status_code == 401:
        st.error("Session expired. Please login again.")
        st.session_state.clear()
        st.stop()

    try:
        st.error(response.json()["detail"])
    except Exception:
        st.error("Unexpected Server Error")

    return None