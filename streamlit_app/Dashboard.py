import streamlit as st
import requests

st.title("User Dashboard")

if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()

text = st.text_area("Paste Book Text")

if st.button("Summarize"):
    summary = requests.post(
        "http://localhost:5000/api/summary/generate",
        json={"text": text}
    ).json()["summary"]

    st.write(summary)
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
