import streamlit as st


# ==========================================================
# Settings Page
# ==========================================================

def settings_page():
    """MegNova AI Settings"""

    st.title("⚙️ Settings")
    st.caption("Configure MegNova AI preferences and system settings.")

    st.divider()

    # =====================================================
    # Appearance
    # =====================================================

    st.subheader("🎨 Appearance")

    col1, col2 = st.columns(2)

    with col1:

        theme = st.selectbox(
            "Theme",
            [
                "System Default",
                "Light",
                "Dark",
            ],
            key="settings_theme",
        )

    with col2:

        layout = st.selectbox(
            "Layout",
            [
                "Wide",
                "Centered",
            ],
            key="settings_layout",
        )

    st.success("Appearance settings are ready.")

    st.divider()

    # =====================================================
    # AI Configuration
    # =====================================================

    st.subheader("🤖 AI Configuration")

    model = st.selectbox(
        "LLM Model",
        [
            "llama3",
            "mistral",
            "phi3",
        ],
        key="settings_model",
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
        key="settings_temperature",
    )

    max_tokens = st.slider(
        "Maximum Tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256,
        key="settings_max_tokens",
    )

    st.info(
        "These settings will be used for future AI model configuration."
    )

    st.divider()

    # =====================================================
    # OCR Configuration
    # =====================================================

    st.subheader("📄 OCR Configuration")

    language = st.selectbox(
        "OCR Language",
        [
            "English",
            "English + Telugu",
            "English + Hindi",
        ],
        key="settings_ocr_language",
    )

    gpu = st.checkbox(
        "Enable GPU Acceleration",
        value=False,
        key="settings_gpu",
    )

    st.divider()

    # =====================================================
    # Backend Configuration
    # =====================================================

    st.subheader("🌐 Backend Configuration")

    backend = st.text_input(
        "Backend URL",
        value="http://127.0.0.1:8000",
        key="settings_backend_url",
    )

    timeout = st.slider(
        "API Timeout (seconds)",
        min_value=5,
        max_value=120,
        value=30,
        step=5,
        key="settings_timeout",
    )

    st.divider()

    # =====================================================
    # System Information
    # =====================================================

    st.subheader("ℹ️ System Information")

    info1, info2 = st.columns(2)

    with info1:

        st.info("**Application**\n\nMegNova AI")

        st.info("**Version**\n\n1.0.0")

        st.info("**Frontend**\n\nStreamlit")

        st.info("**Backend**\n\nFastAPI")

    with info2:

        st.info("**Database**\n\nPostgreSQL")

        st.info("**Vector Database**\n\nQdrant")

        st.info("**OCR Engine**\n\nEasyOCR")

        st.info("**LLM Engine**\n\nOllama")

    st.divider()

    # =====================================================
    # Save Settings
    # =====================================================

    if st.button(
        "💾 Save Settings",
        key="settings_save",
        type="primary",
        use_container_width=True,
    ):

        st.success(
            "✅ Settings saved successfully. (Currently stored locally)"
        )

    st.divider()

    st.caption("MegNova AI • AI Hospital Digital Twin")