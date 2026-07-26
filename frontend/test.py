import streamlit as st

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("Sidebar Test")
    st.write("Sidebar is working!")

st.title("Main Page")
st.write("Hello World")