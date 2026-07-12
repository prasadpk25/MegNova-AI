import streamlit as st


def chatbot_page():

    st.title("🤖 AI Medical Assistant")

    st.write("Ask medical questions or upload patient information.")

    st.divider()

    # -----------------------------
    # Chat History
    # -----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # -----------------------------
    # Chat Input
    # -----------------------------
    prompt = st.chat_input("Ask anything about a patient...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Temporary AI Response
        response = f"""
You asked:

**{prompt}**

This is a placeholder AI response.

Later this will connect to:

✅ Llama 3

✅ Gemini

✅ OpenAI

✅ Medical RAG

✅ Patient Database
"""

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):
            st.markdown(response)