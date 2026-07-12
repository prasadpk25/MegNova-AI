import streamlit as st

def login_page():

    st.title("🏥 AI Hospital Digital Twin")

    st.markdown("### Secure Clinical Decision Support System")

    st.divider()

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    st.checkbox("Remember Me")

    if st.button("🔐 Login", use_container_width=True):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Invalid Username or Password")