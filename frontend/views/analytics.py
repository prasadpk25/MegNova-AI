import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analytics"

def analytics_page():

    st.title("📊 Hospital Analytics Dashboard")

    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error("Unable to fetch analytics")
        return

    data = response.json()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👨‍⚕️ Total Doctors", data["total_doctors"])

    with col2:
        st.metric("🧑‍🤝‍🧑 Active Doctors", data["active_doctors"])

    with col3:
        st.metric("📄 Total Reports", data["total_reports"])

    col4, col5 = st.columns(2)

    with col4:
        st.metric("🏥 Total Patients", data["total_patients"])

    with col5:
        st.metric("❤️ Active Patients", data["active_patients"])