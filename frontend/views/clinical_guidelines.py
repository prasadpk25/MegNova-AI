import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/clinical-guidelines/chat"


def clinical_guidelines_page():

    st.title("📚 Clinical Guideline Assistant")
    st.markdown("---")

    st.write(
        "Ask evidence-based clinical questions using the uploaded WHO, CDC, NICE and NIH guidelines."
    )

    question = st.text_area(
        "Enter your clinical question",
        height=120,
        placeholder="Example: What is the first-line treatment for hypertension?"
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        ask = st.button("🔍 Ask")

    if ask:

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        with st.spinner("Searching clinical guidelines..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.success("Answer")

                    st.markdown(answer)

                else:

                    st.error("Backend Error")
                    st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error("Cannot connect to FastAPI backend.\n\nStart the backend first.")

            except Exception as e:

                st.error(str(e))