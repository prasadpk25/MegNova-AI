import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def get_headers():
    token = st.session_state.get("access_token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }