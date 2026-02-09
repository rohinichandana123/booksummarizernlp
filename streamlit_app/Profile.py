import streamlit as st
import requests
from utils import API_BASE

# Reset padding
st.markdown(
    '<style>.block-container { padding-top: 2rem !important; }</style>',
    unsafe_allow_html=True
)

# ───────────────── AUTH CHECK ─────────────────
if "user_id" not in st.session_state:
    st.warning("Please login first.")
    st.session_state.page = "Login"
    st.rerun()

# ───────────────── PROFILE STYLES ─────────────────
st.markdown("""
<style>
.profile-header {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
}

.profile-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: white;
    color: #6366F1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: bold;
    margin: 0 auto 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.profile-name {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.profile-email {
    font-size: 1rem;
    opacity: 0.9;
    margin-bottom: 0.3rem;
}

.profile-role {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 0.5rem;
}

.info-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 1.5rem;
    border-left: 4px solid #6366F1;
}

.info-label {
    font-size: 0.85rem;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
}

.info-value {
    font-size: 1.1rem;
    color: #1f2937;
    font-weight: 500;
}

.stat-box {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #bae6fd;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0284c7;
    margin-bottom: 0.3rem;
}

.stat-label {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ───────────────── FETCH USER DATA ─────────────────
try:
    response = requests.get(f"{API_BASE}/auth/user/{st.session_state.user_id}")
    if response.status_code == 200:
        user_data = response.json()
    else:
        st.error("Failed to load user profile")
        user_data = {}
except Exception as e:
    st.error(f"Error loading profile: {str(e)}")
    user_data = {}

# Fallback to session state if API fails
username = user_data.get("username", st.session_state.get("username", "User"))
email = user_data.get("email", st.session_state.get("email", "user@example.com"))
role = user_data.get("role", st.session_state.get("role", "user"))
gender = user_data.get("gender", "Not specified")
age = user_data.get("age", "Not specified")
qualification = user_data.get("qualification", "Not specified")
occupation = user_data.get("occupation", "Not specified")
country = user_data.get("country", "Not specified")
created_at = user_data.get("created_at", "Unknown")

# Get initial for avatar
initial = username[0].upper() if username else "U"

# ───────────────── PROFILE HEADER ─────────────────
st.markdown(f"""
<div class="profile-header">
    <div class="profile-avatar">{initial}</div>
    <div class="profile-name">{username}</div>
    <div class="profile-email">{email}</div>
    <div class="profile-role">🎯 {role.upper()}</div>
</div>
""", unsafe_allow_html=True)

# ───────────────── TABS ─────────────────
tab1, tab2, tab3 = st.tabs(["📋 Personal Information", "📊 Statistics", "⚙️ Settings"])

# ───────────────── TAB 1: PERSONAL INFO ─────────────────
with tab1:
    st.markdown("### 👤 Personal Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Username</div>
            <div class="info-value">{username}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Gender</div>
            <div class="info-value">{gender}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Qualification</div>
            <div class="info-value">{qualification}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Country</div>
            <div class="info-value">{country}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Email</div>
            <div class="info-value">{email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Age</div>
            <div class="info-value">{age}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Occupation</div>
            <div class="info-value">{occupation}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">Member Since</div>
            <div class="info-value">{created_at[:10] if created_at != "Unknown" else "Unknown"}</div>
        </div>
        """, unsafe_allow_html=True)

