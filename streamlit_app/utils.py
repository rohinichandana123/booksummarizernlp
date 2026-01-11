import requests

API_BASE = "http://127.0.0.1:5000/api"

def login_user(email, password):
    return requests.post(
        f"{API_BASE}/auth/login",
        json={"email": email, "password": password}
    )

def register_user(username, email, password, gender, age, qualification):
    return requests.post(
        f"{API_BASE}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "gender": gender,
            "age": age,
            "qualification": qualification
        }
    )

