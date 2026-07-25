import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():
    """Application Sidebar"""

    with st.sidebar:

        # =====================================
        # Logo
        # =====================================

        st.markdown(
            """
            <div style="text-align:center">
                <h2 style="color:#00B4D8;margin-bottom:0;">
                    🏥 MegNova AI
                </h2>
                <p style="color:gray;font-size:14px;">
                    AI Hospital Digital Twin
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # =====================================
        # User Details
        # =====================================

        user_name = st.session_state.get(
            "user_name",
            "Doctor",
        )

        user_role = st.session_state.get(
            "user_role",
            "Doctor",
        )

        st.markdown("### 👨‍⚕️ Logged In")

        st.markdown(f"**{user_name}**")

        st.caption(user_role)

        st.success("🟢 Online")

        st.divider()

        # =====================================
        # Navigation
        # =====================================

        options = [
            "Dashboard",
            "Patients",
            "Doctors",
            "Reports",
            "Upload Reports",
            "AI Assistant",
            "Clinical Guidelines",
            "Patient Timeline",
            "Medical Search",
            "Analytics",
            "Settings",
            "Profile",
        ]

        icons = [
            "speedometer2",
            "people",
            "person-badge",
            "file-earmark-medical",
            "cloud-upload",
            "robot",
            "journal-medical",
            "capsule",
            "clock-history",
            "search",
            "bar-chart",
            "gear",
            "person-circle",
        ]

        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            default_index=0,
            styles={
                "container": {
                    "padding": "8px",
                    "background-color": "#0E1117",
                },
                "icon": {
                    "color": "#00B4D8",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "3px",
                    "--hover-color": "#262730",
                    "border-radius": "10px",
                },
                "nav-link-selected": {
                    "background-color": "#0096C7",
                    "color": "white",
                    "border-radius": "10px",
                },
            },
        )

        st.divider()

        # =====================================
        # System Status
        # =====================================

        st.markdown("### 🖥️ Services")

        st.success("FastAPI")
        st.success("PostgreSQL")
        st.success("AI Online")

        st.divider()

        # =====================================
        # Logout
        # =====================================

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            st.session_state.clear()
            st.rerun()

        st.caption("Version 1.0")

    return selected