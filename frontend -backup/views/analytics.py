import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api_client import get


# ==========================================================
# Hospital Analytics Dashboard
# ==========================================================

def analytics_page():
    """Hospital Analytics Dashboard"""

    st.title("ðŸ“Š Hospital Analytics Dashboard")
    st.caption("Real-time insights for MegNova AI")

    if st.button(
        "ðŸ”„ Refresh Dashboard",
        key="analytics_refresh",
        width="stretch",
    ):
        st.rerun()

    # =====================================================
    # Load Analytics
    # =====================================================

    with st.spinner("Loading analytics..."):

        response = get("/analytics/dashboard")

    if response.status_code != 200:

        try:
            message = response.json().get(
                "detail",
                "Unable to load analytics.",
            )
        except Exception:
            message = "Unable to load analytics."

        st.error(message)
        return

    data = response.json()

    # =====================================================
    # Metrics
    # =====================================================

    total_patients = data.get("total_patients", 0)
    active_patients = data.get("active_patients", 0)

    total_doctors = data.get("total_doctors", 0)
    active_doctors = data.get("active_doctors", 0)

    total_reports = data.get("total_reports", 0)

    # =====================================================
    # DataFrames
    # =====================================================

    departments = pd.DataFrame(
        data.get("departments", [])
    )

    specializations = pd.DataFrame(
        data.get("specializations", [])
    )

    report_types = pd.DataFrame(
        data.get("report_types", [])
    )

    # =====================================================
    # Overview
    # =====================================================

    st.divider()

    st.subheader("ðŸ“ˆ Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        label="Patients",
        value=total_patients,
        delta=f"{active_patients} Active",
    )

    c2.metric(
        label="Doctors",
        value=total_doctors,
        delta=f"{active_doctors} Active",
    )

    c3.metric(
        label="Reports",
        value=total_reports,
    )

    # =====================================================
    # Charts
    # =====================================================

    st.divider()

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # Doctors by Department
    # -----------------------------------------------------

    with col1:

        st.subheader("ðŸ¥ Doctors by Department")

        if not departments.empty:

            fig = px.bar(
                departments,
                x="department",
                y="count",
                text="count",
            )

            fig.update_layout(
                xaxis_title="Department",
                yaxis_title="Doctors",
                height=420,
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

        else:

            st.info("No department data available.")

    # -----------------------------------------------------
    # Report Types
    # -----------------------------------------------------

    with col2:

        st.subheader("ðŸ“„ Report Types")

        if not report_types.empty:

            fig = px.pie(
                report_types,
                names="type",
                values="count",
                hole=0.45,
            )

            fig.update_layout(
                height=420,
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

        else:

            st.info("No report data available.")

    # =====================================================
    # Specializations
    # =====================================================

    st.divider()

    st.subheader("ðŸ‘¨â€âš•ï¸ Doctor Specializations")

    if not specializations.empty:

        fig = px.bar(
            specializations,
            x="specialization",
            y="count",
            text="count",
        )

        fig.update_layout(
            xaxis_title="Specialization",
            yaxis_title="Doctors",
            height=420,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    else:

        st.info("No specialization data available.")

    # =====================================================
    # Analytics Tables
    # =====================================================

    st.divider()

    st.subheader("ðŸ“‹ Analytics Data")

    st.markdown("#### Departments")

    st.dataframe(
        departments,
        width="stretch",
        hide_index=True,
    )

    st.markdown("#### Specializations")

    st.dataframe(
        specializations,
        width="stretch",
        hide_index=True,
    )

    st.markdown("#### Report Types")

    st.dataframe(
        report_types,
        width="stretch",
        hide_index=True,
    )

    # =====================================================
    # Export Analytics
    # =====================================================

    st.divider()

    export = pd.DataFrame(
        {
            "Metric": [
                "Total Patients",
                "Active Patients",
                "Total Doctors",
                "Active Doctors",
                "Total Reports",
            ],
            "Value": [
                total_patients,
                active_patients,
                total_doctors,
                active_doctors,
                total_reports,
            ],
        }
    )

    csv = export.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="ðŸ“¥ Download Analytics",
        data=csv,
        file_name="analytics.csv",
        mime="text/csv",
        key="download_analytics",
        width="stretch",
    )
