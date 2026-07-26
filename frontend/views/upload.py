import streamlit as st

from utils.api_client import get, post


# ==========================================================
# Upload Medical Report
# ==========================================================

REPORT_TYPES = [
    "Blood Test",
    "X-Ray",
    "MRI",
    "CT Scan",
    "ECG",
    "Prescription",
    "Discharge Summary",
    "Other",
]


def upload_page():
    """Upload Medical Report Page"""

    st.title("📤 Upload Medical Report")
    st.caption(
        "Upload patient reports for OCR processing and AI analysis."
    )

    st.divider()

    # =====================================================
    # Load Patients
    # =====================================================

    with st.spinner("Loading patients..."):

        patient_response = get("/patients/")

    if patient_response.status_code != 200:

        st.error("Unable to load patient records.")

        return

    patients = patient_response.json()

    if not patients:

        st.warning("No patients available.")

        return

    # =====================================================
    # Load Doctors
    # =====================================================

    with st.spinner("Loading doctors..."):

        doctor_response = get("/doctors/")

    if doctor_response.status_code != 200:

        st.error("Unable to load doctors.")

        return

    doctors = doctor_response.json()

    if not doctors:

        st.warning("No doctors available.")

        return

    # =====================================================
    # Dropdown Data
    # =====================================================

    patient_map = {
        f"{p['patient_id']} - {p['full_name']}": p["id"]
        for p in patients
    }

    doctor_map = {
        f"{d['doctor_id']} - {d['full_name']}": d["id"]
        for d in doctors
    }

    # =====================================================
    # Upload Form
    # =====================================================

    with st.form(
        "upload_form",
        clear_on_submit=True,
    ):

        st.subheader("📋 Report Information")

        col1, col2 = st.columns(2)

        with col1:

            patient = st.selectbox(
                "👤 Patient",
                list(patient_map.keys()),
                key="upload_patient",
            )

            report_name = st.text_input(
                "📄 Report Name",
                placeholder="Example: Blood Test - July",
                key="upload_report_name",
            )

        with col2:

            doctor = st.selectbox(
                "👨‍⚕️ Doctor",
                list(doctor_map.keys()),
                key="upload_doctor",
            )

            report_type = st.selectbox(
                "📑 Report Type",
                REPORT_TYPES,
                key="upload_report_type",
            )

        st.divider()

        uploaded_file = st.file_uploader(
            "Choose Medical Report",
            type=[
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "docx",
            ],
            help="Supported formats: PDF, DOCX, PNG, JPG and JPEG",
            key="upload_report_file",
        )

        st.info(
            "Supported formats: PDF, DOCX, PNG, JPG and JPEG"
        )

        submit = st.form_submit_button(
            "📤 Upload Report",
            type="primary",
            use_container_width=True,
        )

    # =====================================================
    # Validation
    # =====================================================

    if not submit:
        return

    if not report_name.strip():

        st.warning("Please enter a report name.")

        return

    if uploaded_file is None:

        st.warning("Please choose a report file.")

        return

    patient_id = patient_map[patient]
    doctor_id = doctor_map[doctor]

    with st.spinner("Uploading report..."):

        payload = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "report_name": report_name.strip(),
            "report_type": report_type,
        }

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        response = post(
            "/reports/upload",
            data=payload,
            files=files,
        )
    # =====================================================
    # Upload Response
    # =====================================================

    if response.status_code not in (200, 201):

        try:
            message = response.json().get(
                "detail",
                "Unable to upload report."
            )
        except Exception:
            message = "Unable to upload report."

        st.error(message)
        return

    result = response.json()

    report = result.get("report")

    if not report:

        st.error("Upload completed, but report details were not returned.")
        return

    st.success("🎉 Medical Report Uploaded Successfully")

    st.balloons()

    st.divider()

    # =====================================================
    # Uploaded Report Details
    # =====================================================

    st.subheader("📄 Uploaded Report")

    left, right = st.columns(2)

    with left:

        st.text_input(
            "Report ID",
            value=report.get("report_id", ""),
            disabled=True,
            key="report_id_display",
        )

        st.text_input(
            "Report Name",
            value=report.get("report_name", ""),
            disabled=True,
            key="report_name_display",
        )

        st.text_input(
            "Report Type",
            value=report.get("report_type", ""),
            disabled=True,
            key="report_type_display",
        )

    with right:

        st.text_input(
            "Patient ID",
            value=str(report.get("patient_id", "")),
            disabled=True,
            key="patient_id_display",
        )

        st.text_input(
            "Doctor ID",
            value=str(report.get("doctor_id", "")),
            disabled=True,
            key="doctor_id_display",
        )

        created_at = report.get("created_at", "")

        st.text_input(
            "Uploaded At",
            value=created_at[:19] if created_at else "",
            disabled=True,
            key="uploaded_at_display",
        )

    st.divider()

    # =====================================================
    # AI Summary
    # =====================================================

    st.subheader("🤖 AI Report Summary")

    if st.button(
        "🧠 Generate AI Summary",
        key="generate_summary_upload",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Generating AI Summary..."):

            summary_response = post(
                f"/reports/summarize/{report['id']}"
            )

        if summary_response.status_code == 200:

            summary = summary_response.json().get(
                "summary",
                "No summary generated."
            )

            st.success("✅ AI Summary Generated")

            st.text_area(
                "Medical Summary",
                value=summary,
                height=250,
                disabled=True,
                key="generated_summary",
            )

        else:

            try:
                message = summary_response.json().get(
                    "detail",
                    "Unable to generate AI summary."
                )
            except Exception:
                message = "Unable to generate AI summary."

            st.error(message)

    st.divider()

    st.caption(
        "MegNova AI • Medical Report Upload Module"
    )