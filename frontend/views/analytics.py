import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api_client import get


# ==========================================================
# Hospital Analytics Dashboard
# ==========================================================

def analytics_page():
    """Hospital Analytics Dashboard"""

    st.title("📊 Hospital Analytics Dashboard")
    st.caption("Real-time insights for MegNova AI")

    if st.button(
        "🔄 Refresh Dashboard",
        key="analytics_refresh",
        use_container_width=True,
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

    st.subheader("📈 Overview")

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

        st.subheader("🏥 Doctors by Department")

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
                use_container_width=True,
            )

        else:

            st.info("No department data available.")

    # -----------------------------------------------------
    # Report Types
    # -----------------------------------------------------

    with col2:

        st.subheader("📄 Report Types")

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
                use_container_width=True,
            )

        else:

            st.info("No report data available.")

    # =====================================================
    # Specializations
    # =====================================================

    st.divider()

    st.subheader("👨‍⚕️ Doctor Specializations")

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
            use_container_width=True,
        )

    else:

        st.info("No specialization data available.")

    # =====================================================
    # Analytics Tables
    # =====================================================

    st.divider()

    st.subheader("📋 Analytics Data")

    st.markdown("#### Departments")

    st.dataframe(
        departments,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Specializations")

    st.dataframe(
        specializations,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Report Types")

    st.dataframe(
        report_types,
        use_container_width=True,
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
        label="📥 Download Analytics",
        data=csv,
        file_name="analytics.csv",
        mime="text/csv",
        key="download_analytics",
        use_container_width=True,
    )