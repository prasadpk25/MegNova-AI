import pandas as pd
import streamlit as st

from utils.api_client import get, post
from utils.helpers import handle_response


def doctors_page():
    """Doctor Management Page"""

    st.title("👨‍⚕️ Doctor Management")
    st.caption("Register and manage hospital doctors.")

    st.divider()

    # =====================================================
    # Register Doctor
    # =====================================================

    st.subheader("➕ Register Doctor")

    with st.form(
        "doctor_form",
        clear_on_submit=True,
    ):

        left, right = st.columns(2)

        with left:

            full_name = st.text_input(
                "Full Name",
                key="doctor_name",
            )

            email = st.text_input(
                "Email",
                key="doctor_email",
            )

            phone = st.text_input(
                "Phone",
                key="doctor_phone",
            )

            department = st.text_input(
                "Department",
                key="doctor_department",
            )

            specialization = st.text_input(
                "Specialization",
                key="doctor_specialization",
            )

        with right:

            qualification = st.text_input(
                "Qualification",
                key="doctor_qualification",
            )

            experience_years = st.number_input(
                "Experience (Years)",
                min_value=0,
                step=1,
                key="doctor_experience",
            )

            license_number = st.text_input(
                "License Number",
                key="doctor_license",
            )

            availability = st.selectbox(
                "Availability",
                [
                    "Available",
                    "Busy",
                    "On Leave",
                ],
                key="doctor_availability",
            )

        submit = st.form_submit_button(
            "➕ Add Doctor",
            use_container_width=True,
        )

    # =====================================================
    # Save Doctor
    # =====================================================

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

        if any(
            not str(field).strip()
            for field in required_fields
        ):

            st.warning(
                "Please fill in all required fields."
            )

        else:

            payload = {
                "full_name": full_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "department": department.strip(),
                "specialization": specialization.strip(),
                "qualification": qualification.strip(),
                "experience_years": experience_years,
                "license_number": license_number.strip(),
                "availability": availability,
            }

            with st.spinner(
                "Adding doctor..."
            ):

                response = post(
                    "/doctors/",
                    json=payload,
                )

                data = handle_response(response)

            if data:

                st.success(
                    "✅ Doctor added successfully."
                )

                st.rerun()

    st.divider()

    # =====================================================
    # Doctor List
    # =====================================================

    st.subheader("📋 Doctors")

    with st.spinner(
        "Loading doctors..."
    ):

        response = get("/doctors/")
        doctors = handle_response(response)

    if not doctors:

        st.info("No doctors found.")

        return

    df = pd.DataFrame(doctors)

    # =====================================================
    # Search & Filter
    # =====================================================

    left, right = st.columns([3, 1])

    with left:

        search = st.text_input(
            "🔍 Search Doctor",
            placeholder="Search by doctor's name...",
            key="doctor_search",
        )

    with right:

        status = st.selectbox(
            "Availability",
            [
                "All",
                "Available",
                "Busy",
                "On Leave",
            ],
            key="doctor_status_filter",
        )

    filtered = df.copy()

    if (
        search
        and "full_name" in filtered.columns
    ):

        filtered = filtered[
            filtered["full_name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    if (
        status != "All"
        and "availability" in filtered.columns
    ):

        filtered = filtered[
            filtered["availability"] == status
        ]

    # =====================================================
    # Metrics
    # =====================================================

    total = len(df)

    available = len(
        df[
            df["availability"] == "Available"
        ]
    )

    busy = len(
        df[
            df["availability"] == "Busy"
        ]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👨‍⚕️ Total",
        total,
    )

    c2.metric(
        "🟢 Available",
        available,
    )

    c3.metric(
        "🔴 Busy",
        busy,
    )

    st.divider()

    # =====================================================
    # Doctor Table
    # =====================================================

    display_columns = [
        column
        for column in [
            "doctor_id",
            "full_name",
            "department",
            "specialization",
            "experience_years",
            "availability",
            "phone",
            "email",
        ]
        if column in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    # =====================================================
    # Actions
    # =====================================================

    left, right = st.columns(2)

    with left:

        csv = (
            filtered[display_columns]
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name="doctors.csv",
            mime="text/csv",
            key="download_doctors_csv",
            use_container_width=True,
        )

    with right:

        if st.button(
            "🔄 Refresh",
            key="refresh_doctors",
            use_container_width=True,
        ):

            st.rerun()

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        f"Showing {len(filtered)} of {len(df)} doctors"
    )