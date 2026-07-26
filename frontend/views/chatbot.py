import streamlit as st

from utils.api_client import post


def chatbot_page():

    st.title("🤖 MegNova AI Medical Assistant")

    st.caption(
        "Ask questions about uploaded medical reports using AI-powered Retrieval-Augmented Generation (RAG)."
    )

    st.divider()

    # =====================================================
    # Session State
    # =====================================================

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello Doctor!\n\n"
                    "I can answer questions based on uploaded medical reports.\n\n"
                    "**Example Questions**\n"
                    "- Summarize Rahul Sharma's reports\n"
                    "- Does the patient have diabetes?\n"
                    "- Show the latest blood test findings\n"
                    "- What medications are mentioned?\n"
                    "- What abnormalities were detected?\n"
                    "- Compare recent reports."
                ),
            }
        ]

    # =====================================================
    # Header Actions
    # =====================================================

    left, right = st.columns([6, 1])

    with right:

        if st.button(
            "🗑️ Clear",
            key="clear_chat_history",
            use_container_width=True,
        ):

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Conversation cleared.\n\n"
                        "How can I assist you today?"
                    ),
                }
            ]

            st.rerun()

    # =====================================================
    # Conversation
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # =====================================================
    # Chat Input
    # =====================================================

    prompt = st.chat_input(
        "Ask a question about a patient's medical reports..."
    )

    if prompt:

        prompt = prompt.strip()

        if not prompt:

            st.warning("Please enter a question.")

            return

        # =============================================
        # User Message
        # =============================================

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        # =============================================
        # AI Response
        # =============================================

        with st.chat_message("assistant"):

            with st.spinner(
                "MegNova AI is analyzing medical reports..."
            ):

                try:

                    response = post(
                        "/chat/",
                        json={
                            "question": prompt,
                        },
                    )

                    if response.status_code == 200:

                        data = response.json()

                        answer = data.get(
                            "answer",
                            "No response generated.",
                        )

                    else:

                        try:

                            answer = response.json().get(
                                "detail",
                                "Unable to process your request.",
                            )

                        except Exception:

                            answer = (
                                "Unable to process your request."
                            )

                except Exception:

                    answer = (
                        "Unable to connect to the backend service."
                    )

                st.markdown(answer)

        # =============================================
        # Save Assistant Response
        # =============================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    # =====================================================
    # Suggested Questions
    # =====================================================

    st.divider()

    st.subheader("💡 Suggested Questions")

    suggestions = [
        "Summarize the patient's reports.",
        "Does the patient have diabetes?",
        "List abnormal laboratory findings.",
        "What medications are mentioned?",
        "Compare the latest and previous reports.",
        "List allergies mentioned in the reports.",
        "What follow-up is recommended?",
        "Provide a concise discharge summary.",
    ]

    for question in suggestions:

        st.markdown(f"• {question}")

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "🏥 MegNova AI • Medical RAG Assistant"
    )