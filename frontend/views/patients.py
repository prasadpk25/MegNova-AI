import streamlit as st
import pandas as pd

from utils.api_client import get
from utils.helpers import handle_response


def patients_page():

    st.title("👥 Patient Records")

    response = get("/patients/")
    data = handle_response(response)

    if not data:
        st.warning("No patient records found.")
        return

    df = pd.DataFrame(data)

    search = st.text_input(
        "🔍 Search Patient",
        placeholder="Search by patient name..."
    )

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["full_name"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.metric("👥 Total Patients", len(filtered))

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
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Download Patient Data",
        display_df.to_csv(index=False),
        "patients.csv",
        "text/csv",
    )