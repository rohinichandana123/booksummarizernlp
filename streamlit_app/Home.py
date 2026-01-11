import streamlit as st

st.set_page_config(page_title="Book Summarizer")

# 🔒 VERY IMPORTANT
if "page" not in st.session_state:
    st.session_state.page = "Register"

st.sidebar.title("Navigation")

if st.sidebar.button("Register"):
    st.session_state.page = "Register"

if st.sidebar.button("Login"):
    st.session_state.page = "Login"

st.write("🔄 Current Page:", st.session_state.page)

# Routing
if st.session_state.page == "Register":
    import Register
elif st.session_state.page == "Login":
    import Login
elif st.session_state.page == "Dashboard":
    import Dashboard
elif st.session_state.page == "Admin":
    import Admin
