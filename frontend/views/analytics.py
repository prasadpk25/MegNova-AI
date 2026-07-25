import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api_client import get


def analytics_page():

    st.title("📊 Hospital Analytics Dashboard")
    st.caption("Real-time insights for MegNova AI")

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

    with st.spinner("Loading analytics..."):

        response = get("/analytics/dashboard")

    if response.status_code != 200:
        st.error("Unable to load analytics.")
        st.code(response.text)
        return

    data = response.json()

    total_patients = data["total_patients"]
    active_patients = data["active_patients"]

    total_doctors = data["total_doctors"]
    active_doctors = data["active_doctors"]

    total_reports = data["total_reports"]

    departments = pd.DataFrame(data["departments"])
    specializations = pd.DataFrame(data["specializations"])
    report_types = pd.DataFrame(data["report_types"])

    st.divider()

    st.subheader("Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Patients",
        total_patients,
        delta=f"{active_patients} Active",
    )

    c2.metric(
        "Doctors",
        total_doctors,
        delta=f"{active_doctors} Active",
    )

    c3.metric(
        "Reports",
        total_reports,
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Doctors by Department")

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
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info("No department data available.")

    with col2:

        st.subheader("Report Types")

        if not report_types.empty:

            fig = px.pie(
                report_types,
                names="type",
                values="count",
                hole=0.45,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info("No report data available.")

    st.divider()

    st.subheader("Doctor Specializations")

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
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("No specialization data available.")

    st.divider()

    st.subheader("Analytics Data")

    st.write("### Departments")
    st.dataframe(
        departments,
        use_container_width=True,
        hide_index=True,
    )

    st.write("### Specializations")
    st.dataframe(
        specializations,
        use_container_width=True,
        hide_index=True,
    )

    st.write("### Report Types")
    st.dataframe(
        report_types,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    export = pd.DataFrame({
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
    })

    csv = export.to_csv(index=False)

    st.download_button(
        "📥 Download Analytics",
        csv,
        "analytics.csv",
        "text/csv",
        use_container_width=True,
    )