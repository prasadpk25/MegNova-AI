import streamlit as st


def dashboard_page():
    """Main MegNova AI overview."""
    user_name = st.session_state.get("user_name", "Care Team")
    st.markdown('<div class="mn-eyebrow">OVERVIEW / HOSPITAL OPERATIONS</div>', unsafe_allow_html=True)
    st.title(f"Good to see you, {user_name}")
    st.caption("Your hospital workspace at a glance. Monitor activity and jump into key workflows.")

    metric_data = [
        ("👨‍⚕️", "Doctors", "18", "+2 this month"),
        ("🧑", "Patients", "256", "+12 this month"),
        ("📄", "Reports", "1,342", "+25 this month"),
        ("✦", "AI queries", "421", "+31 this month"),
    ]
    cols = st.columns(4, gap="medium")
    for col, (icon, label, value, delta) in zip(cols, metric_data):
        with col:
            st.markdown(
                f"""
                <div style="background:#fff;border:1px solid #e6edf2;border-radius:16px;
                  padding:17px 18px;min-height:126px;box-shadow:0 5px 18px rgba(25,48,70,.035);">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:11px;font-weight:700;color:#718096;">{label}</span>
                    <span style="width:30px;height:30px;display:grid;place-items:center;
                      border-radius:9px;background:#e9f7f3;color:#0e9384;">{icon}</span>
                  </div>
                  <div style="font:800 27px Manrope,sans-serif;color:#15263b;margin-top:9px;">{value}</div>
                  <div style="font-size:10px;color:#0e9384;font-weight:700;margin-top:3px;">↗ {delta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown("## Quick actions")
    st.caption("Go directly to a frequently used workflow.")
    actions = [
        ("＋", "Register a patient", "Open Patients to create or review patient records."),
        ("↥", "Upload a report", "Add a medical document for the patient's record."),
        ("✦", "Ask MegNova AI", "Ask questions about uploaded medical reports."),
        ("▥", "View analytics", "Explore hospital-level reporting and trends."),
    ]
    cols = st.columns(4, gap="medium")
    for col, (symbol, title, description) in zip(cols, actions):
        with col:
            with st.container(border=True):
                st.markdown(f"<div style='font-size:22px;color:#0e9384'>{symbol}</div>", unsafe_allow_html=True)
                st.markdown(f"**{title}**")
                st.caption(description)

    st.write("")
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### Recent activity")
            st.caption("Latest workspace events")
            activities = [
                ("Patient record updated", "Patient information was reviewed", "Today"),
                ("Medical report uploaded", "A new report was added to records", "Today"),
                ("AI report summary generated", "Report analysis completed", "Today"),
                ("Doctor profile created", "A new doctor record was added", "Recently"),
            ]
            for title, detail, when in activities:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:12px;padding:11px 0;border-bottom:1px solid #edf1f4;">
                      <div style="width:8px;height:8px;border-radius:50%;background:#0e9384;margin-top:6px;"></div>
                      <div style="flex:1;"><div style="font-size:12px;font-weight:700;color:#20364a;">{title}</div>
                      <div style="font-size:11px;color:#8291a0;">{detail}</div></div>
                      <div style="font-size:10px;color:#9aa7b3;">{when}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    with right:
        with st.container(border=True):
            st.markdown("### Platform services")
            st.caption("Configured application components")
            services = [
                ("FastAPI backend", "Connected"),
                ("PostgreSQL", "Configured"),
                ("Qdrant vector search", "Configured"),
                ("AI assistant", "Available"),
            ]
            for service, status in services:
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:10px 0;"
                    f"border-bottom:1px solid #edf1f4;font-size:12px;'>"
                    f"<span style='color:#526579'>{service}</span>"
                    f"<span style='color:#0e9384;font-weight:700'>● {status}</span></div>",
                    unsafe_allow_html=True,
                )
            st.caption("Service indicators reflect configured modules, not live health probes.")

    st.write("")
    st.info("MegNova AI supports clinical information workflows. It is not a substitute for professional medical judgement.")
