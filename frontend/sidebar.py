import streamlit as st
from streamlit_option_menu import option_menu


def sidebar():
    """MegNova AI primary navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:18px 8px 14px;text-align:left;">
              <div style="display:flex;align-items:center;gap:11px;">
                <div style="width:42px;height:42px;border-radius:13px;
                  display:grid;place-items:center;background:linear-gradient(145deg,#12a594,#08796f);
                  color:white;font-size:22px;font-weight:800;">✚</div>
                <div>
                  <div style="font-family:Manrope,sans-serif;font-size:18px;
                    font-weight:800;color:#fff;letter-spacing:-.4px;">MegNova AI</div>
                  <div style="font-size:10px;color:#9bb1c0;letter-spacing:1.1px;
                    text-transform:uppercase;">Hospital Digital Twin</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="height:1px;background:#294258;margin:4px 0 18px;"></div>
            <div style="font-size:10px;font-weight:800;letter-spacing:1.4px;
              color:#7792a5;padding:0 9px 9px;text-transform:uppercase;">Workspace</div>
            """,
            unsafe_allow_html=True,
        )

        user_name = st.session_state.get("user_name", "Care Team")
        user_role = st.session_state.get("user_role", "Healthcare professional")
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;padding:11px;
              background:#17364b;border:1px solid #2a4b61;border-radius:12px;margin-bottom:17px;">
              <div style="width:34px;height:34px;border-radius:50%;background:#d8f4ed;
                color:#08796f;display:grid;place-items:center;font-weight:800;">{str(user_name)[:1].upper()}</div>
              <div style="min-width:0;">
                <div style="font-size:12px;font-weight:700;color:#f3f8fb;white-space:nowrap;
                  overflow:hidden;text-overflow:ellipsis;">{user_name}</div>
                <div style="font-size:10px;color:#9bb1c0;">{user_role}</div>
              </div>
              <div style="margin-left:auto;color:#48c4a7;font-size:9px;">●</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                "grid-1x2-fill",
                "people-fill",
                "person-vcard",
                "person-badge-fill",
                "file-earmark-medical-fill",
                "cloud-arrow-up-fill",
                "graph-up-arrow",
                "journal-medical",
                "robot",
                "person-circle",
                "sliders",
            ],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#9bb1c0", "font-size": "15px"},
                "nav-link": {
                    "font-size": "12px",
                    "text-align": "left",
                    "margin": "3px 0",
                    "padding": "10px 12px",
                    "border-radius": "10px",
                    "color": "#c3d2dc",
                    "--hover-color": "#1b3b52",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(100deg,#0e9384,#08796f)",
                    "color": "#ffffff",
                    "font-weight": "700",
                },
            },
        )

        st.markdown(
            """
            <div style="height:1px;background:#294258;margin:16px 0 13px;"></div>
            <div style="font-size:10px;font-weight:800;letter-spacing:1.2px;
              color:#7792a5;padding:0 9px 10px;text-transform:uppercase;">Connected services</div>
            <div style="display:flex;justify-content:space-between;padding:5px 9px;font-size:11px;color:#b6c8d3;">
              <span>API service</span><span style="color:#48c4a7;">●</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:5px 9px;font-size:11px;color:#b6c8d3;">
              <span>Clinical workspace</span><span style="color:#48c4a7;">●</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("↪  Sign out", key="logout_button", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        return selected
