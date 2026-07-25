import streamlit as st

from utils.api_client import get


def profile_page():

    st.title("👤 My Profile")
    st.caption("Manage your MegNova AI account")

    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

    st.divider()

    # ============================================
    # Load User
    # ============================================

    with st.spinner("Loading profile..."):
        response = get("/auth/me")

    if response.status_code != 200:

        st.error("Unable to load profile.")

        st.code(response.text)

        return

    user = response.json()

    # ============================================
    # Header
    # ============================================

    col1, col2 = st.columns([1, 4])

    with col1:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=120,
        )

    with col2:

        st.subheader(user["full_name"])

        st.write(user["email"])

        if user["is_active"]:
            st.success(user["role"].upper())
        else:
            st.error("ACCOUNT DISABLED")

    st.divider()

    # ============================================
    # KPIs
    # ============================================

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "User ID",
        user["id"],
    )

    k2.metric(
        "Role",
        user["role"].title(),
    )

    k3.metric(
        "Status",
        "Active" if user["is_active"] else "Inactive",
    )

    created = user.get("created_at")

    k4.metric(
        "Member Since",
        created[:10] if created else "N/A",
    )

    st.divider()

    # ============================================
    # Tabs
    # ============================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "👤 Personal",
            "🔐 Security",
            "📊 Statistics",
            "📥 Export",
        ]
    )

    # ============================================
    # PERSONAL
    # ============================================

    with tab1:

        st.subheader("Personal Information")

        c1, c2 = st.columns(2)

        with c1:

            st.text_input(
                "Full Name",
                value=user["full_name"],
                disabled=True,
            )

            st.text_input(
                "Email",
                value=user["email"],
                disabled=True,
            )

            st.text_input(
                "User ID",
                value=str(user["id"]),
                disabled=True,
            )

        with c2:

            st.text_input(
                "Role",
                value=user["role"],
                disabled=True,
            )

            st.text_input(
                "Account Status",
                value="Active" if user["is_active"] else "Inactive",
                disabled=True,
            )

            st.text_input(
                "Email Verified",
                value="Yes",
                disabled=True,
            )
    # ============================================
    # SECURITY
    # ============================================

    with tab2:

        st.subheader("Security")

        st.info(
            "Password change functionality will be available once the backend API is implemented."
        )

        current_password = st.text_input(
            "Current Password",
            type="password",
        )

        new_password = st.text_input(
            "New Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
        )

        if st.button(
            "🔐 Update Password",
            use_container_width=True,
        ):

            if not current_password:
                st.warning("Enter your current password.")

            elif not new_password:
                st.warning("Enter a new password.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                st.info(
                    "Backend password update endpoint is not available yet."
                )

    # ============================================
    # STATISTICS
    # ============================================

    with tab3:

        st.subheader("Account Statistics")

        c1, c2 = st.columns(2)

        c1.metric("User ID", user["id"])
        c2.metric("Role", user["role"].title())

        c3, c4 = st.columns(2)

        c3.metric(
            "Account Status",
            "Active" if user["is_active"] else "Inactive",
        )

        c4.metric(
            "Platform",
            "MegNova AI",
        )

        st.success("Profile loaded successfully.")

    # ============================================
    # EXPORT
    # ============================================

    with tab4:

        st.subheader("Export Profile")

        profile_text = f"""
User ID      : {user['id']}
Full Name    : {user['full_name']}
Email        : {user['email']}
Role         : {user['role']}
Status       : {"Active" if user["is_active"] else "Inactive"}
"""

        st.text_area(
            "Preview",
            profile_text,
            height=220,
        )

        st.download_button(
            "📥 Download Profile",
            profile_text,
            file_name="profile.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.divider()

    st.caption(
        "MegNova AI • User Profile"
    )            