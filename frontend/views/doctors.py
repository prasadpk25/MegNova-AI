import pandas as pd
import streamlit as st

from utils.api_client import get, post
from utils.helpers import handle_response


def doctors_page():
    """Doctor Management Page"""

    st.title("👨‍⚕️ Doctor Management")
    st.caption("Register and manage hospital doctors.")

    st.divider()

    # =====================================
    # Add Doctor
    # =====================================

    st.subheader("➕ Register Doctor")

    with st.form("doctor_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            department = st.text_input("Department")
            specialization = st.text_input("Specialization")

        with col2:
            qualification = st.text_input("Qualification")

            experience_years = st.number_input(
                "Experience (Years)",
                min_value=0,
                step=1,
            )

            license_number = st.text_input(
                "License Number"
            )

            availability = st.selectbox(
                "Availability",
                [
                    "Available",
                    "Busy",
                    "On Leave",
                ],
            )

        submit = st.form_submit_button(
            "➕ Add Doctor",
            use_container_width=True,
        )

    # =====================================
    # Save Doctor
    # =====================================

    if submit:

        required_fields = [
            full_name,
            email,
            phone,
            department,
            specialization,
            qualification,
            license_number,
        ]

        if any(not str(field).strip() for field in required_fields):
            st.warning("Please fill in all required fields.")
            return

        payload = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "department": department,
            "specialization": specialization,
            "qualification": qualification,
            "experience_years": experience_years,
            "license_number": license_number,
            "availability": availability,
        }

        with st.spinner("Adding doctor..."):

            response = post(
                "/doctors/",
                json=payload,
            )

            data = handle_response(response)

        if data:
            st.success("✅ Doctor added successfully.")
            st.rerun()

    st.divider()

    # =====================================
    # Doctors List
    # =====================================

    st.subheader("📋 Doctors")

    with st.spinner("Loading doctors..."):

        response = get("/doctors/")
        doctors = handle_response(response)

    if not doctors:
        st.info("No doctors found.")
        return

    df = pd.DataFrame(doctors)

    # =====================================
    # Search & Filter
    # =====================================

    col1, col2 = st.columns([3, 1])

    with col1:

        search = st.text_input(
            "🔍 Search Doctor",
            placeholder="Search by doctor's name...",
        )

    with col2:

        status = st.selectbox(
            "Availability",
            [
                "All",
                "Available",
                "Busy",
                "On Leave",
            ],
        )

    filtered = df.copy()

    if search:

        filtered = filtered[
            filtered["full_name"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    if status != "All":

        filtered = filtered[
            filtered["availability"] == status
        ]

    # =====================================
    # Metrics
    # =====================================

    total = len(df)

    available = len(
        df[df["availability"] == "Available"]
    )

    busy = len(
        df[df["availability"] == "Busy"]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("👨‍⚕️ Total", total)
    c2.metric("🟢 Available", available)
    c3.metric("🔴 Busy", busy)

    st.divider()

    # =====================================
    # Table
    # =====================================

    display_df = filtered[
        [
            "doctor_id",
            "full_name",
            "department",
            "specialization",
            "experience_years",
            "availability",
            "phone",
            "email",
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    # =====================================
    # Actions
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📥 Download CSV",
            display_df.to_csv(index=False),
            file_name="doctors.csv",
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
        f"Showing {len(filtered)} of {len(df)} doctors"
    )