import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


def headers():
    token = st.session_state.get("access_token")

    if token:
        return {
            "Authorization": f"Bearer {token}"
        }

    return {}


def get(endpoint):
    return requests.get(
        BASE_URL + endpoint,
        headers=headers(),
    )


def post(endpoint, json=None, data=None, files=None):
    return requests.post(
        BASE_URL + endpoint,
        json=json,
        data=data,
        files=files,
        headers=headers(),
    )


def put(endpoint, json=None):
    return requests.put(
        BASE_URL + endpoint,
        json=json,
        headers=headers(),
    )


def delete(endpoint):
    return requests.delete(
        BASE_URL + endpoint,
        headers=headers(),
    )