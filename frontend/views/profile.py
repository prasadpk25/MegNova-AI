import streamlit as st

from utils.api_client import get


# ==========================================================
# User Profile
# ==========================================================

def profile_page():
    """User Profile Page"""

    st.title("👤 My Profile")
    st.caption("Manage your MegNova AI account.")

    if st.button(
        "🔄 Refresh",
        key="profile_refresh",
        use_container_width=True,
    ):
        st.rerun()

    st.divider()

    # =====================================================
    # Load User
    # =====================================================

    with st.spinner("Loading profile..."):

        response = get("/auth/me")

    if response.status_code != 200:

        try:
            message = response.json().get(
                "detail",
                "Unable to load profile.",
            )
        except Exception:
            message = "Unable to load profile."

        st.error(message)
        return

    user = response.json()

    full_name = user.get("full_name", "Unknown User")
    email = user.get("email", "N/A")
    role = user.get("role", "user")
    is_active = user.get("is_active", False)
    user_id = user.get("id", "N/A")
    created = user.get("created_at")

    st.divider()

    # =====================================================
    # Profile Header
    # =====================================================

    left, right = st.columns([1, 4])

    with left:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=120,
        )

    with right:

        st.subheader(full_name)

        st.write(email)

        if is_active:
            st.success(f"🟢 {role.upper()}")
        else:
            st.error("🔴 ACCOUNT DISABLED")

    st.divider()

    # =====================================================
    # Overview
    # =====================================================

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "User ID",
        user_id,
    )

    k2.metric(
        "Role",
        role.title(),
    )

    k3.metric(
        "Status",
        "Active" if is_active else "Inactive",
    )

    k4.metric(
        "Member Since",
        created[:10] if created else "N/A",
    )

    st.divider()

    # =====================================================
    # Tabs
    # =====================================================

    personal_tab, security_tab, stats_tab, export_tab = st.tabs(
        [
            "👤 Personal",
            "🔐 Security",
            "📊 Statistics",
            "📥 Export",
        ]
    )

    # =====================================================
    # Personal
    # =====================================================

    with personal_tab:

        st.subheader("Personal Information")

        c1, c2 = st.columns(2)

        with c1:

            st.text_input(
                "Full Name",
                value=full_name,
                disabled=True,
                key="profile_name",
            )

            st.text_input(
                "Email",
                value=email,
                disabled=True,
                key="profile_email",
            )

            st.text_input(
                "User ID",
                value=str(user_id),
                disabled=True,
                key="profile_userid",
            )

        with c2:

            st.text_input(
                "Role",
                value=role.title(),
                disabled=True,
                key="profile_role",
            )

            st.text_input(
                "Account Status",
                value="Active" if is_active else "Inactive",
                disabled=True,
                key="profile_status",
            )

            st.text_input(
                "Email Verified",
                value="Yes",
                disabled=True,
                key="profile_verified",
            )

    # =====================================================
    # Security
    # =====================================================

    with security_tab:

        st.subheader("Security")

        st.info(
            "Password update will be available once the backend API is implemented."
        )

        current_password = st.text_input(
            "Current Password",
            type="password",
            key="current_password",
        )

        new_password = st.text_input(
            "New Password",
            type="password",
            key="new_password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password",
        )

        if st.button(
            "🔐 Update Password",
            key="update_password",
            use_container_width=True,
        ):

            if not current_password:

                st.warning("Please enter your current password.")

            elif not new_password:

                st.warning("Please enter a new password.")

            elif len(new_password) < 8:

                st.warning(
                    "Password should contain at least 8 characters."
                )

            elif new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                st.info(
                    "Backend password update endpoint is not available yet."
                )

    # =====================================================
    # Statistics
    # =====================================================

    with stats_tab:

        st.subheader("Account Statistics")

        a, b = st.columns(2)

        a.metric(
            "User ID",
            user_id,
        )

        b.metric(
            "Role",
            role.title(),
        )

        c, d = st.columns(2)

        c.metric(
            "Account Status",
            "Active" if is_active else "Inactive",
        )

        d.metric(
            "Platform",
            "MegNova AI",
        )

        st.success("Profile loaded successfully.")

    # =====================================================
    # Export
    # =====================================================

    with export_tab:

        st.subheader("Export Profile")

        profile_text = f"""User ID      : {user_id}
Full Name    : {full_name}
Email        : {email}
Role         : {role}
Status       : {"Active" if is_active else "Inactive"}
"""

        st.text_area(
            "Preview",
            value=profile_text,
            height=220,
            disabled=True,
            key="profile_preview",
        )

        st.download_button(
            label="📥 Download Profile",
            data=profile_text.encode("utf-8"),
            file_name="profile.txt",
            mime="text/plain",
            key="download_profile",
            use_container_width=True,
        )

    st.divider()

    st.caption("MegNova AI • AI Hospital Digital Twin")