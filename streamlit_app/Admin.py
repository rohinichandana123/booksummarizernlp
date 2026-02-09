import streamlit as st
import requests
from datetime import datetime
from utils_ui import  render_google_profile
render_google_profile()

# ------------------ AUTH CHECK ------------------
if "role" not in st.session_state or st.session_state.role != "admin":
    st.error("🚫 Admin access required")
    st.stop()

# ------------------ PAGE TITLE ------------------
st.markdown("<h1 class='header-title'>⚙️ Admin Panel</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>System management and comprehensive user overview.</p>", unsafe_allow_html=True)

# ------------------ TABS ------------------
tab1, tab2, tab3 = st.tabs(["👥 Users", "📚 All Books", "📊 System Logs"])

# ================== USERS TAB ==================
with tab1:
    st.write("")
    try:
        from utils import API_BASE
        response = requests.get(
            f"{API_BASE}/auth/users",
            params={"admin_id": st.session_state.user_id}
        )

        if response.status_code == 200:
            users = response.json()

            total_users = len(users)
            admin_count = len([u for u in users if u['role'] == 'admin'])
            user_count = total_users - admin_count

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Users", total_users)
            col2.metric("Regular Users", user_count)
            col3.metric("Admins", admin_count)

            st.divider()

            # -------- USER LIST --------
            st.markdown("### User Directory")
            
            for user in users:
                is_admin = user['role'] == 'admin'
                role_badge = f'<span class="badge badge-{"red" if is_admin else "blue"}">{user["role"].upper()}</span>'
                
                join_date = "-"
                if user['created_at']:
                    join_date = datetime.fromisoformat(
                        user['created_at'].replace('Z', '+00:00')
                    ).strftime('%Y-%m-%d')

                # Using glass-card with flex row for cleaner list view
                with st.container():
                     st.markdown(f"""
                    <div class="glass-card" style="padding: 1.5rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 800; font-size: 1.1rem; margin-bottom: 0.25rem; display:flex; align-items:center; gap:0.5rem;">
                                {user['username']} {role_badge}
                            </div>
                            <div style="color: var(--text-muted); font-size: 0.9rem;">{user['email']}</div>
                        </div>
                        <div style="text-align: right; font-size: 0.9rem;">
                            <div style="color: var(--text-muted); margin-bottom:0.25rem;">Joined: {join_date}</div>
                            <div class="badge badge-green"><b>{user['book_count']}</b> Books</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                     
                     # Action buttons in a row below card for clarity
                     c_act, _ = st.columns([1, 4])
                     with c_act:
                         if st.button(f"📋 Logs", key=f"logs_{user['id']}", use_container_width=True):
                            st.session_state.selected_user_logs = user['id']
                            st.session_state.selected_username = user['username']
                            st.rerun()

        else:
            st.error("Failed to fetch users")

    except Exception as e:
        st.error(f"Connection error: {str(e)}")

# ================== BOOKS TAB ==================
with tab2:
    st.write("")
    st.markdown("### 📚 System-Wide Book Management")
    
    try:
        from utils import API_BASE
        
        # Fetch all books
        with st.spinner("Loading all books..."):
            response = requests.get(f"{API_BASE}/books/all")
        
        if response.status_code == 200:
            all_books = response.json()
            
            if not all_books:
                st.info("📭 No books in the system yet.")
            else:
                # Statistics Dashboard
                total_books = len(all_books)
                summarized_books = sum(1 for b in all_books if b.get("has_summary"))
                unique_users = len(set(b.get("user_id") for b in all_books if b.get("user_id")))
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📚 Total Books", total_books)
                with col2:
                    st.metric("✅ Summarized", summarized_books)
                with col3:
                    st.metric("⏳ Pending", total_books - summarized_books)
                with col4:
                    st.metric("👥 Active Users", unique_users)
                
                st.divider()
                
                # Search and Filter
                with st.expander("🔍 Search & Filter", expanded=False):
                    search_col1, search_col2 = st.columns(2)
                    with search_col1:
                        search_title = st.text_input("Search by title", placeholder="Book title...")
                    with search_col2:
                        search_author = st.text_input("Search by author", placeholder="Author name...")
                    
                    filter_col1, filter_col2 = st.columns(2)
                    with filter_col1:
                        filter_status = st.selectbox("Filter by status", ["All", "Summarized", "Not Summarized"])
                    with filter_col2:
                        filter_type = st.selectbox("Filter by type", ["All", "PDF", "TXT"])
                
                # Apply filters
                filtered_books = all_books
                
                if search_title:
                    filtered_books = [b for b in filtered_books if search_title.lower() in b.get("title", "").lower()]
                
                if search_author:
                    filtered_books = [b for b in filtered_books if search_author.lower() in b.get("author", "").lower()]
                
                if filter_status == "Summarized":
                    filtered_books = [b for b in filtered_books if b.get("has_summary")]
                elif filter_status == "Not Summarized":
                    filtered_books = [b for b in filtered_books if not b.get("has_summary")]
                
                if filter_type != "All":
                    filtered_books = [b for b in filtered_books if b.get("file_type", "").upper() == filter_type]
                
                st.markdown(f"**Showing {len(filtered_books)} of {total_books} books**")
                st.write("")
                
                # Display books
                for book in filtered_books:
                    date = "-"
                    if book.get("created_at"):
                        date = datetime.fromisoformat(
                            book["created_at"].replace("Z", "+00:00")
                        ).strftime("%b %d, %Y")
                    
                    # Status badge
                    status_badge = ""
                    if book.get("has_summary"):
                        status_badge = '<span class="badge badge-green">✓ Summarized</span>'
                    else:
                        status_badge = '<span class="badge" style="background: var(--warning); color: white;">⏳ Pending</span>'
                    
                    # Get username
                    username = book.get("username", "Unknown User")
                    
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid var(--primary);">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                            <div style="flex: 1;">
                                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; color: var(--text-main);">
                                    {book['title']}
                                </h3>
                                <div style="color: var(--text-body); font-size: 0.95rem; margin-bottom: 0.5rem;">
                                    ✍️ {book.get('author', 'Unknown Author')}
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted);">
                                    <span>👤 {username}</span>
                                    <span>🏷️ {book.get('tags', 'No tags')}</span>
                                    <span>📄 {book.get('file_type', 'txt').upper()}</span>
                                    <span>📅 {date}</span>
                                </div>
                            </div>
                            <div style="text-align: right; flex-shrink: 0;">
                                {status_badge}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    btn_col1, btn_col2, btn_col3, spacer = st.columns([1, 1, 1, 3])
                    with btn_col1:
                        if st.button("👁️ View", key=f"admin_view_{book['id']}", use_container_width=True):
                            st.session_state.admin_selected_book = book['id']
                            st.rerun()
                    with btn_col2:
                        if st.button("📊 Stats", key=f"admin_stats_{book['id']}", use_container_width=True):
                            st.session_state.admin_book_stats = book['id']
                            st.rerun()
                    with btn_col3:
                        if st.button("🗑️ Delete", key=f"admin_del_{book['id']}", use_container_width=True, type="secondary"):
                            st.session_state.admin_delete_book = book['id']
                            st.rerun()
                    
                    st.write("")
        
        else:
            st.error("Failed to fetch books from the system")
    
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

# ================== LOGS TAB ==================
with tab3:
    st.write("")
    st.markdown("### 📊 System Activity Logs")
    
    # Check if viewing specific user logs
    if st.session_state.get("selected_user_logs"):
        user_id = st.session_state.selected_user_logs
        username = st.session_state.get("selected_username", "User")

        st.success(f"📋 Viewing logs for: **{username}**")
        st.write("")

        try:
            from utils import API_BASE
            response = requests.get(f"{API_BASE}/auth/logs/{user_id}")

            if response.status_code == 200:
                logs = response.json()

                if logs:
                    st.markdown(f"**Total activities: {len(logs)}**")
                    st.write("")
                    
                    for log in logs:
                        time_str = "-"
                        if log["created_at"]:
                            time_str = datetime.fromisoformat(
                                log["created_at"].replace("Z", "+00:00")
                            ).strftime("%b %d, %Y %H:%M")

                        # Color code based on action type
                        action_color = "var(--primary)"
                        if "delete" in log['action'].lower():
                            action_color = "var(--danger)"
                        elif "upload" in log['action'].lower() or "create" in log['action'].lower():
                            action_color = "var(--success)"
                        elif "login" in log['action'].lower():
                            action_color = "var(--info)"

                        st.markdown(f"""
                        <div class="glass-card" style="padding: 1rem; margin-bottom: 0.75rem; border-left: 3px solid {action_color};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 600; color: var(--text-main);">{log['action']}</span>
                                <span style="color: var(--text-muted); font-size: 0.85rem;">🕒 {time_str}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No logs found for this user")

                st.write("")
                if st.button("⬅️ Back to All Logs", type="secondary"):
                    st.session_state.pop("selected_user_logs", None)
                    st.session_state.pop("selected_username", None)
                    st.rerun()

            else:
                st.error("Failed to fetch logs")

        except Exception as e:
            st.error(f"Connection error: {str(e)}")
    
    else:
        # Show all system logs
        try:
            from utils import API_BASE
            
            # Fetch all logs
            with st.spinner("Loading system logs..."):
                response = requests.get(f"{API_BASE}/auth/logs/all")
            
            if response.status_code == 200:
                all_logs = response.json()
                
                if not all_logs:
                    st.info("📭 No system logs available yet.")
                else:
                    # Statistics
                    total_logs = len(all_logs)
                    unique_users_in_logs = len(set(log.get("user_id") for log in all_logs if log.get("user_id")))
                    
                    # Count action types
                    login_count = sum(1 for log in all_logs if "login" in log.get("action", "").lower())
                    upload_count = sum(1 for log in all_logs if "upload" in log.get("action", "").lower())
                    summary_count = sum(1 for log in all_logs if "summary" in log.get("action", "").lower())
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📝 Total Activities", total_logs)
                    with col2:
                        st.metric("👥 Active Users", unique_users_in_logs)
                    with col3:
                        st.metric("🔐 Logins", login_count)
                    with col4:
                        st.metric("📚 Uploads", upload_count)
                    
                    st.divider()
                    
                    # Filters
                    with st.expander("🔍 Filter Logs", expanded=False):
                        filter_col1, filter_col2 = st.columns(2)
                        with filter_col1:
                            filter_user = st.text_input("Filter by username", placeholder="Enter username...")
                        with filter_col2:
                            filter_action = st.selectbox("Filter by action type", 
                                ["All", "Login", "Upload", "Summary", "Delete", "Register"])
                    
                    # Apply filters
                    filtered_logs = all_logs
                    
                    if filter_user:
                        filtered_logs = [log for log in filtered_logs 
                                       if filter_user.lower() in log.get("username", "").lower()]
                    
                    if filter_action != "All":
                        filtered_logs = [log for log in filtered_logs 
                                       if filter_action.lower() in log.get("action", "").lower()]
                    
                    st.markdown(f"**Showing {len(filtered_logs)} of {total_logs} logs**")
                    st.write("")
                    
                    # Display logs
                    for log in filtered_logs[:100]:  # Limit to 100 most recent
                        time_str = "-"
                        if log.get("created_at"):
                            time_str = datetime.fromisoformat(
                                log["created_at"].replace("Z", "+00:00")
                            ).strftime("%b %d, %Y %H:%M")
                        
                        username = log.get("username", "Unknown User")
                        action = log.get("action", "Unknown Action")
                        
                        # Color code based on action type
                        action_color = "var(--primary)"
                        action_icon = "📌"
                        
                        if "delete" in action.lower():
                            action_color = "var(--danger)"
                            action_icon = "🗑️"
                        elif "upload" in action.lower() or "create" in action.lower():
                            action_color = "var(--success)"
                            action_icon = "📤"
                        elif "login" in action.lower():
                            action_color = "var(--info)"
                            action_icon = "🔐"
                        elif "summary" in action.lower():
                            action_color = "var(--secondary)"
                            action_icon = "✨"
                        elif "register" in action.lower():
                            action_color = "var(--success)"
                            action_icon = "👤"
                        
                        st.markdown(f"""
                        <div class="glass-card" style="padding: 1rem; margin-bottom: 0.75rem; border-left: 3px solid {action_color};">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                                <div style="flex: 1;">
                                    <div style="font-weight: 600; color: var(--text-main); margin-bottom: 0.25rem;">
                                        {action_icon} {action}
                                    </div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                                        👤 {username}
                                    </div>
                                </div>
                                <div style="text-align: right; font-size: 0.85rem; color: var(--text-muted); flex-shrink: 0;">
                                    🕒 {time_str}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if len(filtered_logs) > 100:
                        st.info(f"ℹ️ Showing first 100 of {len(filtered_logs)} logs. Use filters to narrow down results.")
            
            else:
                st.error("Failed to fetch system logs")
        
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("💡 Tip: Make sure the backend API endpoint `/auth/logs/all` is implemented.")

# ------------------ NAVIGATION ------------------
st.divider()
nav1, nav2 = st.columns(2)

with nav1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

with nav2:
    if st.button("🚪 Logout", use_container_width=True, key="admin_logout_btn"):
        st.session_state.clear()
        st.session_state.page = "Home"
        st.rerun()

