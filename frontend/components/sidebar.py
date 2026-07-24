import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():

    with st.sidebar:

        # =====================================
        # Logo
        # =====================================
        st.markdown(
            """
            <h2 style='text-align:center;color:#00B4D8;'>
                🏥 MegNova AI
            </h2>
            <p style='text-align:center;color:gray;'>
                Smart Hospital Management Platform
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # =====================================
        # User Information
        # =====================================
        st.markdown("### 👨‍⚕️ Welcome")
        st.write("**Dr. Prasad**")
        st.success("🟢 Online")

        st.divider()

        # =====================================
        # Navigation Menu
        # =====================================

        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Patients",
                "Doctors",
                "Reports",
                "Upload Reports",
                "AI Assistant",
                "Clinical Guidelines",
                "Drug Interaction",
                "Patient Timeline",
                "Medical Search",
                "Analytics",
                "Settings",
                "Profile",
            ],
            icons=[
                "speedometer2",
                "people",
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
            ],
            menu_icon="hospital",
            default_index=0,
            styles={
                "container": {
                    "padding": "5!important",
                    "background-color": "#0E1117",
                },
                "icon": {
                    "color": "#00B4D8",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "4px",
                    "--hover-color": "#262730",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#0096C7",
                    "border-radius": "8px",
                    "color": "white",
                },
            },
        )

        st.divider()

        # =====================================
        # Logout Button
        # =====================================

        if st.button("🚪 Logout", use_container_width=True):
    
           st.session_state.clear()

           st.rerun()

    return selected