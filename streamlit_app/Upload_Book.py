import streamlit as st
from utils import upload_book_text, upload_book_pdf

# ───────────────── AUTH CHECK ─────────────────
if "user_id" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# ───────────────── PAGE TITLE ─────────────────
# We assume CSS is loaded by Dashboard/Home

st.markdown("## 🆕 Upload Book")
st.markdown("<p style='color: var(--text-muted); margin-bottom: 2rem;'>Add a new book to your library to generate summaries.</p>", unsafe_allow_html=True)

# ───────────────── UPLOAD METHOD ─────────────────
upload_method = st.radio(
    "Choose upload method",
    ["Text Input", "PDF Upload"],
    horizontal=True
)

st.write("") # Spacer

# ───────────────── TEXT INPUT ─────────────────
if upload_method == "Text Input":
    with st.form("text_upload_form"):
        title = st.text_input("📘 Book Title *", placeholder="e.g. Atomic Habits")
        
        c1, c2 = st.columns(2)
        with c1:
            author = st.text_input("✍️ Author", placeholder="e.g. James Clear")
        with c2:
             tags = st.text_input("🏷️ Tags (optional)", placeholder="productivity, habits")

        content = st.text_area(
            "📖 Book Content *",
            height=300,
            placeholder="Paste your book content here..."
        )

        st.write("")
        submitted = st.form_submit_button("🚀 Upload Book", use_container_width=True)

    if submitted:
        if not title or not content:
            st.error("Title and content are required!")
        else:
            try:
                with st.spinner("Uploading and processing..."):
                    response = upload_book_text({
                        "title": title,
                        "author": author,
                        "content": content,
                        "tags": tags,
                        "file_type": "txt",
                        "user_id": st.session_state["user_id"]
                    })

                if response.status_code == 200:
                    st.success("✅ Book uploaded successfully!")
                    st.balloons()
                else:
                    st.error(response.json().get("error", "Upload failed"))

            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# ───────────────── PDF UPLOAD ─────────────────
elif upload_method == "PDF Upload":
    with st.form("pdf_upload_form"):
        uploaded_file = st.file_uploader(
            "📄 Upload PDF",
            type=["pdf"]
        )
        
        title = st.text_input(
            "📘 Book Title (optional)",
            placeholder="Leave empty to use filename"
        )
        
        c1, c2 = st.columns(2)
        with c1:
            author = st.text_input("✍️ Author", placeholder="Author name")
        with c2:
            tags = st.text_input("🏷️ Tags", placeholder="education, finance")

        st.write("")
        submitted = st.form_submit_button("🚀 Upload PDF", use_container_width=True)

    if submitted:
        if not uploaded_file:
            st.error("Please select a PDF file!")
        else:
            try:
                files = {"file": uploaded_file}
                data = {
                    "title": title if title else uploaded_file.name,
                    "author": author,
                    "tags": tags,
                    "user_id": str(st.session_state["user_id"])
                }

                with st.spinner("Uploading PDF..."):
                    response = upload_book_pdf(files, data)

                if response.status_code == 200:
                    st.success("✅ PDF uploaded successfully!")
                    st.balloons()
                else:
                    st.error(response.json().get("error", "Upload failed"))

            except Exception as e:
                st.error(f"Connection error: {str(e)}")