# ───────────────── TAB 2: STATISTICS ─────────────────
with tab2:
    st.markdown("### 📈 Your Activity")
    
    # Fetch user statistics
    # Fetch user statistics
    try:
        # Get books count (Fixed Endpoint)
        books_res = requests.get(f"{API_BASE}/books/list/{st.session_state.user_id}")
        books = books_res.json() if books_res.status_code == 200 else []
        total_books = len(books)
        
        # Get logs
        logs_res = requests.get(f"{API_BASE}/auth/logs/{st.session_state.user_id}")
        logs = logs_res.json() if logs_res.status_code == 200 else []
        
        # Count summaries based on action string (case-insensitive match)
        total_summaries = sum(
            1 for log in logs
            if "summary" in log.get("action", "").lower()
        )
        
        # Calculate Reading Time Saved (Real Calculation)
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box" style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-color: #bae6fd;">
            <div class="stat-number" style="color: #0284c7;">{total_books}</div>
            <div class="stat-label">📚 Books Uploaded</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box" style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-color: #bbf7d0;">
            <div class="stat-number" style="color: #16a34a;">{total_summaries}</div>
            <div class="stat-label">✨ Summaries Generated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box" style="background: linear-gradient(135deg, #fef3c7, #fde68a); border-color: #fcd34d;">
            <div class="stat-number" style="color: #d97706;">{time_saved_str}</div>
            <div class="stat-label">⏱️ Time Saved</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### 📜 Recent Activity")
    
    if logs:
        # Display recent 10 logs
        recent_logs = logs[:10]
        for log in recent_logs:
            action = log.get("action", "Unknown")
            timestamp = log.get("created_at", "Unknown")
            
            # Format timestamp
            if timestamp != "Unknown":
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.strftime("%B %d, %Y at %I:%M %p")
                except:
                    pass
            
            # Icon based on action
            icon = "📤" if "UPLOAD" in action else "✨" if "SUMMARY" in action else "📋"
            
            st.markdown(f"""
            <div class="info-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                        <span style="font-weight: 600; color: #1f2937;">{action.replace('_', ' ').title()}</span>
                    </div>
                    <div style="color: #6b7280; font-size: 0.85rem;">{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No activity yet. Start by uploading a book!")

# ───────────────── TAB 3: SETTINGS ─────────────────
with tab3:
    st.markdown("### ⚙️ Account Settings")
    
    st.markdown("#### ✏️ Edit Profile")
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username", value=username)
            new_gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                     index=["Male", "Female", "Other", "Prefer not to say"].index(gender) if gender in ["Male", "Female", "Other", "Prefer not to say"] else 0)
            new_qualification = st.text_input("Qualification", value=qualification if qualification != "Not specified" else "")
        
        with col2:
            new_age = st.number_input("Age", min_value=1, max_value=120, value=int(age) if str(age).isdigit() else 25)
            new_occupation = st.text_input("Occupation", value=occupation if occupation != "Not specified" else "")
            new_country = st.text_input("Country", value=country if country != "Not specified" else "")
        
        submit_profile = st.form_submit_button("💾 Save Changes", use_container_width=True)
    
    if submit_profile:
        try:
            update_data = {
                "username": new_username,
                "gender": new_gender,
                "age": new_age,
                "qualification": new_qualification,
                "occupation": new_occupation,
                "country": new_country
            }
            
            response = requests.put(
                f"{API_BASE}/auth/user/{st.session_state.user_id}",
                json=update_data
            )
            
            if response.status_code == 200:
                st.toast("Profile Updated!", icon="✅")
                st.session_state.username = new_username
                st.rerun()
            else:
                st.error(f"Failed to update profile: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error updating profile: {str(e)}")
    
    st.markdown("---")
    st.markdown("#### 🔒 Change Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submit_password = st.form_submit_button("🔐 Update Password", use_container_width=True)
    
    if submit_password:
        if not current_password or not new_password or not confirm_password:
            st.error("Please fill in all password fields")
        elif new_password != confirm_password:
            st.error("New passwords do not match")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            try:
                response = requests.put(
                    f"{API_BASE}/auth/user/{st.session_state.user_id}/password",
                    json={
                        "current_password": current_password,
                        "new_password": new_password
                    }
                )
                
                if response.status_code == 200:
                    st.success("✅ Password updated successfully!")
                else:
                    st.error(f"Failed to update password: {response.json().get('error', 'Invalid current password')}")
            except Exception as e:
                st.error(f"Error updating password: {str(e)}")
    
    st.markdown("---")
    st.markdown("#### 🗑️ Danger Zone")
    
    with st.expander("⚠️ Delete Account", expanded=False):
        st.warning("This action cannot be undone. All your data will be permanently deleted.")
        
        if st.button("🗑️ Delete My Account", type="secondary"):
            st.session_state.confirm_delete = True
        
        if st.session_state.get("confirm_delete", False):
            st.error("Are you absolutely sure? Type 'DELETE' to confirm:")
            confirm_text = st.text_input("Confirmation", key="delete_confirm")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_delete = False
                    st.rerun()
            
            with col2:
                if st.button("Confirm Delete", type="primary", use_container_width=True):
                    if confirm_text == "DELETE":
                        try:
                            response = requests.delete(f"{API_BASE}/auth/user/{st.session_state.user_id}")
                            if response.status_code == 200:
                                st.success("Account deleted successfully")
                                st.session_state.clear()
                                st.session_state.page = "Home"
                                st.rerun()
                            else:
                                st.error("Failed to delete account")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.error("Please type 'DELETE' to confirm")
    
    # Logout button at the bottom
    st.markdown("---")
    st.markdown("#### 🚪 Session")
    if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_btn"):
        st.session_state.clear()
        st.session_state.page = "Home"
        st.rerun()

# ───────────────── BACK BUTTON ─────────────────
st.write("")
st.write("")
if st.button("⬅️ Back to Dashboard", use_container_width=True):
    st.session_state.page = "Dashboard"
    st.rerun()
