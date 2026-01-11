import streamlit as st
import requests

st.title("Admin Panel")

users = requests.get("http://localhost:5000/api/auth/users").json()
st.table(users)
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
