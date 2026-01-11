import streamlit as st
import requests

if "user_id" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.title("Upload Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
content = st.text_area("Paste Text Here")

if st.button("Upload"):
    r = requests.post(
        "http://127.0.0.1:5000/api/books/upload",
        json={
            "title": title,
            "author": author,
            "content": content,
            "user_id": st.session_state["user_id"]
        }
    )
    st.success("Book uploaded!")
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
