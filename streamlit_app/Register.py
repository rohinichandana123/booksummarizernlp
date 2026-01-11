import streamlit as st
import requests

st.title("📝 Register")

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", 18, 100)
    qualification = st.text_input("Qualification")
    occupation = st.text_input("Occupation")
    country = st.text_input("Country")

    submitted = st.form_submit_button("Register")

if submitted:
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "gender": gender,
        "age": age,
        "qualification": qualification,
        "occupation": occupation,
        "country": country
    }

    try:
        res = requests.post(
            "http://localhost:5000/api/auth/register",
            json=payload
        )

        if res.status_code == 200:
            st.success("Registration successful!")
            st.session_state.page = "Login"
        else:
            st.error(res.text)

    except Exception as e:
        st.error("Backend not reachable")
