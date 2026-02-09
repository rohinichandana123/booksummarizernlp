import streamlit as st
import requests

# =========================================================
# 🔒 HARD AUTH GUARD — MUST BE FIRST (NO UI ABOVE THIS)
# =========================================================
if st.session_state.get("user_id"):
    st.session_state.page = "Dashboard"
    st.rerun()
    st.stop()

# Note: st.set_page_config is handled by Home.py

# Reset navbar padding for auth pages
st.markdown("""
<style>
    .main .block-container,
    .block-container,
    section.main > div {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ───────────────── LAYOUT ─────────────────
col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    st.markdown("<h1 class='header-title'>Welcome Back</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='header-subtitle'>Enter your credentials to access your account.</p>",
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="name@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submit = st.form_submit_button("🚀 Sign In", use_container_width=True)

    # ───────────────── LOGIN HANDLER ─────────────────
    if submit:
        if not email or not password:
            st.error("⚠️ Please fill in all fields")
        else:
            try:
                from utils import login_user

                with st.spinner("Authenticating..."):
                    response = login_user(email, password)

                if response.status_code == 200:
                    data = response.json()

                    # ✅ SET STATE FIRST
                    st.session_state["user_id"] = data["user_id"]
                    st.session_state["username"] = data["username"]
                    st.session_state["role"] = data["role"]

                    # ✅ ROUTE
                    st.session_state.page = "Dashboard"
                    st.session_state.nav = "Overview"

                    # ✅ HARD EXIT
                    st.rerun()
                    st.stop()

                else:
                    st.error(response.json().get("error", "Login failed"))

            except Exception as e:
                st.error(f"🔌 Connection error: {str(e)}")

    # ───────────────── FOOTER ACTIONS ─────────────────
    c1, c2 = st.columns(2)

    with c1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
            st.stop()

    with c2:
        if st.button("✨ Create Account", use_container_width=True):
            st.session_state.page = "Register"
            st.rerun()
            st.stop()
