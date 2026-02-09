import streamlit as st
import requests

# Note: st.set_page_config is handled by Home.py

# Reset navbar padding for auth pages - FORCE override
st.markdown('''
<style>
    .main .block-container,
    .block-container,
    section.main > div {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }
</style>
''', unsafe_allow_html=True)

# ───────────────── LAYOUT ─────────────────
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.write("")
    st.markdown("<h1 class='header-title'>Create an Account</h1>", unsafe_allow_html=True)
    st.markdown("<p class='header-subtitle'>Join thousands of readers using AI to summarize books.</p>", unsafe_allow_html=True)

    # 🧊 GLASS CARD
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    with st.form("register_form"):
        # Section 1
        st.markdown("### 👤 Account Details")
        c1, c2 = st.columns(2)
        with c1:
             username = st.text_input("Username *", placeholder="e.g. bookworm99")
        with c2:
             email = st.text_input("Email Address *", placeholder="name@example.com")
        
        password = st.text_input("Password *", type="password", placeholder="Create a strong password")

        st.write("")
        st.markdown("### 📝 Profile Info")
        
        c3, c4 = st.columns(2)
        with c3:
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
            age = st.number_input("Age", 18, 100, 25)
            country = st.text_input("Country", placeholder="United States")
        with c4:
            qualification = st.text_input("Qualification", placeholder="e.g. BSc")
            occupation = st.text_input("Occupation", placeholder="e.g. Student")
            role = st.selectbox("Role", ["User", "Admin"])

        st.write("")
        submit = st.form_submit_button("✨ Create Account", use_container_width=True)

    # st.markdown('</div>', unsafe_allow_html=True)

    # ───────────────── LOGIC ─────────────────
    if submit:
        if not username or not email or not password:
             st.error("⚠️ Please fill in all mandatory fields (*)")
        else:
            payload = {
                "username": username,
                "email": email,
                "password": password,
                "gender": gender,
                "age": str(age),
                "qualification": qualification,
                "occupation": occupation,
                "country": country,
                "role": role.lower()
            }
            
            try:
                from utils import register_user
                
                with st.spinner("Creating your account..."):
                    res = register_user(payload)
                
                if res.status_code in [200, 201]:
                    st.toast("✅ Account created successfully!")
                    st.session_state.page = "Login"
                    st.rerun()
                else:
                    error_msg = res.json().get("message", "Registration failed")
                    st.error(f"❌ {error_msg}")

            except Exception as e:
                st.error(f"🔌 Connection error: {str(e)}")

    # ───────────────── FOOTER ACTIONS ─────────────────
    st.write("")
    f1, f2 = st.columns(2)
    with f1:
        if st.button("⬅️ Back to Home", use_container_width=True, key="reg_home"):
            st.session_state.page = "Home"
            st.rerun()
    with f2:
         if st.button("🔑 Log in", use_container_width=True, key="reg_login"):
            st.session_state.page = "Login"
            st.rerun()

