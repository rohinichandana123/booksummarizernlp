import requests

API_BASE = "http://127.0.0.1:5000/api"

# ✅ Timeout settings (in seconds)
DEFAULT_TIMEOUT = 30
SUMMARY_TIMEOUT = 180  # 3 minutes for summarization

def login_user(email, password):
    return requests.post(
        f"{API_BASE}/auth/login",
        json={"email": email, "password": password},
        timeout=DEFAULT_TIMEOUT
    )

def register_user(payload):
    return requests.post(
        f"{API_BASE}/auth/register",
        json=payload,
        timeout=DEFAULT_TIMEOUT
    )

def list_books(user_id):
    return requests.get(f"{API_BASE}/books/list/{user_id}", timeout=DEFAULT_TIMEOUT)

def get_book_details(book_id):
    return requests.get(f"{API_BASE}/books/detail/{book_id}", timeout=DEFAULT_TIMEOUT)

def upload_book_text(data):
    return requests.post(f"{API_BASE}/books/upload", json=data, timeout=DEFAULT_TIMEOUT)

def upload_book_pdf(files, data):
    return requests.post(f"{API_BASE}/books/upload-pdf", files=files, data=data, timeout=60)

# ✅ Longer timeout for summary generation
def generate_summary(payload):
    return requests.post(
        f"{API_BASE}/summary/generate",
        json=payload,
        timeout=SUMMARY_TIMEOUT  # 3 minutes
    )

def generate_summary_from_file(files):
    return requests.post(
        f"{API_BASE}/summary/generate",
        files=files,
        timeout=SUMMARY_TIMEOUT  # 3 minutes
    )

def delete_book(book_id):
    return requests.delete(f"{API_BASE}/books/delete/{book_id}", timeout=DEFAULT_TIMEOUT)

def get_all_users():
    return requests.get(f"{API_BASE}/admin/users", timeout=DEFAULT_TIMEOUT)

def get_all_books():
    return requests.get(f"{API_BASE}/admin/books", timeout=DEFAULT_TIMEOUT)
from gtts import gTTS
import tempfile
import streamlit as st


@st.cache_data(show_spinner=False)
def generate_audio(summary_text):
    tts = gTTS(text=summary_text, lang="en")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return temp_file.name
