import streamlit as st


def dashboard_page():
    """Main Dashboard"""

    # =====================================================
    # Header
    # =====================================================

    st.title("ðŸ¥ MegNova AI Dashboard")
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
## Welcome, **{user_name}** ðŸ‘‹

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
        ("ðŸ‘¨â€âš•ï¸ Doctors", doctor_count, "+2"),
        ("ðŸ§‘ Patients", patient_count, "+12"),
        ("ðŸ“„ Reports", report_count, "+25"),
        ("ðŸ¤– AI Queries", ai_queries, "+31"),
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

    st.subheader("âš¡ Quick Actions")

    actions = [
        (
            "âž• Add Patient",
            "Open Patients page from the sidebar.",
            "dashboard_add_patient",
        ),
        (
            "ðŸ“¤ Upload Report",
            "Open Reports page from the sidebar.",
            "dashboard_upload_report",
        ),
        (
            "ðŸ¤– Open AI Assistant",
            "Open AI Assistant from the sidebar.",
            "dashboard_ai_assistant",
        ),
        (
            "ðŸ“Š Analytics",
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
                width="stretch",
            ):

                st.info(message)

    st.divider()

    # =====================================================
    # Recent Activity
    # =====================================================

    st.subheader("ðŸ•’ Recent Activity")

    activities = [
        "Patient MR000145 admitted",
        "Blood Report uploaded successfully",
        "AI generated report summary",
        "New doctor account created",
        "Clinical guideline searched",
    ]

    for activity in activities:

        st.markdown(f"â€¢ {activity}")

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

        st.subheader("ðŸ¤– AI Services")

        for service in ai_services:

            st.success(f"âœ… {service}")

    with right:

        st.subheader("ðŸ–¥ï¸ System Status")

        for service in system_services:

            st.success(f"ðŸŸ¢ {service}")

    st.divider()

    # =====================================================
    # Footer
    # =====================================================

    st.caption(
        "ðŸ¥ MegNova AI â€¢ AI Hospital Digital Twin â€¢ Version 1.0"
    )
