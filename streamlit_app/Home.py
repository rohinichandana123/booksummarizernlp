import streamlit as st
import os
from utils_ui import init_page, section_header, card  # ❌ removed render_navbar

# ───────────────── ROUTING LOGIC ─────────────────
if st.query_params.get("nav") == "login":
    st.session_state.page = "Login"
    st.query_params.clear()

if "page" not in st.session_state:
    st.session_state.page = "Home"

# Redirect logic (FIXED — prevents admin loop)
if "user_id" in st.session_state:
    # Redirect ONLY if user is on Home/Login
    if st.session_state.page in ["Home", "Login"]:
        if st.session_state.get("role") == "admin":
            st.session_state.page = "Admin"
        else:
            st.session_state.page = "Dashboard"

# ───────────────── PAGE SETUP ─────────────────
init_page(page_title="AI Book Summarizer")

# ───────────────── HELPER FOR ROUTING ─────────────────
def run_page(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r", encoding="utf-8") as f:
        code = compile(f.read(), path, "exec")
        exec(code, globals())

# ───────────────── VIEW CONTROLLER ─────────────────
if st.session_state.page == "Home":

    # ─── HERO SECTION ───
    st.markdown(
        """
        <div style="text-align: center; padding: 6rem 1rem 4rem;">
            <h1 style="font-size: 3.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 1.5rem;">
                Unlock the Knowledge<br>
                <span style="background: linear-gradient(135deg, var(--primary), var(--secondary));
                             -webkit-background-clip: text;
                             -webkit-text-fill-color: transparent;">
                    Hidden in Your Books
                </span>
            </h1>
            <p style="font-size: 1.25rem; color: var(--text-body);
                      max-width: 600px; margin: 0 auto 3rem;">
                Stop skimming. Start understanding. Our AI-powered platform summarizes
                entire books into key insights, chapter breakdowns, and actionable
                takeaways in seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── ACTION BUTTON ───
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.session_state.page = "Login"
            st.rerun()

    # ─── TRUST BADGE ───
    st.markdown(
        """
        <div style="text-align: center; margin-top: 4rem; margin-bottom: 6rem; opacity: 0.7;">
            <p style="font-size: 0.875rem; text-transform: uppercase;
                      letter-spacing: 0.05em; font-weight: 600; margin-bottom: 1rem;">
                Trusted by readers from top universities
            </p>
            <div style="display: flex; justify-content: center; gap: 3rem;
                        font-weight: 700; color: var(--text-muted); font-size: 1.2rem;">
                <span>Stanford</span>
                <span>MIT</span>
                <span>Harvard</span>
                <span>Oxford</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─── FEATURES ───
    section_header(
        title="Everything you need to learn faster",
    )

    r1_col1, r1_col2, r1_col3 = st.columns(3, gap="large")
    st.write("")
    st.write("")
    r2_col1, r2_col2, r2_col3 = st.columns(3, gap="large")

    with r1_col1:
        card(
            "⚡ Instant Summaries",
            "Upload PDFs and get comprehensive summaries in seconds, not hours.",
        )

    with r1_col2:
        card(
            "📖 Chapter Breakdowns",
            "Don't miss the details. Get summaries for every single chapter.",
        )

    with r1_col3:
        card(
            "💬 AI Q&A",
            "Chat with your book. Ask specific questions and get answers cited from the text.",
        )

    with r2_col1:
        card(
            "🧠 Concept Extraction",
            "Automatically identify and define key concepts and terminology.",
        )

    with r2_col2:
        card(
            "📂 Smart Library",
            "Organize all your summaries in one meaningful, searchable knowledge base.",
        )

    with r2_col3:
        card(
            "📢 Audio Summaries",
            "Listen to your summaries on the go with our realistic text-to-speech engine.",
        )

    # ─── HOW IT WORKS ───
    section_header(
        title="How it works",
        subtitle="Start summarizing books in just 3 simple steps",
    )

    step1, step2, step3 = st.columns(3, gap="large")

    with step1:
        st.markdown(
            """
            <div class="glass-card feature-card" style="text-align:center;">
                <div style="font-size:2.5rem;">🔐</div>
                <h3>Step 1</h3>
                <p><b>Login</b></p>
                <p style="color:gray;">
                    Sign in securely to access your personal AI dashboard.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
            <div class="glass-card feature-card" style="text-align:center;">
                <div style="font-size:2.5rem;">📤</div>
                <h3>Step 2</h3>
                <p><b>Upload Book</b></p>
                <p style="color:gray;">
                    Upload your PDF or document with one click.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="glass-card feature-card" style="text-align:center;">
                <div style="font-size:2.5rem;">✨</div>
                <h3>Step 3</h3>
                <p><b>Generate Summary</b></p>
                <p style="color:gray;">
                    Click generate and get AI-powered summaries instantly.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ─── FOOTER ───
    st.markdown(
        """
        <div style="border-top: 1px solid var(--border-color);
                    margin-top: 6rem; padding-top: 2rem;
                    text-align: center; color: var(--text-muted);
                    font-size: 0.875rem;">
            &copy; 2026 AI Book Summarizer. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ───────────────── ROUTES ─────────────────
elif st.session_state.page == "Register":
    run_page("Register.py")

elif st.session_state.page == "Login":
    run_page("Login.py")

elif st.session_state.page == "Dashboard":
    run_page("Dashboard.py")

elif st.session_state.page == "Admin":
    run_page("Admin.py")
