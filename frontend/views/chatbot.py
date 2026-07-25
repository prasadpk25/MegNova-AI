import streamlit as st

from utils.api_client import post


def chatbot_page():

    st.title("🤖 MegNova AI Medical Assistant")
    st.caption(
        "Ask questions about uploaded medical reports using AI-powered Retrieval-Augmented Generation (RAG)."
    )

    st.divider()

    # =====================================
    # Session State
    # =====================================

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello Doctor!\n\n"
                    "I can answer questions based on the uploaded and summarized medical reports.\n\n"
                    "Example questions:\n"
                    "- Summarize Rahul Sharma's reports\n"
                    "- Does the patient have diabetes?\n"
                    "- Show the latest blood test findings\n"
                    "- What medications are mentioned?"
                ),
            }
        ]

    # =====================================
    # Clear Chat
    # =====================================

    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. How can I help you?",
                }
            ]
            st.rerun()

    # =====================================
    # Display Conversation
    # =====================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # =====================================
    # Chat Input
    # =====================================

    prompt = st.chat_input(
        "Ask a question about a patient's medical reports..."
    )

    if prompt:

        # User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):

            with st.spinner("MegNova AI is analyzing medical reports..."):

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
                        "No response received.",
                    )

                else:

                    answer = (
                        f"❌ Error ({response.status_code})\n\n"
                        f"{response.text}"
                    )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )