import streamlit as st
import requests

st.title("🔑 Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    try:
        res = requests.post(
            "http://localhost:5000/api/auth/login",
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.user_id = data["user_id"]
            st.session_state.role = data["role"]

            st.session_state.page = (
                "Admin" if data["role"] == "admin" else "Dashboard"
            )
        else:
            st.error("Invalid credentials")

    except:
        st.error("Backend not reachable")
