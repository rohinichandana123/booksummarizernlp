import streamlit as st
import os

import streamlit.components.v1 as components

# ---------------- LOAD CSS ---------------- #

def load_css(file_path="assets/style.css"):
    path = os.path.join(os.path.dirname(__file__), file_path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass


# ---------------- INIT PAGE ---------------- #

def init_page(page_title="AI Book Summarizer", layout="wide"):

    try:
        st.set_page_config(
            page_title=page_title,
            page_icon="📚",
            layout=layout,
            initial_sidebar_state="collapsed"
        )
    except Exception:
        pass

    load_css()

    # 🔥 GLOBAL PREMIUM BACKGROUND
    st.markdown("""
    <style>

    .stApp{
        background: linear-gradient(
            180deg,
            #f8fbff 0%,
            #eef2ff 45%,
            #ffffff 100%
        );
    }

    header[data-testid="stHeader"]{
        background: transparent;
    }

    [data-testid="collapsedControl"]{
        display:none;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------- NAVBAR ---------------- #

def render_navbar():

    logged_in = "user_id" in st.session_state

    nav_html = f"""
    <div class="custom-navbar">
        <div class="nav-brand">
            📚 <span class="brand-text">AI Book Summarizer</span>
        </div>

        <div style="display:flex;gap:1rem;align-items:center;">
            {'<a href="?nav=login" target="_self" style="text-decoration:none;"><div class="nav-btn">Login</div></a>' if not logged_in else ''}
        </div>
    </div>
    """

    st.markdown(nav_html, unsafe_allow_html=True)

    st.markdown(
        '<style>.block-container { padding-top: 5rem !important; }</style>',
        unsafe_allow_html=True
    )


# ---------------- CARD ---------------- #
import streamlit.components.v1 as components

def card(
    title,
    content,
    link="#",
    gradient="blue",
   svg_icon="🤖"
):

    gradients = {
        "blue": "linear-gradient(135deg, #e0e7ff, #f8fbff)",
        "green": "linear-gradient(135deg, #dcfce7, #f0fdf4)",
        "purple": "linear-gradient(135deg, #ede9fe, #faf5ff)",
        "orange": "linear-gradient(135deg, #ffedd5, #fff7ed)",
        "pink": "linear-gradient(135deg, #fce7f3, #fff1f2)",
        "teal": "linear-gradient(135deg, #ccfbf1, #f0fdfa)",
    }

    bg = gradients.get(gradient, gradients["blue"])

    components.html(
        f"""
        <style>
        /* FIX STREAMLIT CLIPPING */
        div[data-testid="column"] {{
            overflow: visible !important;
        }}

        .card-wrapper {{
            perspective: 1200px;
        }}

        .saas-card {{
            height: 260px;
            border-radius: 24px;
            padding: 1.6rem;

            background: {bg};
            border: 1px solid rgba(255,255,255,0.6);

            box-shadow:
                0 18px 40px rgba(0,0,0,0.08),
                inset 0 1px 0 rgba(255,255,255,0.8);

            display: flex;
            flex-direction: column;
            justify-content: space-between;

            transition: all 0.35s ease;
            cursor: pointer;

            opacity: 0;
            transform: translateY(30px) scale(0.97);
        }}

        .saas-card.visible {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}

        .saas-card:hover {{
            transform: translateY(-10px) scale(1.02);
            border: 1px solid #6366f1;
            box-shadow:
                0 35px 80px rgba(99,102,241,0.35);
        }}

        .icon-box {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }}

        .saas-card h3 {{
            font-size: 1.15rem;
            font-weight: 700;
            margin: 1rem 0 0.4rem;
        }}

        .saas-card p {{
            font-size: 0.9rem;
            color: #6b7280;
            line-height: 1.5;
        }}

        /* DARK MODE */
        @media (prefers-color-scheme: dark) {{
            .saas-card {{
                background: linear-gradient(135deg, #1f2933, #111827);
                border: 1px solid rgba(255,255,255,0.1);
            }}

            .saas-card p {{
                color: #d1d5db;
            }}

            .icon-box {{
                background: #111827;
                color: white;
            }}
        }}
        </style>

        <div class="card-wrapper">
            <div class="saas-card" onclick="window.location='{link}'">
                <div>
                    <div class="icon-box">{svg_icon}</div>
                    <h3>{title}</h3>
                    <p>{content}</p>
                </div>
            </div>
        </div>

        <script>
        const cards = document.querySelectorAll('.saas-card');

        const observer = new IntersectionObserver(entries => {{
            entries.forEach(entry => {{
                if(entry.isIntersecting){{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, {{ threshold: 0.2 }});

        cards.forEach(card => observer.observe(card));
        </script>
        """,
        height=280
    )

# ---------------- SECTION HEADER ---------------- #

def section_header(title, subtitle=None):

    subtitle_html = f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:3rem;margin-top:2rem;">
        <h2 class="header-title" style="font-size:2.2rem;">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


# ---------------- GOOGLE STYLE PROFILE ---------------- #

def render_google_profile():

    if "show_profile" not in st.session_state:
        st.session_state.show_profile = False

    name = st.session_state.get("name", "User")
    email = st.session_state.get("email", "user@email.com")
    role = st.session_state.get("role", "user")

    initial = name[0].upper()

    # ---------- CSS ---------- #

    st.markdown(f"""
    <style>

    .avatar-btn {{
        position: fixed;
        top: 18px;
        right: 25px;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: #5b5ce2;
        color: white;
        font-weight: 600;
        display:flex;
        align-items:center;
        justify-content:center;
        cursor:pointer;
        z-index:9999;
        box-shadow:0 6px 18px rgba(0,0,0,0.18);
    }}

    .profile-card {{
        position: fixed;
        top: 75px;
        right: 25px;
        width: 330px;
        border-radius: 20px;
        background: white;
        box-shadow:0 25px 70px rgba(0,0,0,0.2);
        overflow:hidden;
        z-index:9998;
        animation:fade .15s ease-in-out;
    }}

    @keyframes fade {{
        from{{opacity:0;transform:translateY(-8px)}}
        to{{opacity:1}}
    }}

    .profile-top {{
        background:#eef2ff;
        padding:28px;
        text-align:center;
    }}

    .avatar-big {{
        width:82px;
        height:82px;
        border-radius:50%;
        background:#5b5ce2;
        color:white;
        font-size:34px;
        font-weight:600;
        display:flex;
        align-items:center;
        justify-content:center;
        margin:auto;
        margin-bottom:12px;
    }}

    .menu-item {{
        padding:16px 22px;
        font-size:15px;
        cursor:pointer;
        display:flex;
        gap:12px;
        align-items:center;
    }}

    .menu-item:hover {{
        background:#f6f8ff;
    }}

    .logout-btn button {{
        width:90%;
        margin:12px;
        border-radius:10px;
        height:42px;
        background:#5b5ce2;
        color:white;
        border:none;
    }}

    </style>
    """, unsafe_allow_html=True)

    # ---------- AVATAR CLICK ---------- #

    col1, col2 = st.columns([20,1])

    with col2:
        if st.button(initial, key=f"avatar_top_{st.session_state.get('page','home')}"):
            st.session_state.show_profile = not st.session_state.show_profile

    # ---------- PROFILE DROPDOWN ---------- #

    if st.session_state.show_profile:

        st.markdown(f"""
        <div class="profile-card">

            <div class="profile-top">
                <div class="avatar-big">{initial}</div>

                <div style="font-weight:600;font-size:18px;">
                    {name}
                </div>

                <div style="color:gray;font-size:14px;">
                    {email}
                </div>

                <div style="color:#5b5ce2;font-size:13px;margin-top:4px;">
                    {role.upper()}
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)
        
        # Interactive menu items
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("👤 My Profile", key="goto_profile", use_container_width=True):
                st.session_state.nav = "Profile"
                st.session_state.show_profile = False
                st.rerun()
        
        with col2:
            if st.button("🚪 Logout", key="profile_logout", use_container_width=True):
                st.session_state.clear()
                st.session_state.page = "Home"
                st.rerun()

      