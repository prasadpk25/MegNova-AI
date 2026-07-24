import streamlit as st
import pandas as pd

from utils.api_client import get, post
from utils.helpers import handle_response


def reports_page():

    st.title("📄 Medical Reports")
    st.caption("Upload, manage and summarize patient medical reports.")

    # ==========================================
    # Load Patients
    # ==========================================

    patient_response = get("/patients/")
    patients = handle_response(patient_response)

    patient_dict = {}

    if patients:
        patient_dict = {
            p["full_name"]: p["id"]
            for p in patients
        }

    # ==========================================
    # Load Doctors
    # ==========================================

    doctor_response = get("/doctors/")
    doctors = handle_response(doctor_response)

    doctor_dict = {}

    if doctors:
        doctor_dict = {
            d["full_name"]: d["id"]
            for d in doctors
        }

    st.divider()

    st.subheader("📤 Upload Medical Report")

    col1, col2 = st.columns(2)

    with col1:

        selected_patient = st.selectbox(
            "Patient",
            list(patient_dict.keys())
            if patient_dict else []
        )

        report_name = st.text_input(
            "Report Name"
        )

    with col2:

        selected_doctor = st.selectbox(
            "Doctor",
            list(doctor_dict.keys())
            if doctor_dict else []
        )

        report_type = st.selectbox(
            "Report Type",
            [
                "Blood Test",
                "X-Ray",
                "MRI",
                "CT Scan",
                "ECG",
                "Prescription",
                "Discharge Summary",
                "Other"
            ]
        )

    uploaded_file = st.file_uploader(
        "Choose Medical Report",
        type=["pdf", "png", "jpg", "jpeg", "docx"]
    )

    if st.button(
        "📤 Upload Report",
        use_container_width=True
    ):

        if not uploaded_file:
            st.warning("Please select a report file.")

        elif report_name.strip() == "":
            st.warning("Please enter report name.")

        else:

            data = {
                "patient_id": patient_dict[selected_patient],
                "doctor_id": doctor_dict[selected_doctor],
                "report_name": report_name,
                "report_type": report_type,
            }

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            with st.spinner("Uploading report..."):

                response = post(
                    "/reports/upload",
                    data=data,
                    files=files,
                )

            if response.status_code in (200, 201):

                st.success("✅ Report uploaded successfully.")

                st.rerun()

            else:

                st.error(response.text)

    st.divider()

    # ==========================================
    # Fetch Reports
    # ==========================================

    response = get("/reports/")

    reports = handle_response(response)

    if not reports:

        st.warning("No reports available.")

        return

    # ==========================================
    # Dashboard Metrics
    # ==========================================

    total_reports = len(reports)

    summarized = len(
        [
            r
            for r in reports
            if r.get("summary")
        ]
    )

    pending = total_reports - summarized

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Reports",
        total_reports
    )

    c2.metric(
        "AI Summaries",
        summarized
    )

    c3.metric(
        "Pending",
        pending
    )

    st.divider()

    # ==========================================
    # Prepare DataFrame
    # ==========================================

    rows = []

    for r in reports:

        rows.append(
            {
                "ID": r["report_id"],
                "Patient": r["patient"]["full_name"],
                "Doctor": r["doctor"]["full_name"],
                "Report": r["report_name"],
                "Type": r["report_type"],
                "File": r["file_name"],
                "Created": r["created_at"][:10],
                "Summary": "Yes" if r.get("summary") else "No",
                "ReportID": r["id"],
                "SummaryText": r.get("summary") or "",
            }
        )

    df = pd.DataFrame(rows)

    search = st.text_input(
        "🔍 Search Reports"
    )

    if search:

        df = df[
            df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False
                )
            )
            .any(axis=1)
        ]

    st.subheader("📋 Uploaded Reports")

    st.dataframe(
        df[
            [
                "ID",
                "Patient",
                "Doctor",
                "Report",
                "Type",
                "File",
                "Created",
                "Summary",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )

    st.divider()
        # ==========================================
    # AI Summary
    # ==========================================

    st.subheader("🤖 AI Medical Summary")

    selected_report = st.selectbox(
        "Select Report",
        df["ID"].tolist()
    )

    selected_row = df[df["ID"] == selected_report].iloc[0]

    report_db_id = int(selected_row["ReportID"])

    if st.button(
        "🧠 Generate AI Summary",
        use_container_width=True
    ):

        with st.spinner("Generating AI Summary..."):

            response = post(
                f"/reports/summarize/{report_db_id}"
            )

        if response.status_code == 200:

            st.success("✅ AI Summary Generated")

            st.rerun()

        else:

            st.error(response.text)

    st.divider()

    # ==========================================
    # View Summary
    # ==========================================

    st.subheader("📑 Report Summary")

    summary = selected_row["SummaryText"]

    if summary:

        st.info(summary)

    else:

        st.warning("No AI summary available for this report.")

    st.divider()

    # ==========================================
    # Report Details
    # ==========================================

    st.subheader("📋 Selected Report")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Patient**")
        st.success(selected_row["Patient"])

        st.write("**Doctor**")
        st.success(selected_row["Doctor"])

        st.write("**Report Name**")
        st.info(selected_row["Report"])

    with col2:
        st.write("**Type**")
        st.info(selected_row["Type"])

        st.write("**File**")
        st.info(selected_row["File"])

        st.write("**Created**")
        st.info(selected_row["Created"])

    st.divider()

    # ==========================================
    # Download CSV
    # ==========================================

    st.download_button(
        "📥 Download Reports CSV",
        df.drop(columns=["ReportID", "SummaryText"]).to_csv(index=False),
        "reports.csv",
        "text/csv",
        use_container_width=True,
    )