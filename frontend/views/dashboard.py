import streamlit as st


def dashboard_page():
    """Main Dashboard"""

    # =====================================================
    # Header
    # =====================================================

    st.title("🏥 MegNova AI Dashboard")
    st.caption("AI-Powered Hospital Digital Twin")

    st.divider()

    # =====================================================
    # Welcome
    # =====================================================

    user_name = st.session_state.get(
        "user_name",
        "Doctor",
    )

    st.markdown(
        f"""
## Welcome, **{user_name}** 👋

Monitor hospital operations, manage patients, analyze medical reports,
and interact with the AI Medical Assistant from one unified dashboard.
"""
    )

    st.divider()

    # =====================================================
    # Hospital Statistics
    # =====================================================

    doctor_count = 18
    patient_count = 256
    report_count = 1342
    ai_queries = 421

    metric_data = [
        ("👨‍⚕️ Doctors", doctor_count, "+2"),
        ("🧑 Patients", patient_count, "+12"),
        ("📄 Reports", report_count, "+25"),
        ("🤖 AI Queries", ai_queries, "+31"),
    ]

    cols = st.columns(4)

    for col, metric in zip(cols, metric_data):

        label, value, delta = metric

        with col:

            st.metric(
                label=label,
                value=value,
                delta=delta,
            )

    st.divider()

    # =====================================================
    # Quick Actions
    # =====================================================

    st.subheader("⚡ Quick Actions")

    actions = [
        (
            "➕ Add Patient",
            "Open Patients page from the sidebar.",
            "dashboard_add_patient",
        ),
        (
            "📤 Upload Report",
            "Open Reports page from the sidebar.",
            "dashboard_upload_report",
        ),
        (
            "🤖 Open AI Assistant",
            "Open AI Assistant from the sidebar.",
            "dashboard_ai_assistant",
        ),
        (
            "📊 Analytics",
            "Open Analytics page from the sidebar.",
            "dashboard_analytics",
        ),
    ]

    cols = st.columns(4)

    for col, action in zip(cols, actions):

        title, message, key = action

        with col:

            if st.button(
                title,
                key=key,
                use_container_width=True,
            ):

                st.info(message)

    st.divider()

    # =====================================================
    # Recent Activity
    # =====================================================

    st.subheader("🕒 Recent Activity")

    activities = [
        "Patient MR000145 admitted",
        "Blood Report uploaded successfully",
        "AI generated report summary",
        "New doctor account created",
        "Clinical guideline searched",
    ]

    for activity in activities:

        st.markdown(f"• {activity}")

    st.divider()

    # =====================================================
    # System Status
    # =====================================================

    left, right = st.columns(2)

    ai_services = [
        "OCR Service",
        "Medical Summarizer",
        "Vector Database",
        "AI Chatbot",
    ]

    system_services = [
        "FastAPI Running",
        "PostgreSQL Connected",
        "Qdrant Connected",
        "Streamlit Active",
    ]

    with left:

        st.subheader("🤖 AI Services")

        for service in ai_services:

            st.success(f"✅ {service}")

    with right:

        st.subheader("🖥️ System Status")

        for service in system_services:

            st.success(f"🟢 {service}")

    st.divider()

    # =====================================================
    # Footer
    # =====================================================

    st.caption(
        "🏥 MegNova AI • AI Hospital Digital Twin • Version 1.0"
    )