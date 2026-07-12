import streamlit as st
import pandas as pd

from components.cards import metric_card
from components.charts import department_chart, status_chart

def dashboard_page():

    df = pd.read_csv("../datasets/patients.csv")

    st.title("🏥 AI Hospital Dashboard")

    st.write("Welcome Dr. Prasad 👋")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Patients", len(df))

    with col2:
        metric_card("ICU Patients",
                    len(df[df["department"]=="ICU"]))

    with col3:
        metric_card("Critical",
                    len(df[df["status"]=="Critical"]))

    with col4:
        metric_card("Avg Oxygen",
                    f"{df['oxygen_level'].mean():.1f}%")
        st.divider()

    col1, col2 = st.columns(2)

    with col1:
        department_chart(df)

    with col2:
        status_chart(df)