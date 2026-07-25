import streamlit as st

from utils.api import login


def login_page():
    """User Login Page"""

    # =====================================
    # Header
    # =====================================

    st.title("🏥 MegNova AI")
    st.caption("AI-Powered Hospital Digital Twin")

    st.markdown(
        """
        ### 🔐 Secure Clinical Decision Support System

        Login to access patients, reports, AI assistant,
        analytics, and hospital management tools.
        """
    )

    st.divider()

    # =====================================
    # Login Form
    # =====================================

    with st.form("login_form"):

        email = st.text_input(
            "📧 Email",
            placeholder="doctor@hospital.com",
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
        )

        remember = st.checkbox("Remember Me")

        submitted = st.form_submit_button(
            "🔐 Login",
            use_container_width=True,
        )

    # =====================================
    # Login
    # =====================================

    if submitted:

        # Basic Validation
        if not email.strip():
            st.warning("Please enter your email.")
            return

        if not password.strip():
            st.warning("Please enter your password.")
            return

        with st.spinner("Authenticating..."):

            try:
                response = login(email, password)

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.logged_in = True
                    st.session_state.access_token = data["access_token"]

                    # Optional (recommended if returned by backend)
                    st.session_state.user_name = data.get(
                        "full_name",
                        "Doctor",
                    )

                    st.session_state.user_role = data.get(
                        "role",
                        "Doctor",
                    )

                    if remember:
                        st.session_state.remember_me = True

                    st.success("✅ Login Successful")

                    st.rerun()

                else:

                    try:
                        message = response.json().get(
                            "detail",
                            "Invalid credentials.",
                        )
                    except Exception:
                        message = "Login failed."

                    st.error(message)

            except Exception:
                st.error(
                    "Unable to connect to the server. Please try again."
                )

    # =====================================
    # Footer
    # =====================================

    st.divider()

    st.caption(
        "MegNova AI • AI Hospital Digital Twin • Version 1.0"
    )