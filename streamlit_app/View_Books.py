import streamlit as st
import requests
from datetime import datetime

# ───────────────── AUTH CHECK ─────────────────
if "user_id" not in st.session_state:
    st.warning("Login required")
    st.stop()

# ───────────────── PAGE TITLE ─────────────────
st.markdown('<h2 class="header-title"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 0.5rem;"><path d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.5 2H20V22H6.5C5.83696 22 5.20107 21.7366 4.73223 21.2678C4.26339 20.7989 4 20.163 4 19.5V4.5C4 3.83696 4.26339 3.20107 4.73223 2.73223C5.20107 2.26339 5.83696 2 6.5 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> My Library</h2>', unsafe_allow_html=True)
st.markdown("<p class='header-subtitle' style='margin-bottom: 2rem;'>Manage, search, and revisit your uploaded books.</p>", unsafe_allow_html=True)

# ───────────────── SEARCH & FILTER ─────────────────
with st.expander("🔍 Search & Filter", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        search_title = st.text_input("Search by title", placeholder="e.g. Harry Potter")
    with col2:
        search_author = st.text_input("Search by author", placeholder="e.g. J.K. Rowling")
    with col3:
        search_tag = st.text_input("Search by tag", placeholder="e.g. Fantasy")

# ───────────────── FETCH BOOKS ─────────────────
try:
    from utils import get_book_details, delete_book, API_BASE

    params = {}
    if search_title:
        params["search"] = search_title
    if search_author:
        params["author"] = search_author
    if search_tag:
        params["tag"] = search_tag

    # Use spinner for better UX
    with st.spinner("Loading library..."):
        response = requests.get(
            f"{API_BASE}/books/list/{st.session_state.user_id}",
            params=params
        )

    if response.status_code != 200:
        st.error("Failed to fetch books")
        st.stop()

    books = response.json()

    if not books:
        st.info("📭 No books found in your library.")
    else:
        st.markdown(f"**Found {len(books)} book(s)**")
        st.write("")

        for book in books:
            # CARD DISPLAY
            # We create a visual card using standard elements
            
            with st.container():
                # Top Row: Info
                # We can't wrap this perfectly in a CSS box without breaking buttons, 
                # so we use a markdown block for the visual info, and buttons below.
                
                date = "-"
                if book.get("created_at"):
                    date = datetime.fromisoformat(
                        book["created_at"].replace("Z", "+00:00")
                    ).strftime("%Y-%m-%d")

                badge_html = "<div></div>"
                if book.get("has_summary"):
                    badge_html = '<span class="badge badge-green">Summarized</span>'


                # HTML Info Card
                st.markdown(f"""
                <div class="glass-card" style="padding: 1.25rem; margin-bottom: 0.5rem; border-left: 4px solid var(--primary);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 style="margin: 0; font-size: 1.2rem; color: var(--text-main);">{book['title']}</h3>
                            <p style="margin: 0.2rem 0 0.5rem; color: var(--text-body); font-size: 0.95rem;">
                                ✍️ {book.get('author', 'Unknown')}
                            </p>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">
                                🏷️ {book.get('tags', 'No tags')} &bull; 📄 {book['file_type'].upper()}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 0.8rem; color: var(--text-muted);">{date}</span>
                            <br>
                            {badge_html}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Action Row (Buttons)
                # We place buttons right under the card
                c1, c2, c3, spacer = st.columns([1, 1, 1, 3])
                
                with c1:
                    if st.button("📝 Summarize", key=f"sum_{book['id']}", use_container_width=True):
                         st.session_state.nav = "Summarize New"
                         st.session_state.prefill_book_id = book["id"] 
                         st.rerun()
                with c2:
                    if st.button("👁️ Details", key=f"view_{book['id']}", use_container_width=True):
                        st.session_state.selected_book_id = book["id"]
                        st.session_state.show_book_detail = True
                        st.rerun()
                
                # Close container visually
                st.write("") 

except Exception as e:
    st.error(f"Error loading books: {e}")
    st.stop()


# ───────────────── BOOK DETAIL VIEW ─────────────────
if st.session_state.get("show_book_detail") and st.session_state.get("selected_book_id"):
    st.markdown("---")
    st.markdown("### 📖 Book Details")
    
    try:
        res = get_book_details(st.session_state.selected_book_id)

        if res.status_code != 200:
            st.error("Failed to load book details")
            st.stop()

        book = res.json()

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.markdown(f"## {book['title']}")

        m1, m2 = st.columns(2)
        with m1:
            if book.get("author"):
                st.markdown(f"**Author:** {book['author']}")
            if book.get("tags"):
                st.markdown(f"**Tags:** {book['tags']}")

        with m2:
            st.markdown(f"**File Type:** {book['file_type'].upper()}")
            if book.get("created_at"):
                uploaded = datetime.fromisoformat(
                    book["created_at"].replace("Z", "+00:00")
                ).strftime("%Y-%m-%d %H:%M")
                st.markdown(f"**Uploaded:** {uploaded}")

        st.markdown("#### 📄 Content Preview")
        preview = book["content"][:800] + "..." if len(book["content"]) > 800 else book["content"]
        st.text_area("", preview, height=200, disabled=True)

        if book.get("summaries"):
            st.markdown("#### 📋 Existing Summaries")
            for s in book["summaries"]:
                with st.expander(f"{s.get('length_setting', 'Summary')} – {s.get('created_at', '')[:10]}"):
                    st.write(s["summary_text"])

        # ───────────────── ACTIONS ─────────────────
        st.divider()
        st.markdown("#### Actions")

        a1, a2 = st.columns(2)

        with a1:
            if st.button("📝 Generate New Summary", use_container_width=True):
                st.session_state.nav = "Summarize New"
                st.session_state.prefill_text = book["content"] # Pass content
                st.session_state.prefill_source_type = "Paste Text" # Hint
                st.rerun()

        with a2:
            if st.button("🗑️ Delete Book", type="primary", use_container_width=True):
                st.session_state.confirm_delete = True

        if st.session_state.get("confirm_delete"):
            st.warning("⚠️ Are you sure you want to delete this book? This cannot be undone.")
            d1, d2 = st.columns(2)

            with d1:
                if st.button("✅ Yes, Delete", key="confirm_del_btn", use_container_width=True):
                    del_res = delete_book(book["id"])
                    if del_res.status_code == 200:
                        st.success("Book deleted")
                        st.session_state.pop("confirm_delete")
                        st.session_state.pop("show_book_detail")
                        st.session_state.pop("selected_book_id")
                        st.rerun()
                    else:
                        st.error("Delete failed")

            with d2:
                if st.button("❌ Cancel", key="cancel_del_btn", use_container_width=True):
                    st.session_state.pop("confirm_delete")
                    st.rerun()

        if st.button("❌ Close Details", key="close_details"):
            st.session_state.pop("show_book_detail")
            st.session_state.pop("selected_book_id")
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Detail error: {e}")