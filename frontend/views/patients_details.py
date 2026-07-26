import streamlit as st
import pandas as pd

from datetime import date

from utils.api_client import get, post, delete


def patient_detail_page():

    st.title("👤 Patient Details")
    st.caption(
        "View complete patient information and medical history."
    )

    # =====================================================
    # Refresh
    # =====================================================

    if st.button(
        "🔄 Refresh",
        key="patient_refresh",
        use_container_width=True,
    ):
        st.rerun()

    st.divider()

    # =====================================================
    # Load Patients
    # =====================================================

    with st.spinner("Loading patients..."):

        response = get("/patients/")

    if response.status_code != 200:

        try:
            message = response.json().get(
                "detail",
                "Unable to load patients.",
            )
        except Exception:
            message = "Unable to load patients."

        st.error(message)
        return

    patients = response.json()

    if not patients:

        st.info("No patients found.")
        return

    patient_map = {
        f"{patient['patient_id']} - {patient['full_name']}": patient["id"]
        for patient in patients
    }

    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_map.keys()),
        key="patient_selector",
    )

    patient_id = patient_map[selected_patient]

    # =====================================================
    # Load Selected Patient
    # =====================================================

    with st.spinner("Fetching patient details..."):

        response = get(f"/patients/{patient_id}")

    if response.status_code != 200:

        try:
            message = response.json().get(
                "detail",
                "Unable to fetch patient details.",
            )
        except Exception:
            message = "Unable to fetch patient details."

        st.error(message)
        return

    patient = response.json()

    # =====================================================
    # Safe Fields
    # =====================================================

    full_name = patient.get("full_name", "Unknown")
    patient_code = patient.get("patient_id", "N/A")
    gender = patient.get("gender", "N/A")
    blood_group = patient.get("blood_group", "N/A")

    phone = patient.get("phone", "")
    email = patient.get("email", "")
    address = patient.get("address", "")
    emergency_contact = patient.get(
        "emergency_contact",
        "",
    )

    medical_history = (
        patient.get("medical_history")
        or "No medical history available."
    )

    allergies = (
        patient.get("allergies")
        or "No allergies reported."
    )

    created_at = patient.get("created_at", "")
    is_active = patient.get("is_active", False)
    dob = patient.get("date_of_birth")

    age = "N/A"

    if dob:

        try:

            birth_date = date.fromisoformat(dob)

            today = date.today()

            age = (
                today.year
                - birth_date.year
                - (
                    (today.month, today.day)
                    < (
                        birth_date.month,
                        birth_date.day,
                    )
                )
            )

        except Exception:

            age = "N/A"

    # =====================================================
    # Header
    # =====================================================

    col1, col2 = st.columns([1, 5])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/387/387561.png",
            width=100,
        )

    with col2:

        st.subheader(full_name)

        st.write(f"**Patient ID:** {patient_code}")

        if is_active:

            st.success("🟢 Active")

        else:

            st.error("🔴 Inactive")

    st.divider()

    # =====================================================
    # Basic Information
    # =====================================================

    st.subheader("📋 Basic Information")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Gender",
        gender,
    )

    c2.metric(
        "Blood Group",
        blood_group,
    )

    c3.metric(
        "Age",
        age,
    )

    st.divider()

    # =====================================================
    # Contact Information
    # =====================================================

    st.subheader("📞 Contact Information")

    c1, c2 = st.columns(2)

    with c1:

        st.text_input(
            "Phone",
            value=phone,
            disabled=True,
            key="patient_phone",
        )

        st.text_input(
            "Emergency Contact",
            value=emergency_contact,
            disabled=True,
            key="patient_emergency_contact",
        )

    with c2:

        st.text_input(
            "Email",
            value=email,
            disabled=True,
            key="patient_email",
        )

        st.text_area(
            "Address",
            value=address,
            disabled=True,
            height=90,
            key="patient_address",
        )

    st.divider()

    # =====================================================
    # Medical Information
    # =====================================================

    st.subheader("🩺 Medical Information")

    st.text_area(
        "Medical History",
        value=medical_history,
        disabled=True,
        height=120,
        key="patient_medical_history",
    )

    st.text_area(
        "Allergies",
        value=allergies,
        disabled=True,
        height=100,
        key="patient_allergies",
    )

    st.divider()

    # =====================================================
    # Statistics
    # =====================================================

    c1, c2 = st.columns(2)

    c1.metric(
        "Created",
        created_at[:10] if created_at else "N/A",
    )

    c2.metric(
        "Status",
        "Active" if is_active else "Inactive",
    )

    st.divider()

    # =====================================================
    # Tabs
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Reports",
            "🕒 Timeline",
            "🤖 AI Assistant",
        ]
    )
    # =====================================================
    # REPORTS TAB
    # =====================================================

    with tab1:

        st.subheader("📄 Patient Reports")

        with st.spinner("Loading reports..."):

            response = get("/reports/")

        if response.status_code != 200:

            try:
                message = response.json().get(
                    "detail",
                    "Unable to load reports.",
                )
            except Exception:
                message = "Unable to load reports."

            st.error(message)

        else:

            reports = [
                report
                for report in response.json()
                if report.get("patient_id") == patient_id
            ]

            if not reports:

                st.info(
                    "No reports available for this patient."
                )

            else:

                report_df = pd.DataFrame(reports)

                search = st.text_input(
                    "🔍 Search Report",
                    placeholder="Search by report name...",
                    key="patient_report_search",
                )

                if (
                    search
                    and "report_name" in report_df.columns
                ):

                    report_df = report_df[
                        report_df["report_name"]
                        .fillna("")
                        .str.contains(
                            search,
                            case=False,
                            na=False,
                        )
                    ]

                columns = [
                    col
                    for col in [
                        "report_id",
                        "report_name",
                        "report_type",
                        "created_at",
                    ]
                    if col in report_df.columns
                ]

                st.dataframe(
                    report_df[columns],
                    use_container_width=True,
                    hide_index=True,
                )

                st.divider()

                report_map = {
                    f"{r.get('report_name','Unknown')} ({r.get('report_type','Unknown')})": r
                    for r in reports
                }

                selected_report = st.selectbox(
                    "Select Report",
                    list(report_map.keys()),
                    key="patient_report_selector",
                )

                report = report_map[selected_report]

                left, right = st.columns(2)

                # ==========================================
                # AI Summary
                # ==========================================

                with left:

                    if st.button(
                        "🤖 Generate AI Summary",
                        key="generate_ai_summary",
                        type="primary",
                        use_container_width=True,
                    ):

                        with st.spinner(
                            "Generating AI Summary..."
                        ):

                            summary_response = post(
                                f"/reports/summarize/{report['id']}"
                            )

                        if summary_response.status_code == 200:

                            summary = summary_response.json().get(
                                "summary",
                                "No summary generated.",
                            )

                            st.success(
                                "AI Summary Generated"
                            )

                            st.text_area(
                                "Medical Summary",
                                value=summary,
                                height=220,
                                disabled=True,
                                key="patient_ai_summary",
                            )

                        else:

                            try:
                                message = summary_response.json().get(
                                    "detail",
                                    "Unable to generate summary.",
                                )
                            except Exception:
                                message = (
                                    "Unable to generate summary."
                                )

                            st.error(message)

                # ==========================================
                # Download Metadata
                # ==========================================

                with right:

                    metadata = (
                        pd.DataFrame([report])
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        "📥 Download Metadata",
                        data=metadata,
                        file_name=f"{report.get('report_name','report')}.csv",
                        mime="text/csv",
                        key="download_report_metadata",
                        use_container_width=True,
                    )

                st.divider()

                # ==========================================
                # Report Details
                # ==========================================

                st.subheader("📋 Report Details")

                c1, c2 = st.columns(2)

                with c1:

                    st.text_input(
                        "Report Name",
                        value=report.get(
                            "report_name",
                            "",
                        ),
                        disabled=True,
                        key="report_name",
                    )

                    st.text_input(
                        "Report Type",
                        value=report.get(
                            "report_type",
                            "",
                        ),
                        disabled=True,
                        key="report_type",
                    )

                    st.text_input(
                        "File Name",
                        value=report.get(
                            "file_name",
                            "N/A",
                        ),
                        disabled=True,
                        key="report_file_name",
                    )

                with c2:

                    created = report.get(
                        "created_at",
                        "",
                    )

                    st.text_input(
                        "Report ID",
                        value=report.get(
                            "report_id",
                            "",
                        ),
                        disabled=True,
                        key="report_id",
                    )

                    st.text_input(
                        "Uploaded",
                        value=(
                            created[:19]
                            if created
                            else "N/A"
                        ),
                        disabled=True,
                        key="report_uploaded",
                    )

                    st.text_input(
                        "Patient ID",
                        value=str(
                            report.get(
                                "patient_id",
                                "",
                            )
                        ),
                        disabled=True,
                        key="report_patient_id",
                    )

                if report.get("summary"):

                    st.divider()

                    st.subheader(
                        "🧠 Existing AI Summary"
                    )

                    st.text_area(
                        "Summary",
                        value=report.get(
                            "summary",
                            "",
                        ),
                        height=220,
                        disabled=True,
                        key="existing_summary",
                    )
    # =====================================================
    # TIMELINE TAB
    # =====================================================

    with tab2:

        st.subheader("🕒 Medical Timeline")

        with st.spinner("Loading timeline..."):

            response = get(
                f"/patients/{patient_id}/timeline"
            )

        if response.status_code != 200:

            try:
                message = response.json().get(
                    "detail",
                    "Timeline endpoint unavailable.",
                )
            except Exception:
                message = "Timeline endpoint unavailable."

            st.warning(message)

        else:

            timeline = response.json()

            if not timeline:

                st.info(
                    "No medical timeline available."
                )

            else:

                for index, event in enumerate(
                    timeline,
                    start=1,
                ):

                    with st.container():

                        st.markdown(
                            f"""
### 📄 {event.get("report_name","Unknown Report")}

**Type:** {event.get("report_type","N/A")}

**Created:** {(event.get("created_at",""))[:19] if event.get("created_at") else "N/A"}

**File:** {event.get("file_name","N/A")}
"""
                        )

                        if event.get("summary"):

                            with st.expander(
                                f"🤖 AI Summary #{index}"
                            ):

                                st.write(
                                    event.get(
                                        "summary",
                                        "No summary available.",
                                    )
                                )

                        st.divider()

    # =====================================================
    # AI ASSISTANT TAB
    # =====================================================

    with tab3:

        st.subheader(
            "🤖 AI Patient History Assistant"
        )

        st.info(
            "Ask questions about this patient's medical history."
        )

        question = st.text_area(
            "Your Question",
            placeholder="Example: Summarize this patient's medical history.",
            height=120,
            key="patient_question",
        )

        if st.button(
            "🧠 Ask AI",
            key="ask_patient_ai",
            type="primary",
            use_container_width=True,
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Analyzing patient history..."
                ):

                    response = post(
                        f"/patient-history/{patient_id}",
                        json={
                            "question": question
                        },
                    )

                if response.status_code == 200:

                    answer = response.json().get(
                        "answer",
                        "No response generated.",
                    )

                    st.success(
                        "Analysis Complete"
                    )

                    st.markdown(answer)

                else:

                    try:
                        message = response.json().get(
                            "detail",
                            "Unable to process request.",
                        )
                    except Exception:
                        message = (
                            "Unable to process request."
                        )

                    st.error(message)

        st.divider()

        st.subheader(
            "💡 Suggested Questions"
        )

        suggestions = [
            "Summarize the patient's medical history.",
            "List all major diagnoses.",
            "What allergies does the patient have?",
            "Summarize uploaded reports.",
            "What medications are mentioned?",
            "Are there any recurring medical conditions?",
            "What follow-up is recommended?",
            "Show abnormal findings across reports.",
        ]

        for suggestion in suggestions:

            st.markdown(f"• {suggestion}")
    # =====================================================
    # ACTIONS
    # =====================================================

    st.divider()

    st.subheader("⚙️ Patient Actions")

    col1, col2 = st.columns(2)

    # ==========================================
    # Delete Patient
    # ==========================================

    with col1:

        confirm_delete = st.checkbox(
            "Confirm patient deletion",
            key="confirm_delete_patient",
        )

        if st.button(
            "🗑 Delete Patient",
            key="delete_patient_button",
            use_container_width=True,
        ):

            if not confirm_delete:

                st.warning(
                    "Please confirm deletion before continuing."
                )

            else:

                with st.spinner(
                    "Deleting patient..."
                ):

                    response = delete(
                        f"/patients/{patient_id}"
                    )

                if response.status_code == 200:

                    st.success(
                        "✅ Patient deleted successfully."
                    )

                    st.rerun()

                else:

                    try:
                        message = response.json().get(
                            "detail",
                            "Unable to delete patient.",
                        )
                    except Exception:
                        message = (
                            "Unable to delete patient."
                        )

                    st.error(message)

    # ==========================================
    # Refresh Data
    # ==========================================

    with col2:

        if st.button(
            "🔄 Refresh Data",
            key="refresh_patient_data",
            use_container_width=True,
        ):

            st.rerun()

    # =====================================================
    # QUICK SUMMARY
    # =====================================================

    st.divider()

    st.subheader("📋 Quick Summary")

    summary = f"""
Patient Name : {full_name}
Patient ID : {patient_code}
Gender : {gender}
Blood Group : {blood_group}
Age : {age}
Phone : {phone}
Email : {email}
Emergency Contact : {emergency_contact}
Status : {"Active" if is_active else "Inactive"}
Created : {created_at[:10] if created_at else "N/A"}
"""

    st.text_area(
        "Patient Overview",
        value=summary.strip(),
        height=230,
        disabled=True,
        key="patient_summary",
    )

    # =====================================================
    # EXPORT
    # =====================================================

    st.download_button(
        "📥 Export Patient Details",
        data=summary,
        file_name=f"{patient_code}.txt",
        mime="text/plain",
        key="export_patient_details",
        use_container_width=True,
    )

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.caption(
        "🏥 MegNova AI • Patient Details Module • Version 1.0"
    )