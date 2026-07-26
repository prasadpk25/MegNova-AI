import pandas as pd
import streamlit as st

from utils.api_client import get
from utils.helpers import handle_response


def patients_page():
    """Patient Management Page"""

    st.title("👥 Patient Management")
    st.caption("View and manage registered patients.")

    st.divider()

    # =====================================
    # Fetch Patients
    # =====================================

    with st.spinner("Loading patient records..."):
        response = get("/patients/")
        data = handle_response(response)

    if not data:
        st.warning("No patient records found.")
        return

    df = pd.DataFrame(data)

    # =====================================
    # Validate Columns
    # =====================================

    required_columns = [
        "patient_id",
        "full_name",
        "gender",
        "date_of_birth",
        "blood_group",
        "phone",
        "email",
        "is_active",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        return

    # =====================================
    # Search & Filter
    # =====================================

    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(
            "🔍 Search Patient",
            placeholder="Search by Patient ID or Name",
        )

    with col2:
        status = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"],
        )

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["full_name"].astype(str).str.contains(search, case=False, na=False)
            | filtered["patient_id"].astype(str).str.contains(search, case=False, na=False)
        ]

    if status == "Active":
        filtered = filtered[filtered["is_active"]]

    elif status == "Inactive":
        filtered = filtered[~filtered["is_active"]]

    # =====================================
    # Dashboard Metrics
    # =====================================

    total = len(df)
    active = len(df[df["is_active"]])
    inactive = total - active

    c1, c2, c3 = st.columns(3)

    c1.metric("👥 Total Patients", total)
    c2.metric("🟢 Active", active)
    c3.metric("🔴 Inactive", inactive)

    st.divider()

    # =====================================
    # Display Table
    # =====================================

    display_df = filtered[
        [
            "patient_id",
            "full_name",
            "gender",
            "date_of_birth",
            "blood_group",
            "phone",
            "email",
            "is_active",
        ]
    ].copy()

    display_df["Status"] = display_df["is_active"].map(
        {
            True: "🟢 Active",
            False: "🔴 Inactive",
        }
    )

    display_df.drop(columns=["is_active"], inplace=True)

    display_df.rename(
        columns={
            "patient_id": "Patient ID",
            "full_name": "Full Name",
            "gender": "Gender",
            "date_of_birth": "Date of Birth",
            "blood_group": "Blood Group",
            "phone": "Phone",
            "email": "Email",
        },
        inplace=True,
    )

    st.subheader("📋 Patient Records")

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    # =====================================
    # Actions
    # =====================================

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📥 Download CSV",
            display_df.to_csv(index=False),
            file_name="patients.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()

    st.divider()

    st.caption(
        f"Showing {len(filtered)} of {len(df)} patient(s)"
    )