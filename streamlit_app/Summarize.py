import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/api/summary/generate"

st.title("📚 Book Summarizer")
st.write("Upload a book or paste text to generate a summary.")

# Text Input
input_text = st.text_area("Enter text to summarize:", height=200)

# File Upload
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

summary = ""

if st.button("Generate Summary"):
    if input_text.strip() == "" and uploaded_file is None:
        st.error("Please enter text or upload a PDF file.")
    else:
        payload = {"text": input_text}

        # If file uploaded, send file to API
        if uploaded_file:
            files = {"pdf": uploaded_file.getvalue()}
            response = requests.post(API_URL, files=files)
        else:
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            summary = result["summary"]
            st.success("Summary generated successfully!")
        else:
            st.error("Error from API: " + response.text)

# Show output
if summary:
    st.subheader("📘 Summary")
    st.write(summary)
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
