import pandas as pd
import streamlit as st

from utils.api_client import delete, get, post
from utils.helpers import handle_response

# ==========================================
# Constants
# ==========================================

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

# ==========================================
# Helper Functions
# ==========================================


def load_patients():
    """Fetch all patients."""

    response = get("/patients/")
    patients = handle_response(response)

    if not patients:
        return {}, []

    patient_dict = {
        patient["full_name"]: patient["id"]
        for patient in patients
    }

    return patient_dict, patients


def load_doctors():
    """Fetch all doctors."""

    response = get("/doctors/")
    doctors = handle_response(response)

    if not doctors:
        return {}, []

    doctor_dict = {
        doctor["full_name"]: doctor["id"]
        for doctor in doctors
    }

    return doctor_dict, doctors


# ==========================================
# Upload Section
# ==========================================


def upload_section(patient_dict, doctor_dict):
    """Upload Medical Report"""

    st.subheader("📤 Upload Medical Report")

    with st.form("upload_report_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            selected_patient = st.selectbox(
                "Patient",
                list(patient_dict.keys()),
            )

            report_name = st.text_input(
                "Report Name",
                placeholder="Enter report name",
            )

        with col2:

            selected_doctor = st.selectbox(
                "Doctor",
                list(doctor_dict.keys()),
            )

            report_type = st.selectbox(
                "Report Type",
                REPORT_TYPES,
            )

        uploaded_file = st.file_uploader(
            "Choose Medical Report",
            type=[
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "docx",
            ],
        )

        submit = st.form_submit_button(
            "📤 Upload Report",
            use_container_width=True,
        )

    # --------------------------------------

    if not submit:
        return

    # Validation

    if not patient_dict:

        st.error("No patients available.")
        return

    if not doctor_dict:

        st.error("No doctors available.")
        return

    if not report_name.strip():

        st.warning("Please enter report name.")
        return

    if uploaded_file is None:

        st.warning("Please select a medical report.")
        return

    payload = {
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

    with st.spinner("Uploading medical report..."):

        response = post(
            "/reports/upload",
            data=payload,
            files=files,
        )

    if response.status_code in (200, 201):

        st.success("✅ Medical report uploaded successfully.")

        st.rerun()

    else:

        try:
            message = response.json().get(
                "detail",
                "Upload failed.",
            )

        except Exception:
            message = response.text

        st.error(message)


# ==========================================
# Main Page (Part 1)
# ==========================================


def reports_page():

    st.title("📄 Medical Reports")

    st.caption(
        "Upload, manage and summarize patient medical reports."
    )

    st.divider()

    with st.spinner("Loading hospital data..."):

        patient_dict, _ = load_patients()

        doctor_dict, _ = load_doctors()

    upload_section(
        patient_dict,
        doctor_dict,
    )

    st.divider()

    # -----------------------------
    # Continue in Part 2

# ==========================================
# Load Reports
# ==========================================


def load_reports():
    """Fetch all medical reports."""

    with st.spinner("Loading medical reports..."):
        response = get("/reports/")
        reports = handle_response(response)

    if not reports:
        return pd.DataFrame()

    rows = []

    for report in reports:

        patient = report.get("patient", {})
        doctor = report.get("doctor", {})

        rows.append(
            {
                "ID": report["report_id"],
                "ReportID": report["id"],
                "Patient": patient.get("full_name", "N/A"),
                "Doctor": doctor.get("full_name", "N/A"),
                "Report": report.get("report_name", ""),
                "Type": report.get("report_type", ""),
                "File": report.get("file_name", ""),
                "Created": report.get("created_at", "")[:10],
                "Summary": (
                    "Available"
                    if report.get("summary")
                    else "Pending"
                ),
                "SummaryText": report.get("summary") or "",
            }
        )

    return pd.DataFrame(rows)


# ==========================================
# Dashboard Metrics
# ==========================================


def metrics_section(df):

    total = len(df)

    summarized = len(
        df[df["Summary"] == "Available"]
    )

    pending = total - summarized

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📄 Reports",
        total,
    )

    c2.metric(
        "🤖 AI Summaries",
        summarized,
    )

    c3.metric(
        "⏳ Pending",
        pending,
    )


# ==========================================
# Search & Filters
# ==========================================


