import streamlit as st


def settings_page():

    st.title("⚙️ Settings")
    st.caption("Configure MegNova AI")

    st.divider()

    # ===========================================
    # Appearance
    # ===========================================

    st.subheader("🎨 Appearance")

    theme = st.selectbox(
        "Theme",
        [
            "System Default",
            "Light",
            "Dark",
        ],
    )

    page_width = st.selectbox(
        "Layout",
        [
            "Wide",
            "Centered",
        ],
    )

    st.success("Appearance settings are ready.")

    st.divider()

    # ===========================================
    # AI Configuration
    # ===========================================

    st.subheader("🤖 AI Configuration")

    model = st.selectbox(
        "LLM Model",
        [
            "llama3",
            "mistral",
            "phi3",
        ],
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.2,
        0.1,
    )

    max_tokens = st.slider(
        "Maximum Tokens",
        256,
        4096,
        1024,
    )

    st.info("These values are for future AI configuration.")

    st.divider()

    # ===========================================
    # OCR
    # ===========================================

    st.subheader("📄 OCR")

    language = st.selectbox(
        "OCR Language",
        [
            "English",
            "English + Telugu",
            "English + Hindi",
        ],
    )

    gpu = st.checkbox(
        "Enable GPU",
        value=False,
    )

    st.divider()

    # ===========================================
    # Backend
    # ===========================================

    st.subheader("🌐 Backend")

    backend = st.text_input(
        "Backend URL",
        "http://127.0.0.1:8000",
    )

    timeout = st.slider(
        "API Timeout (seconds)",
        5,
        120,
        30,
    )

    st.divider()

    # ===========================================
    # About
    # ===========================================

    st.subheader("ℹ️ About")

    st.write("**MegNova AI**")
    st.write("AI Powered Hospital Digital Twin")

    st.write("Version: 1.0")

    st.write("Backend: FastAPI")

    st.write("Frontend: Streamlit")

    st.write("Database: PostgreSQL")

    st.write("Vector DB: Qdrant")

    st.write("OCR: EasyOCR")

    st.write("LLM: Ollama")

    st.divider()

    # ===========================================
    # Save
    # ===========================================

    if st.button(
        "💾 Save Settings",
        use_container_width=True,
        type="primary",
    ):

        st.success(
            "Settings saved successfully (local UI only)."
        )

    st.divider()

    st.caption("MegNova AI • Settings")