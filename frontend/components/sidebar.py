import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():
    """Reusable application sidebar."""

    with st.sidebar:

        # ==================================================
        # LOGO
        # ==================================================

        st.markdown(
            """
            <div style="text-align:center;padding:10px;">
                <h1>🏥</h1>
                <h2 style="margin-bottom:0;">MegNova AI</h2>
                <p style="color:gray;">
                    AI Hospital Digital Twin
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ==================================================
        # USER
        # ==================================================

        user_name = st.session_state.get("user_name", "Doctor")
        user_role = st.session_state.get("user_role", "Doctor")

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
            orientation="vertical",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#0F172A",
                },
                "icon": {
                    "color": "#38BDF8",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "2px",
                    "--hover-color": "#1E293B",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#0284C7",
                    "color": "white",
                },
            },
        )

        st.divider()

        # ==================================================
        # SERVICES
        # ==================================================

        st.markdown("### 🖥️ Services")

        st.success("✅ FastAPI")
        st.success("✅ PostgreSQL")
        st.success("✅ AI Online")

        st.divider()

        # ==================================================
        # LOGOUT
        # ==================================================

        if st.button(
    "🚪 Logout",
    use_container_width=True,
):
            st.session_state.clear()
            st.rerun()

        st.caption("🚨 THIS IS THE REAL SIDEBAR FILE 🚨")

    return selected