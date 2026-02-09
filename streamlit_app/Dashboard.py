import streamlit as st
import requests
import pandas as pd
import os
from utils_ui import card, section_header, load_css
from utils import list_books, API_BASE

# ✅ PREVENT DUPLICATE AVATAR BUTTON
# if "profile_rendered" not in st.session_state:
#     render_google_profile()
#     st.session_state.profile_rendered = True

# Reset padding that might be set by Home page's navbar
# st.markdown(
#     '<style>.block-container { padding-top: 2rem !important; }</style>',
#     unsafe_allow_html=True
# )

# ───────────────── AUTH CHECK ─────────────────
if "user_id" not in st.session_state:
    st.warning("Please login first.")
    st.session_state.page = "Login"
    st.rerun()
    st.stop()  # CRITICAL: Stop Dashboard rendering

# ───────────────── DEFAULT NAV STATE ─────────────────
if "nav" not in st.session_state:
    st.session_state.nav = "Overview"

# ───────────────── TOP NAV CSS (FINAL FIX) ─────────────────
st.markdown("""
<style>
/* =========================================================
   TOP NAV BUTTONS — HEIGHT LOCK + NO WRAP (FINAL)
   ========================================================= */

div[data-testid="column"] button {
    height: 64px !important;
    min-height: 64px !important;
    max-height: 64px !important;

    width: 100% !important;
    padding: 6px 8px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-sizing: border-box !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    text-overflow: ellipsis !important;

    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    line-height: 1 !important;
    transition: all 0.2s ease !important;
}

/* 🚨 Critical fix: prevent flex wrapping */
div[data-testid="column"] button > div {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Text container */
div[data-testid="column"] button span {
    display: block !important;
    max-width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

/* Secondary (inactive) */
div[data-testid="column"] button[kind="secondary"] {
    background: white !important;
    color: #374151 !important;
    border: 1px solid #e5e7eb !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

/* Primary (active) */
div[data-testid="column"] button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3) !important;
}

/* Hover states */
div[data-testid="column"] button[kind="secondary"]:hover {
    background: #f9fafb !important;
    border-color: #6366F1 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.2) !important;
}

div[data-testid="column"] button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(99,102,241,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

nav_options = {
    "Overview": "📊",
    "Upload": "📤",
    "Summarize": "✨",
    "My Books": "📚",
    "History": "📜",
    "Profile": "👤"
}

# Navigation buttons (full width, no logout button)
nav_cols = st.columns(len(nav_options), gap="small")
for col, (option, icon) in zip(nav_cols, nav_options.items()):
    btn_type = "primary" if st.session_state.nav == option else "secondary"
    with col:
        if st.button(
            f"{icon} {option}",
            key=f"topnav_{option}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.nav = option
            st.rerun()

# ───────────────── ROUTING VIEW ─────────────────
if st.session_state.nav == "Overview":

    col1, col2, col3 = st.columns(3)

    try:
        res = list_books(st.session_state.user_id)
        books = res.json() if res.status_code == 200 else []
        total_books = len(books)

        logs_res = requests.get(
            f"{API_BASE}/auth/logs/{st.session_state.user_id}"
        )
        logs = logs_res.json() if logs_res.status_code == 200 else []

        # Count summaries based on action string (case-insensitive match)
        total_summaries = sum(
            1 for log in logs
            if "summary" in log.get("action", "").lower()
        )

        # Calculate Reading Time Saved
        # Avg reading speed = 250 wpm
        total_book_words = sum(b.get("word_count", 0) for b in books)
        total_summary_words = sum(b.get("summary_word_count", 0) for b in books)
        
        # Time in minutes
        time_saved_minutes = (total_book_words - total_summary_words) / 250
        time_saved_hours = max(0, round(time_saved_minutes / 60, 1))
        
        # Format: 1.5h or 2h
        if time_saved_hours.is_integer():
            time_saved_str = f"{int(time_saved_hours)}h"
        else:
            time_saved_str = f"{time_saved_hours}h"

    except Exception:
        total_books = 0
        total_summaries = 0
        time_saved_str = "0h"

    with col1:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #6366F1;">
            <h3 style="margin:0;font-size:2.5rem;color:#6366F1;">{total_books}</h3>
            <p style="margin:0;color:gray;">Books Uploaded</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #8B5CF6;">
            <h3 style="margin:0;font-size:2.5rem;color:#8B5CF6;">{total_summaries}</h3>
            <p style="margin:0;color:gray;">Summaries Generated</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #10B981;">
            <h3 style="margin:0;font-size:2.5rem;color:#10B981;">{time_saved_str}</h3>
            <p style="margin:0;color:gray;">Reading Time Saved</p>
        </div>
        """, unsafe_allow_html=True)

    # ───────── QUICK ACTIONS ─────────
    st.markdown("## ⚡ Quick Actions")
    qa1, qa2, qa3 = st.columns(3)

    with qa1:
        if st.button("📤 Upload a Book", use_container_width=True):
            st.session_state.nav = "Upload"
            st.rerun()

    with qa2:
        if st.button("✨ Summarize a Book", use_container_width=True):
            st.session_state.nav = "Summarize"
            st.rerun()

    with qa3:
        if st.button("📚 My Books", use_container_width=True):
            st.session_state.nav = "My Books"
            st.rerun()

    # ───────── HOW IT WORKS ─────────
    st.markdown("## 🪜 How It Works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <h2>🔐</h2>
            <h4>Step 1</h4>
            <p><b>Login</b></p>
            <p style="color:gray;">
                Securely sign in to access your personalized AI dashboard.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with step2:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <h2>📤</h2>
            <h4>Step 2</h4>
            <p><b>Upload Book</b></p>
            <p style="color:gray;">
                Upload your PDF or document in just one click.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with step3:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <h2>✨</h2>
            <h4>Step 3</h4>
            <p><b>Generate Summary</b></p>
            <p style="color:gray;">
                Click generate and get AI-powered summaries instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ───────── RECENT ACTIVITY ─────────
    st.markdown("## 🕒 Recent Activity")

    if logs:
        # Show top 5 recent activities
        for log in logs[:5]:
            action = log.get("action", "").replace("_", " ").title()
            # Parse timestamp if needed, or just show action for now to keep it simple/fast
            # (Profile.py has complex datetime parsing, we can do simpler here or copy it)
            
            timestamp = log.get("created_at", "")
            if timestamp:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%b %d, %H:%M")
                except:
                    time_str = ""
            else:
                time_str = ""

            icon = "📤" if "UPLOAD" in action.upper() else "✨" if "SUMMARY" in action.upper() else "🔹"

            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 10px 0; border-bottom: 1px solid #eee;">
                <div>
                    <span style="font-size:1.2rem; margin-right:10px;">{icon}</span>
                    <span style="font-weight:500; color:#374151;">{action}</span>
                </div>
                <div style="font-size:0.85rem; color:#9ca3af;">{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:15px; text-align:center;'><a href='#' onclick='document.getElementById(\"topnav_History\").click(); return false;' style='color:#6366f1; text-decoration:none; font-weight:600; font-size:0.9rem;'>View Full History</a></div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <p style="color:gray; text-align:center; padding: 20px;">No recent activity yet.</p>
        <p style="text-align:center;">Upload a book to get started.</p>
        """, unsafe_allow_html=True)


elif st.session_state.nav == "Upload":
    exec(open(os.path.join(os.path.dirname(__file__), "Upload_Book.py"), encoding="utf-8").read())

elif st.session_state.nav == "Summarize":
    exec(open(os.path.join(os.path.dirname(__file__), "Summarize.py"), encoding="utf-8").read())

elif st.session_state.nav == "My Books":
    exec(open(os.path.join(os.path.dirname(__file__), "View_Books.py"), encoding="utf-8").read())

elif st.session_state.nav == "History":
    res = requests.get(f"{API_BASE}/auth/logs/{st.session_state.user_id}")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        st.dataframe(df, use_container_width=True)

elif st.session_state.nav == "Profile":
    exec(open(os.path.join(os.path.dirname(__file__), "Profile.py"), encoding="utf-8").read())

