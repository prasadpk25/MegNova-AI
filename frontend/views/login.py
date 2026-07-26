import streamlit as st

from utils.api import login


def login_page():
    """User Login Page"""

    # =====================================================
    # Header
    # =====================================================

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

    # =====================================================
    # Login Form
    # =====================================================

    with st.form(
        "login_form",
        clear_on_submit=False,
    ):

        email = st.text_input(
            "📧 Email",
            placeholder="doctor@hospital.com",
            key="login_email",
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        remember = st.checkbox(
            "Remember Me",
            key="remember_me_checkbox",
        )

        submitted = st.form_submit_button(
            "🔐 Login",
            use_container_width=True,
        )

    # =====================================================
    # Login
    # =====================================================

    if submitted:

        email = email.strip()
        password = password.strip()

        if not email:

            st.warning("Please enter your email address.")
            return

        if not password:

            st.warning("Please enter your password.")
            return

        with st.spinner("Authenticating..."):

            try:

                response = login(
                    email,
                    password,
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.logged_in = True

                    st.session_state.access_token = data.get(
                        "access_token",
                        "",
                    )

                    st.session_state.user_name = data.get(
                        "full_name",
                        "Doctor",
                    )

                    st.session_state.user_role = data.get(
                        "role",
                        "Doctor",
                    )

                    st.session_state.remember_me = remember

                    st.success(
                        "✅ Login successful."
                    )

                    st.rerun()

                else:

                    try:

                        message = response.json().get(
                            "detail",
                            "Invalid email or password.",
                        )

                    except Exception:

                        message = (
                            "Invalid email or password."
                        )

                    st.error(message)

            except Exception:

                st.error(
                    "Unable to connect to the server. Please try again later."
                )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "🏥 MegNova AI • AI Hospital Digital Twin • Version 1.0"
    )