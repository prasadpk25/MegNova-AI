import streamlit as st
import pandas as pd
from utils.api_client import get, post
from utils.helpers import handle_response


def doctors_page():

    st.title("👨‍⚕️ Doctor Management")

    st.write("Manage hospital doctors.")

    st.divider()

    # ==========================
    # Add Doctor
    # ==========================

    st.subheader("➕ Add Doctor")

    with st.form("doctor_form"):

        full_name = st.text_input("Full Name")

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        department = st.text_input("Department")

        specialization = st.text_input("Specialization")

        qualification = st.text_input("Qualification")

        experience_years = st.number_input(
            "Experience (Years)",
            min_value=0,
            step=1,
        )

        license_number = st.text_input("License Number")

        availability = st.selectbox(
            "Availability",
            [
                "Available",
                "Busy",
                "On Leave",
            ],
        )

        submit = st.form_submit_button(
            "Add Doctor",
            use_container_width=True,
        )

    if submit:

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

        response = post(
            "/doctors/",
            json=payload,
        )

        data = handle_response(response)

        if data:
            st.success("Doctor added successfully.")
            st.rerun()

    st.divider()

    # ==========================
    # View Doctors
    # ==========================

    st.subheader("📋 Doctors List")

    response = get("/doctors/")

    doctors = handle_response(response)

    if doctors:

        df = pd.DataFrame(doctors)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No doctors found.")