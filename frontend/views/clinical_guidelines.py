
import streamlit as st
from utils.api_client import post


def clinical_guidelines_page():

    st.title("Clinical Guideline Assistant")
    st.caption(
        "Ask questions about clinical guidelines available in the knowledge base."
    )

    st.divider()

    st.info(
        "This assistant provides informational clinical guidance "
        "based on available uploaded documents. It is not a diagnostic tool."
    )

    question = st.text_area(
        "Clinical Question",
        height=130,
        placeholder="Example: What do the available guidelines say about hypertension?",
        key="clinical_guideline_question"
    )

    if st.button(
        "Search Clinical Guidelines",
        type="primary",
        key="ask_guideline_button",
        width="stretch"
    ):

        if not question.strip():
            st.warning("Please enter a clinical question.")

        else:
            try:
                with st.spinner("Searching clinical guidelines..."):

                    response = post(
                        "/clinical-guidelines/chat",
                        json={"question": question.strip()}
                    )

                if response.status_code == 200:

                    data = response.json()
                    answer = data.get("answer", "No answer returned.")

                    st.success("Response received")
                    st.markdown(answer)

                    with st.expander("View request details"):
                        st.write("Question:", question)

                else:
                    try:
                        error_data = response.json()
                        message = error_data.get(
                            "detail",
                            "Backend returned an error."
                        )
                    except Exception:
                        message = response.text[:1000]

                    st.error(f"API Error ({response.status_code}): {message}")

            except Exception as e:
                st.error("Unable to contact the Clinical Guidelines API.")
                st.code(str(e))

    st.divider()

    st.subheader("Example Questions")

    examples = [
        "What do the available guidelines say about hypertension?",
        "What are the diagnostic criteria for diabetes?",
        "How is community-acquired pneumonia managed?",
        "What do the uploaded documents say about tuberculosis?",
        "Summarize the available asthma guidelines.",
        "What are the contraindications for thrombolytic therapy?"
    ]

    for example in examples:
        st.write(f"- {example}")

    st.divider()

    st.caption("MegNova AI | Clinical Guideline Assistant")
