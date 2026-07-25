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
    # Fetch Patient Data
    # =====================================

    with st.spinner("Loading patient records..."):
        response = get("/patients/")
        data = handle_response(response)

    if not data:
        st.info("No patient records found.")
        return

    df = pd.DataFrame(data)

    # =====================================
    # Search & Filter
    # =====================================

    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(
            "🔍 Search Patient",
            placeholder="Search by patient name...",
        )

    with col2:
        status = st.selectbox(
            "Status",
            [
                "All",
                "Active",
                "Inactive",
            ],
        )

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["full_name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    if status == "Active":
        filtered = filtered[
            filtered["is_active"] == True
        ]

    elif status == "Inactive":
        filtered = filtered[
            filtered["is_active"] == False
        ]

    # =====================================
    # Dashboard Metrics
    # =====================================

    total = len(df)

    active = len(
        df[df["is_active"] == True]
    )

    inactive = total - active

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👥 Total Patients",
        total,
    )

    c2.metric(
        "✅ Active",
        active,
    )

    c3.metric(
        "❌ Inactive",
        inactive,
    )

    st.divider()

    # =====================================
    # Patient Table
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

    display_df["is_active"] = display_df[
        "is_active"
    ].map(
        {
            True: "🟢 Active",
            False: "🔴 Inactive",
        }
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

    # =====================================
    # Footer
    # =====================================

    st.caption(
        f"Showing {len(filtered)} of {len(df)} patient(s)"
    )