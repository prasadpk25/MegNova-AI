import streamlit as st
from datetime import date

from utils.api_client import get, post, delete


def patient_detail_page():

    st.title("👤 Patient Details")
    st.caption("View complete patient information and medical history.")

    # -----------------------------------
    # Refresh
    # -----------------------------------

    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

    st.divider()

    # -----------------------------------
    # Load Patients
    # -----------------------------------

    with st.spinner("Loading patients..."):
        response = get("/patients/")

    if response.status_code != 200:
        st.error("Unable to load patients.")
        st.code(response.text)
        return

    patients = response.json()

    if not patients:
        st.info("No patients found.")
        return

    patient_map = {
        f"{p['patient_id']} - {p['full_name']}": p["id"]
        for p in patients
    }

    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_map.keys()),
    )

    patient_id = patient_map[selected_patient]

    # -----------------------------------
    # Load Selected Patient
    # -----------------------------------

    with st.spinner("Fetching patient details..."):
        response = get(f"/patients/{patient_id}")

    if response.status_code != 200:
        st.error("Unable to fetch patient details.")
        st.code(response.text)
        return

    patient = response.json()

    # -----------------------------------
    # Header
    # -----------------------------------

    col1, col2 = st.columns([1, 5])

    with col1:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/387/387561.png",
            width=100,
        )

    with col2:
        st.subheader(patient["full_name"])
        st.write(f"**Patient ID:** {patient['patient_id']}")

        if patient["is_active"]:
            st.success("🟢 Active")
        else:
            st.error("🔴 Inactive")

    st.divider()

    # -----------------------------------
    # Basic Information
    # -----------------------------------

    st.subheader("Basic Information")

    age = (
        date.today().year
        - date.fromisoformat(
            patient["date_of_birth"]
        ).year
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Gender", patient["gender"])
    c2.metric("Blood Group", patient["blood_group"])
    c3.metric("Age", age)

    st.divider()

    # -----------------------------------
    # Contact Information
    # -----------------------------------

    st.subheader("Contact Information")

    c1, c2 = st.columns(2)

    with c1:

        st.text_input(
            "Phone",
            value=patient["phone"],
            disabled=True,
        )

        st.text_input(
            "Emergency Contact",
            value=patient["emergency_contact"],
            disabled=True,
        )

    with c2:

        st.text_input(
            "Email",
            value=patient["email"],
            disabled=True,
        )

        st.text_area(
            "Address",
            value=patient["address"],
            disabled=True,
            height=90,
        )

    st.divider()

    # -----------------------------------
    # Medical Information
    # -----------------------------------

    st.subheader("Medical Information")

    st.text_area(
        "Medical History",
        value=patient.get(
            "medical_history",
            ""
        ) or "No medical history available.",
        disabled=True,
        height=120,
    )

    st.text_area(
        "Allergies",
        value=patient.get(
            "allergies",
            ""
        ) or "No allergies reported.",
        disabled=True,
        height=100,
    )

    st.divider()

    # -----------------------------------
    # Statistics
    # -----------------------------------

    c1, c2 = st.columns(2)

    c1.metric(
        "Created",
        patient["created_at"][:10],
    )

    c2.metric(
        "Status",
        "Active" if patient["is_active"] else "Inactive",
    )

    st.divider()

    # -----------------------------------
    # Tabs
    # -----------------------------------

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

        st.subheader("Patient Reports")

        with st.spinner("Loading reports..."):
            response = get("/reports/")

        if response.status_code != 200:

            st.error("Unable to load reports.")

        else:

            reports = [
                r for r in response.json()
                if r["patient_id"] == patient_id
            ]

            if not reports:

                st.info("No reports available for this patient.")

            else:

                import pandas as pd

                report_df = pd.DataFrame(reports)

                search = st.text_input(
                    "🔍 Search Report",
                    placeholder="Search by report name...",
                )

                if search:

                    report_df = report_df[
                        report_df["report_name"].str.contains(
                            search,
                            case=False,
                            na=False,
                        )
                    ]

                st.dataframe(
                    report_df[
                        [
                            "report_id",
                            "report_name",
                            "report_type",
                            "created_at",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

                st.divider()

                report_map = {
                    f"{r['report_name']} ({r['report_type']})": r
                    for r in reports
                }

                selected = st.selectbox(
                    "Select Report",
                    list(report_map.keys()),
                )

                report = report_map[selected]

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "🤖 Generate AI Summary",
                        use_container_width=True,
                    ):

                        with st.spinner("Generating summary..."):

                            summary = post(
                                f"/reports/summarize/{report['id']}"
                            )

                        if summary.status_code == 200:

                            st.success("Summary Generated")

                            st.info(
                                summary.json().get(
                                    "summary",
                                    "No summary returned.",
                                )
                            )

                        else:

                            st.error(summary.text)

                with col2:

                    csv = pd.DataFrame(
                        [report]
                    ).to_csv(index=False)

                    st.download_button(
                        "📥 Download Metadata",
                        csv,
                        file_name=f"{report['report_name']}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

                st.divider()

                st.subheader("Report Details")

                c1, c2 = st.columns(2)

                with c1:

                    st.text_input(
                        "Report Name",
                        report["report_name"],
                        disabled=True,
                    )

                    st.text_input(
                        "Report Type",
                        report["report_type"],
                        disabled=True,
                    )

                with c2:

                    st.text_input(
                        "Report ID",
                        report["report_id"],
                        disabled=True,
                    )

                    st.text_input(
                        "Uploaded",
                        report["created_at"][:19],
                        disabled=True,
                    )

    # =====================================================
    # TIMELINE TAB
    # =====================================================

    with tab2:

        st.subheader("Medical Timeline")

        response = get(
            f"/patients/{patient_id}/timeline"
        )

        if response.status_code != 200:

            st.warning("Timeline endpoint unavailable.")

        else:

            timeline = response.json()

            if not timeline:

                st.info("No medical timeline available.")

            else:

                for event in timeline:

                    with st.container():

                        st.markdown(
                            f"""
### 📄 {event['report_name']}

**Type:** {event['report_type']}

**Created:** {event['created_at'][:19]}

**File:** {event['file_name']}
"""
                        )

                        if event.get("summary"):

                            with st.expander(
                                "AI Summary"
                            ):

                                st.write(
                                    event["summary"]
                                )

                        st.divider()  
    # =====================================================
    # AI ASSISTANT TAB
    # =====================================================

    with tab3:

        st.subheader("🤖 AI Patient History Assistant")

        st.info(
            "Ask questions about this patient's medical history."
        )

        question = st.text_area(
            "Your Question",
            placeholder="Example: Summarize this patient's medical history.",
            height=120,
        )

        if st.button(
            "🧠 Ask AI",
            use_container_width=True,
            type="primary",
        ):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                with st.spinner("Analyzing patient history..."):

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

                    st.success("Analysis Complete")

                    st.markdown(answer)

                else:

                    st.error(response.text)

        st.divider()

        st.subheader("Suggested Questions")

        suggestions = [
            "Summarize the patient's medical history.",
            "List all major diagnoses.",
            "What allergies does the patient have?",
            "Summarize uploaded reports.",
            "What medications are mentioned?",
        ]

        for item in suggestions:
            st.markdown(f"- {item}")

    # =====================================================
    # ACTIONS
    # =====================================================

    st.divider()

    st.subheader("Patient Actions")

    col1, col2 = st.columns(2)

    with col1:

        confirm = st.checkbox(
            "Confirm patient deletion"
        )

        if st.button(
            "🗑 Delete Patient",
            use_container_width=True,
        ):

            if not confirm:

                st.warning(
                    "Please confirm deletion first."
                )

            else:

                response = delete(
                    f"/patients/{patient_id}"
                )

                if response.status_code == 200:

                    st.success(
                        "Patient deleted successfully."
                    )

                    st.rerun()

                else:

                    st.error(response.text)

    with col2:

        if st.button(
            "🔄 Refresh Data",
            use_container_width=True,
        ):

            st.rerun()

    # =====================================================
    # QUICK SUMMARY
    # =====================================================

    st.divider()

    st.subheader("Quick Summary")

    summary = f"""
Patient Name : {patient['full_name']}
Patient ID : {patient['patient_id']}
Gender : {patient['gender']}
Blood Group : {patient['blood_group']}
Phone : {patient['phone']}
Email : {patient['email']}
Status : {"Active" if patient["is_active"] else "Inactive"}
"""

    st.text_area(
        "Overview",
        summary,
        height=220,
    )

    # =====================================================
    # EXPORT
    # =====================================================

    st.download_button(
        "📥 Export Patient Details",
        summary,
        file_name=f"{patient['patient_id']}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.caption(
        "MegNova AI • Patient Details Module"
    )                          