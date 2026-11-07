
import os
import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "MEGNOVA_API_URL",
    "http://127.0.0.1:8000"
)


def get_auth_headers():
    token = st.session_state.get("access_token")

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}"
    }


def get_dashboard_data():
    headers = get_auth_headers()

    if not headers:
        return None, "Please log in again."

    try:
        response = requests.get(
            f"{API_BASE_URL}/dashboard/",
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:
            return response.json(), None

        if response.status_code == 401:
            return None, "Session expired. Please log in again."

        return None, f"Dashboard API error: {response.status_code}"

    except requests.RequestException:
        return None, "Cannot connect to MegNova AI backend."
