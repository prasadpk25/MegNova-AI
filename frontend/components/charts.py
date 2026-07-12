import streamlit as st
import plotly.express as px


def department_chart(df):

    dept = (
        df.groupby("department")
        .size()
        .reset_index(name="Patients")
    )

    fig = px.bar(
        dept,
        x="department",
        y="Patients",
        title="Patients by Department",
        text="Patients",
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Patients",
        template="plotly_dark",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)


def status_chart(df):

    status = (
        df.groupby("status")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        status,
        names="status",
        values="Count",
        title="Patient Status"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)