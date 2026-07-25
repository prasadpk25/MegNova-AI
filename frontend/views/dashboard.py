import streamlit as st

# =====================================
# Dashboard
# =====================================

def dashboard_page():
    """Main dashboard page."""

    # =====================================
    # Header
    # =====================================

    st.title("🏥 MegNova AI Dashboard")
    st.caption("AI-Powered Hospital Digital Twin")

    st.divider()

    # =====================================
    # Welcome
    # =====================================

    user_name = st.session_state.get("user_name", "Doctor")

    st.markdown(f"""
    ## Welcome, **{user_name}** 👋

    Monitor hospital operations, manage patients, analyze reports,
    and interact with the AI Medical Assistant from one unified dashboard.
    """)

    st.divider()

    # =====================================
    # Hospital Statistics
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👨‍⚕️ Doctors",
            value="18",
            delta="+2",
        )

    with col2:
        st.metric(
            label="🧑 Patients",
            value="256",
            delta="+12",
        )

    with col3:
        st.metric(
            label="📄 Reports",
            value="1342",
            delta="+25",
        )

    with col4:
        st.metric(
            label="🤖 AI Queries",
            value="421",
            delta="+31",
        )

    st.divider()

    # =====================================
    # Quick Actions
    # =====================================

    st.subheader("⚡ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button(
            "➕ Add Patient",
            use_container_width=True,
        ):
            st.info("Open Patients page from the sidebar.")

    with c2:
        if st.button(
            "📤 Upload Report",
            use_container_width=True,
        ):
            st.info("Open Reports page from the sidebar.")

    with c3:
        if st.button(
            "🤖 Open AI Assistant",
            use_container_width=True,
        ):
            st.info("Open AI Assistant from the sidebar.")

    with c4:
        if st.button(
            "📊 Analytics",
            use_container_width=True,
        ):
            st.info("Open Analytics page from the sidebar.")

    st.divider()

    # =====================================
    # Recent Activity
    # =====================================

    st.subheader("🕒 Recent Activity")

    st.info(
        """
        • Patient MR000145 admitted

        • Blood Report uploaded successfully

        • AI generated report summary

        • New doctor account created

        • Clinical guideline searched
        """
    )

    st.divider()

    # =====================================
    # AI Status
    # =====================================

    left, right = st.columns(2)

    with left:
        st.subheader("🤖 AI Services")

        st.success("✅ OCR Service")
        st.success("✅ Medical Summarizer")
        st.success("✅ Vector Database")
        st.success("✅ AI Chatbot")

    with right:
        st.subheader("🖥️ System Status")

        st.success("🟢 FastAPI Running")
        st.success("🟢 PostgreSQL Connected")
        st.success("🟢 Qdrant Connected")
        st.success("🟢 Streamlit Active")

    st.divider()

    # =====================================
    # Footer
    # =====================================

    st.caption(
        "MegNova AI • AI Hospital Digital Twin • Version 1.0"
    )