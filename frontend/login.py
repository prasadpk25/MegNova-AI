import streamlit as st
from utils.api import login


def login_page():
    """MegNova AI sign-in screen."""
    st.markdown(
        """
        <style>
        .block-container { max-width: 1080px; padding-top: 5vh; }
        .login-hero {
          min-height:520px; padding:48px; border-radius:24px;
          background:radial-gradient(circle at 90% 10%,rgba(55,190,168,.30),transparent 30%),
            linear-gradient(145deg,#10253a,#173f53 65%,#0e766f);
          display:flex; flex-direction:column; justify-content:space-between;
          color:white; box-shadow:0 20px 55px rgba(16,37,58,.18);
        }
        .login-hero h1 { color:#fff !important; font-size:36px !important; margin:16px 0 8px; }
        .login-hero p { color:#c4d9e2 !important; max-width:390px; line-height:1.7; }
        .login-pill { display:inline-block; padding:7px 12px; border-radius:30px;
          border:1px solid rgba(255,255,255,.22); color:#d9f8f1; font-size:11px; }
        .login-foot { color:#a8c2ce; font-size:11px; }
        div[data-testid="stForm"] { border:1px solid #e5edf2; border-radius:20px;
          padding:26px; background:#fff; box-shadow:0 14px 40px rgba(21,38,59,.06); }
        </style>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown(
            """
            <div class="login-hero">
              <div>
                <span class="login-pill">✚ &nbsp; INTELLIGENT CARE OPERATIONS</span>
                <h1>Clarity for care.<br>Intelligence for teams.</h1>
                <p>One connected workspace for patient information, medical reports,
                clinical guidelines and AI-assisted hospital workflows.</p>
              </div>
              <div class="login-foot">MEGNOVA AI &nbsp; · &nbsp; HOSPITAL DIGITAL TWIN</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.write("")
        st.write("")
        st.markdown('<div class="mn-eyebrow">WELCOME BACK</div>', unsafe_allow_html=True)
        st.markdown("## Sign in to your workspace")
        st.caption("Use your registered account to continue.")
        with st.form("megnova_login_form"):
            email = st.text_input("Email address", placeholder="name@hospital.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign in  →", use_container_width=True, type="primary")
        if submitted:
            if not email.strip() or not password:
                st.warning("Please enter your email and password.")
                return
            try:
                response = login(email.strip(), password)
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    if not token:
                        st.error("Login response did not contain an access token.")
                        return
                    st.session_state["access_token"] = token
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = {"email": email.strip()}
                    st.session_state["user_name"] = email.split("@")[0]
                    st.rerun()
                elif response.status_code in (400, 401, 403):
                    st.error("Invalid email or password.")
                else:
                    st.error(f"Login failed: HTTP {response.status_code}")
            except Exception as error:
                st.error(f"Unable to connect to the backend: {error}")
        st.markdown(
            '<p style="font-size:11px;color:#8a99a7;margin-top:24px;">'
            'Secure access · Clinical decision support workspace</p>',
            unsafe_allow_html=True,
        )
