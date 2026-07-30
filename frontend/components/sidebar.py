import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():
    """Reusable application sidebar."""

    try:
        with st.sidebar:

            # ==================================================
            # LOGO
            # ==================================================

            st.markdown(
                """
                <div style="text-align:center;padding:10px;">
                    <h1>🏥</h1>
                    <h2>MegNova AI</h2>
                    <p>AI Hospital Digital Twin</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.divider()

            # ==================================================
            # USER
            # ==================================================

            user_name = st.session_state.get(
                "user_name",
                "Doctor",
            )

            user_role = st.session_state.get(
                "user_role",
                "Doctor",
            )

            st.success(f"🟢 {user_name}")
            st.caption(user_role)

            st.divider()

            # ==================================================
            # MENU
            # ==================================================

            selected = option_menu(
                menu_title=None,
                options=[
                    "Dashboard",
                    "Patients",
                    "Patient Details",
                    "Doctors",
                    "Reports",
                    "Upload Reports",
                    "Analytics",
                    "Clinical Guidelines",
                    "AI Assistant",
                    "Profile",
                    "Settings",
                ],
                icons=[
                    "house",
                    "people",
                    "person-lines-fill",
                    "person-badge",
                    "file-earmark-medical",
                    "cloud-upload",
                    "bar-chart",
                    "journal-medical",
                    "robot",
                    "person-circle",
                    "gear",
                ],
                default_index=0,
            )

            st.divider()

            st.markdown("### 🖥️ Services")

            st.success("✅ FastAPI")
            st.success("✅ PostgreSQL")
            st.success("✅ AI Online")

            st.divider()

            if st.button(
                "🚪 Logout",
                use_container_width=True,
                key="logout_button",
            ):
                st.session_state.clear()
                st.rerun()

            return selected

    except Exception as e:
        st.error(f"Sidebar error: {e}")
        return "Dashboard"