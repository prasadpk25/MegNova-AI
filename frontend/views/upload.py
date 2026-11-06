
import streamlit as st
from utils.api_client import get, post

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
    st.title("📤 Upload Medical Report")
    st.caption("Upload patient reports for OCR processing and AI analysis.")
    st.divider()

    # Preserve uploaded report across Streamlit reruns
    if "uploaded_report" not in st.session_state:
        st.session_state.uploaded_report = None

    if "generated_summary" not in st.session_state:
        st.session_state.generated_summary = None

    # Load patients
    with st.spinner("Loading patients..."):
        patient_response = get("/patients/")

    if patient_response.status_code != 200:
        st.error("Unable to load patient records.")
        return

    patients = patient_response.json()

    if not patients:
        st.warning("No patients available.")
        return

    # Load doctors
    with st.spinner("Loading doctors..."):
        doctor_response = get("/doctors/")

    if doctor_response.status_code != 200:
        st.error("Unable to load doctor records.")
        return

    doctors = doctor_response.json()

    if not doctors:
        st.warning("No doctors available.")
        return

    patient_map = {
        f"{p['patient_id']} - {p['full_name']}": p["id"]
        for p in patients
    }

    doctor_map = {
        f"{d['doctor_id']} - {d['full_name']}": d["id"]
        for d in doctors
    }

    # Upload form
    with st.form("upload_form", clear_on_submit=True):

        st.subheader("📋 Report Information")

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
                REPORT_TYPES,
            )

        uploaded_file = st.file_uploader(
            "Choose Medical Report",
            type=["pdf", "png", "jpg", "jpeg", "docx"],
        )

        submit = st.form_submit_button(
            "📤 Upload Report",
            type="primary",
            width="stretch",
        )

    # Process upload only when submitted
    if submit:

        if not report_name.strip():
            st.warning("Please enter a report name.")

        elif uploaded_file is None:
            st.warning("Please choose a report file.")

        else:
            payload = {
                "patient_id": patient_map[patient],
                "doctor_id": doctor_map[doctor],
                "report_name": report_name.strip(),
                "report_type": report_type,
            }

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                )
            }

            try:
                with st.spinner("Uploading medical report..."):
                    response = post(
                        "/reports/upload",
                        data=payload,
                        files=files,
                    )

                if response.status_code not in (200, 201):
                    try:
                        message = response.json().get(
                            "detail", "Unable to upload report."
                        )
                    except Exception:
                        message = "Unable to upload report."

                    st.error(message)

                else:
                    result = response.json()
                    report = result.get("report")

                    if not report or not report.get("id"):
                        st.error("Upload response did not contain a report ID.")
                    else:
                        st.session_state.uploaded_report = report
                        st.session_state.generated_summary = None
                        st.success("Medical report uploaded successfully!")
                        st.rerun()

            except Exception as error:
                st.error(f"Upload failed: {error}")

    # Display saved report outside the form
    report = st.session_state.uploaded_report

    if report:
        st.divider()
        st.subheader("📄 Uploaded Report")

        left, right = st.columns(2)

        with left:
            st.text_input(
                "Report ID",
                value=str(report.get("report_id", report.get("id", ""))),
                disabled=True,
                key="display_report_id",
            )

            st.text_input(
                "Report Name",
                value=report.get("report_name", ""),
                disabled=True,
                key="display_report_name",
            )

            st.text_input(
                "Report Type",
                value=report.get("report_type", ""),
                disabled=True,
                key="display_report_type",
            )

        with right:
            st.text_input(
                "Patient ID",
                value=str(report.get("patient_id", "")),
                disabled=True,
                key="display_patient_id",
            )

            st.text_input(
                "Doctor ID",
                value=str(report.get("doctor_id", "")),
                disabled=True,
                key="display_doctor_id",
            )

            created_at = report.get("created_at", "")
            st.text_input(
                "Uploaded At",
                value=str(created_at)[:19],
                disabled=True,
                key="display_uploaded_at",
            )

        st.divider()
        st.subheader("🤖 AI Report Summary")

        if st.button(
            "🧠 Generate AI Summary",
            key="generate_summary_upload",
            type="primary",
            width="stretch",
        ):
            with st.spinner("Extracting text and generating AI summary..."):
                try:
                    summary_response = post(
                        f"/reports/summarize/{report['id']}"
                    )

                    if summary_response.status_code == 200:
                        st.session_state.generated_summary = (
                            summary_response.json().get(
                                "summary",
                                "No summary returned.",
                            )
                        )
                    else:
                        try:
                            message = summary_response.json().get(
                                "detail",
                                "Unable to generate AI summary.",
                            )
                        except Exception:
                            message = summary_response.text

                        st.error(message)

                except Exception as error:
                    st.error(f"Summary request failed: {error}")

        if st.session_state.generated_summary:
            st.success("AI Summary Generated")

            st.text_area(
                "Medical Summary",
                value=st.session_state.generated_summary,
                height=250,
                disabled=True,
                key="display_generated_summary",
            )

        if st.button("Clear Uploaded Report"):
            st.session_state.uploaded_report = None
            st.session_state.generated_summary = None
            st.rerun()

    st.divider()
    st.caption("MegNova AI • Medical Report Upload Module")
