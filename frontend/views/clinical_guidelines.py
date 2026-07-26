import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/clinical-guidelines/chat"


def clinical_guidelines_page():

    st.title("📚 Clinical Guideline Assistant")
    st.divider()

    st.write(
        "Ask evidence-based clinical questions using uploaded WHO, CDC, NICE, and NIH clinical guidelines."
    )

    question = st.text_area(
        "Clinical Question",
        height=140,
        placeholder="Example: What is the first-line treatment for hypertension?",
        key="clinical_guideline_question",
    )

    col1, col2 = st.columns([1, 5])

    with col1:

        ask = st.button(
            "🔍 Ask",
            key="ask_guideline_button",
            type="primary",
            use_container_width=True,
        )

    if ask:

        if not question.strip():

            st.warning("Please enter a clinical question.")
            return

        with st.spinner("Searching clinical guidelines..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question.strip()
                    },
                    timeout=120,
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer returned.",
                    )

                    st.success("Answer Generated")

                    st.markdown(answer)

                else:

                    try:
                        message = response.json().get(
                            "detail",
                            "Backend returned an error.",
                        )
                    except Exception:
                        message = "Backend returned an error."

                    st.error(message)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the FastAPI backend. Please ensure the backend server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            except Exception:

                st.error(
                    "An unexpected error occurred while processing your request."
                )

    st.divider()

    st.subheader("💡 Example Questions")

    examples = [
        "What is the first-line treatment for hypertension?",
        "What are the diagnostic criteria for diabetes mellitus?",
        "How should community-acquired pneumonia be managed?",
        "What are the WHO recommendations for tuberculosis treatment?",
        "Summarize the NICE guideline for asthma management.",
        "What are the contraindications for thrombolytic therapy?",
    ]

    for example in examples:

        st.markdown(f"• {example}")

    st.divider()

    st.caption(
        "MegNova AI • Clinical Guideline Assistant"
    )