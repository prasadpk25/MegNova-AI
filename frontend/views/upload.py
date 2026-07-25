import streamlit as st

from utils.api_client import get, post


# ============================================================
# UPLOAD REPORT PAGE
# ============================================================

def upload_page():

    st.title("📤 Upload Medical Report")
    st.caption("Upload reports for OCR processing and AI analysis.")

    st.divider()

    # --------------------------------------------------------
    # Load Patients
    # --------------------------------------------------------

    with st.spinner("Loading patients..."):

        patient_response = get("/patients/")

    if patient_response.status_code != 200:

        st.error("Unable to load patients.")

        return

    patients = patient_response.json()

    # --------------------------------------------------------
    # Load Doctors
    # --------------------------------------------------------

    with st.spinner("Loading doctors..."):

        doctor_response = get("/doctors/")

    if doctor_response.status_code != 200:

        st.error("Unable to load doctors.")

        return

    doctors = doctor_response.json()

    # --------------------------------------------------------
    # Dropdown Data
    # --------------------------------------------------------

    patient_map = {
        f"{p['patient_id']} - {p['full_name']}": p["id"]
        for p in patients
    }

    doctor_map = {
        f"{d['doctor_id']} - {d['full_name']}": d["id"]
        for d in doctors
    }

    # --------------------------------------------------------
    # Upload Form
    # --------------------------------------------------------

    with st.form("upload_form"):

        st.subheader("Report Information")

        col1, col2 = st.columns(2)

        with col1:

            patient = st.selectbox(
                "👤 Patient",
                list(patient_map.keys()),
            )

            report_name = st.text_input(
                "📄 Report Name",
                placeholder="Example: Blood Test - July",
            )

        with col2:

            doctor = st.selectbox(
                "👨‍⚕️ Doctor",
                list(doctor_map.keys()),
            )

            report_type = st.selectbox(
                "📑 Report Type",
                [
                    "Blood Test",
                    "X-Ray",
                    "MRI",
                    "CT Scan",
                    "ECG",
                    "Prescription",
                    "Discharge Summary",
                    "Other",
                ],
            )

        st.divider()

        uploaded_file = st.file_uploader(
            "Choose Report",
            type=[
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "docx",
            ],
            help="Supported formats: PDF, DOCX, PNG, JPG, JPEG",
        )

        st.info(
            "Maximum supported file types: PDF, DOCX, PNG, JPG, JPEG"
        )

        submit = st.form_submit_button(
            "📤 Upload Report",
            use_container_width=True,
            type="primary",
        )

    # --------------------------------------------------------
    # Wait for Part 2
    # --------------------------------------------------------

    if not submit:
        return

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if uploaded_file is None:

        st.warning("Please choose a report file.")

        return

    if not report_name.strip():

        st.warning("Report name is required.")

        return

    patient_id = patient_map[patient]

    doctor_id = doctor_map[doctor]

    st.divider()

    st.success("✅ Validation Successful")

    # Upload logic will be added in Part 2
    st.success("✅ Validation Successful")
    # --------------------------------------------------------
    # Upload Report
    # --------------------------------------------------------

    with st.spinner("Uploading report..."):

        data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "report_name": report_name,
            "report_type": report_type,
        }

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type,
            )
        }

        response = post(
            "/reports/upload",
            data=data,
            files=files,
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    if response.status_code != 201:

        st.error("Upload failed.")

        try:
            st.error(response.json()["detail"])
        except Exception:
            st.code(response.text)

        return

    result = response.json()

    report = result["report"]

    st.success("🎉 Report Uploaded Successfully")

    st.balloons()

    st.divider()

    st.subheader("Uploaded Report")

    c1, c2 = st.columns(2)

    with c1:

        st.text_input(
            "Report ID",
            value=report["report_id"],
            disabled=True,
        )

        st.text_input(
            "Report Name",
            value=report["report_name"],
            disabled=True,
        )

        st.text_input(
            "Report Type",
            value=report["report_type"],
            disabled=True,
        )

    with c2:

        st.text_input(
            "Patient ID",
            value=str(report["patient_id"]),
            disabled=True,
        )

        st.text_input(
            "Doctor ID",
            value=str(report["doctor_id"]),
            disabled=True,
        )

        st.text_input(
            "Uploaded At",
            value=report["created_at"][:19],
            disabled=True,
        )

    st.divider()

    # --------------------------------------------------------
    # AI Summary
    # --------------------------------------------------------

    st.subheader("🤖 AI Report Summary")

    if st.button(
        "Generate AI Summary",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Generating summary..."):

            summary_response = post(
                f"/reports/summarize/{report['id']}"
            )

        if summary_response.status_code == 200:

            summary = summary_response.json()["summary"]

            st.success("Summary Generated")

            st.markdown(summary)

        else:

            st.error("Unable to generate summary.")

            try:
                st.error(
                    summary_response.json()["detail"]
                )
            except Exception:
                st.code(summary_response.text)    