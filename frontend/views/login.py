import streamlit as st
from utils.api import login


def login_page():

    st.title("🏥 MegNova AI")
    st.caption("AI-Powered Smart Hospital Management System")

    st.markdown("### Secure Clinical Decision Support System")

    st.divider()

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔒 Password",
        type="password",
    )

    remember = st.checkbox("Remember Me")

    if st.button("🔐 Login", use_container_width=True):

        response = login(email, password)

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.logged_in = True
            st.session_state.access_token = token

            st.success("Login Successful")

            st.rerun()

        else:

            st.error(response.json()["detail"])