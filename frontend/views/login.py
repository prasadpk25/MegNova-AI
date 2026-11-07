
import streamlit as st

from utils.api import login


def login_page():
    """MegNova AI Login Page"""

    st.set_page_config(
        page_title="MegNova AI | Login",
        page_icon="ðŸ¥",
        layout="centered",
    )

    st.markdown(
        """
        <style>
        .block-container {
            max-width: 520px;
            padding-top: 5rem;
        }
        .login-subtitle {
            color: #64748b;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align:center;'>ðŸ¥ MegNova AI</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='login-subtitle'>AI-Powered Hospital Digital Twin</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Welcome back")
    st.caption("Sign in to access your hospital workspace.")

    with st.form("megnova_login_form"):
        email = st.text_input(
            "Email address",
            placeholder="Enter your registered email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        submitted = st.form_submit_button(
            "Sign in",
            width="stretch",
            type="primary",
        )

    if submitted:
        if not email.strip() or not password:
            st.warning("Please enter your email and password.")
            return

        try:
            response = login(email.strip(), password)

            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")

                if not token:
                    st.error("Login response did not contain an access token.")
                    return

                st.session_state["access_token"] = token
                st.session_state["logged_in"] = True

                st.session_state["user"] = {
                    "email": email.strip()
                }

                st.session_state["user_name"] = email.split("@")[0]

                st.success("Login successful!")
                st.rerun()

            elif response.status_code in (400, 401, 403):
                st.error("Invalid email or password.")

            else:
                st.error(f"Login failed: HTTP {response.status_code}")

        except Exception as error:
            st.error(f"Unable to connect to the backend: {error}")

    st.divider()

    st.caption(
        "MegNova AI Â© 2026 | Clinical Decision Support Platform"
    )

