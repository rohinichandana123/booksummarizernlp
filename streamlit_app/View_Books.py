import streamlit as st
import requests

if "user_id" not in st.session_state:
    st.warning("Login required")
    st.stop()

st.title("My Books")

user_id = st.session_state["user_id"]
r = requests.get(f"http://127.0.0.1:5000/api/books/list/{user_id}")

books = r.json()
for b in books:
    st.write(f"📘 **{b['title']}** by {b['author']}")

if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()