def filter_reports(df):

    st.subheader("🔍 Search & Filter")

    col1, col2 = st.columns(2)

    with col1:

        search = st.text_input(
    "🔍 Search Reports",
    placeholder="Search by report name...",
    key="reports_search",
)

        patient = st.selectbox(
            "Patient",
            ["All"] + sorted(df["Patient"].unique().tolist()),
        )

    with col2:

        report_type = st.selectbox(
            "Report Type",
            ["All"] + sorted(df["Type"].unique().tolist()),
        )

        summary = st.selectbox(
            "Summary Status",
            [
                "All",
                "Available",
                "Pending",
            ],
        )

    filtered = df.copy()

    if search:

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        ]

    if patient != "All":

        filtered = filtered[
            filtered["Patient"] == patient
        ]

    if report_type != "All":

        filtered = filtered[
            filtered["Type"] == report_type
        ]

    if summary != "All":

        filtered = filtered[
            filtered["Summary"] == summary
        ]

    return filtered


# ==========================================
# Reports Table
# ==========================================


def reports_table(df):

    st.subheader("📋 Uploaded Reports")

    display = df[
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
    ]

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📥 Download CSV",
            display.to_csv(index=False),
            file_name="reports.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:

        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()

    st.caption(
        f"Showing {len(df)} report(s)"
    )


# ==========================================
# Continue Main Page
# ==========================================

    reports_df = load_reports()

    if reports_df.empty:

        st.info(
            "No medical reports found. Upload one to get started."
        )

        return

    metrics_section(reports_df)

    st.divider()

    filtered_df = filter_reports(reports_df)

    st.divider()

    reports_table(filtered_df)

    st.divider()

    # -----------------------------
    # Continue in Part 3
    # -----------------------------
    # ==========================================
# AI Summary Section
# ==========================================

def ai_summary_section(df):
    """Generate and view AI summaries."""

    st.subheader("🤖 AI Medical Summary")

    report_options = {
        f'{row["ID"]} - {row["Report"]}': row["ReportID"]
        for _, row in df.iterrows()
    }

    selected = st.selectbox(
        "Select Report",
        list(report_options.keys()),
    )

    report_db_id = report_options[selected]

    selected_row = df[df["ReportID"] == report_db_id].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🧠 Generate AI Summary",
            use_container_width=True,
        ):

            with st.spinner("Generating AI Summary..."):

                response = post(
                    f"/reports/summarize/{report_db_id}"
                )

            if response.status_code == 200:

                st.success("AI Summary generated successfully.")

                st.rerun()

            else:

                try:
                    message = response.json().get(
                        "detail",
                        "Failed to generate summary.",
                    )

                except Exception:
                    message = response.text

                st.error(message)

    with col2:

        confirm_delete = st.checkbox(
            "Confirm Delete"
        )

        if st.button(
            "🗑 Delete Report",
            use_container_width=True,
            type="secondary",
            disabled=not confirm_delete,
        ):

            response = delete(
                f"/reports/{report_db_id}"
            )

            if response.status_code == 200:

                st.success("Report deleted successfully.")

                st.rerun()

            else:

                st.error("Failed to delete report.")

    st.divider()

    # =====================================
    # Summary Viewer
    # =====================================

    st.subheader("📑 AI Summary")

    summary = selected_row["SummaryText"]

    if summary:

        st.text_area(
            "Summary",
            value=summary,
            height=220,
            disabled=True,
        )

    else:

        st.info(
            "No AI summary available for this report."
        )

    st.divider()

    # =====================================
    # Report Details
    # =====================================

    st.subheader("📋 Report Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Patient**")
        st.success(selected_row["Patient"])

        st.write("**Doctor**")
        st.success(selected_row["Doctor"])

        st.write("**Report Name**")
        st.info(selected_row["Report"])

    with col2:

        st.write("**Report Type**")
        st.info(selected_row["Type"])

        st.write("**Uploaded File**")
        st.info(selected_row["File"])

        st.write("**Created On**")
        st.info(selected_row["Created"])


# ==========================================
# Main Page
# ==========================================

def reports_page():

    st.title("📄 Medical Reports")

    st.caption(
        "Upload, manage and summarize patient medical reports."
    )

    st.divider()

    # ----------------------------
    # Load master data
    # ----------------------------

    with st.spinner("Loading hospital data..."):

        patient_dict, _ = load_patients()
        doctor_dict, _ = load_doctors()

    upload_section(
        patient_dict,
        doctor_dict,
    )

    st.divider()

    # ----------------------------
    # Load reports
    # ----------------------------

    reports_df = load_reports()

    if reports_df.empty:

        st.info(
            "No medical reports found."
        )

        return

    metrics_section(reports_df)

    st.divider()

    filtered_df = filter_reports(
        reports_df
    )

    st.divider()

    reports_table(filtered_df)

    st.divider()

    ai_summary_section(filtered_df)