import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():

    with st.sidebar:

        # -----------------------------
        # Logo
        # -----------------------------
        st.markdown(
            """
            <h2 style='text-align:center;'>
            🏥 AI Hospital
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Digital Twin Platform")

        st.divider()

        # -----------------------------
        # User Card
        # -----------------------------
        st.markdown("### 👨‍⚕️ Dr. Prasad")
        st.success("🟢 Online")

        st.divider()

        # -----------------------------
        # Navigation
        # -----------------------------
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Patients",
                "Reports",
                "Upload",
                "AI Assistant",
                "Drug Checker",
                "Medical Search",
                "Analytics",
                "Settings",
                "Profile"
            ],
            icons=[
                "speedometer2",
                "people",
                "file-earmark-medical",
                "cloud-upload",
                "robot",
                "capsule",
                "search",
                "bar-chart",
                "gear",
                "person-circle"
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#0E1117",
                },
                "icon": {
                    "color": "#00B4D8",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "4px",
                    "--hover-color": "#262730",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#0096C7",
                    "border-radius": "8px",
                },
            },
        )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    return selected