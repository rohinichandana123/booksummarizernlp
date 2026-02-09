import streamlit as st
import streamlit.components.v1 as components
from utils import generate_summary, generate_summary_from_file, generate_audio, API_BASE
import requests
import base64

# =========================================================
# SESSION STATE
# =========================================================
if "show_copy_box" not in st.session_state:
    st.session_state.show_copy_box = False

if "current_summary" not in st.session_state:
    st.session_state.current_summary = None

summary_ready = st.session_state.current_summary is not None

# =========================================================
# HERO HEADER
# =========================================================
st.markdown("""
<div style="text-align:center; margin-top:20px; margin-bottom:50px;">
    <h1 style="font-size:44px;font-weight:800;">✨ Generate Summary</h1>
    <p style="font-size:18px;color:#6b7280;">
        Extract key insights from your books instantly.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 🟦 GENERATE PANEL
# =========================================================
if not summary_ready:

    spacer_l, main_col, spacer_r = st.columns([1, 7, 1])

    with main_col:

        # ===============================
        # 📄 INPUT SOURCE
        # ===============================
        st.markdown("### 📄 Input Source")

        source = st.radio(
            "Choose Source",
            ["Paste Text", "Upload File (PDF/TXT)"],
            horizontal=True,
            key="summary_source"
        )

        if source == "Paste Text":
            input_text = st.text_area(
                "Paste book content here:",
                height=360,
                placeholder="Type or paste your text here...",
                key="summary_text"
            )
            uploaded_file = None

            if input_text:
                st.caption(f"Words entered: {len(input_text.split())}")

        else:
            uploaded_file = st.file_uploader(
                "Upload PDF or Text file",
                type=["pdf", "txt"],
                key="summary_file"
            )
            input_text = ""
            st.info("Supported formats: .pdf, .txt")

        # ===============================
        # ⚙️ SETTINGS
        # ===============================
        st.markdown("### ⚙️ Settings")

        c1, c2 = st.columns(2)

        with c1:
            output_format = st.selectbox(
                "Output Format",
                ["Paragraph", "Bullet Points"],
                key="summary_format"
            )

        with c2:
            summary_length = st.selectbox(
                "Summary Length",
                ["100 words", "200 words", "300 words"],
                index=1,
                key="summary_length"
            )

        st.write("")

        generate_clicked = st.button(
            "🚀 Generate Summary",
            use_container_width=True
        )

        # ===============================
        # GENERATE ACTION
        # ===============================
        if generate_clicked:
            with st.spinner("Generating summary..."):
                try:
                    word_limit = int(summary_length.split()[0])
                    res = None

                    if source == "Paste Text" and input_text.strip():
                        res = generate_summary({
                            "text": input_text,
                            "user_id": st.session_state.get("user_id"),
                            "format": output_format,
                            "max_words": word_limit
                        })

                    elif source == "Upload File (PDF/TXT)" and uploaded_file:
                        files = (
                            {"pdf": uploaded_file.getvalue()}
                            if uploaded_file.name.endswith(".pdf")
                            else {"text_file": uploaded_file.getvalue()}
                        )
                        res = generate_summary_from_file(files)

                    else:
                        st.error("Please provide text or upload a file.")
                        st.stop()

                    if res and res.status_code == 200:
                        st.session_state.current_summary = res.json().get("summary", "")
                        st.rerun()

                    elif res:
                        st.error(res.text)

                except Exception as e:
                    st.error(f"Connection error: {str(e)}")


# =========================================================
# 🟩 OUTPUT PANEL (VISIBLE IF SUMMARY READY)
# =========================================================
else:

    spacer_l, main_col, spacer_r = st.columns([1, 7, 1])

    with main_col:
        
        # ===============================
        # 🔹 BACK NAVIGATION
        # ===============================
        top_l, top_r = st.columns([6, 2])
        
        # NOTE: We can keep or remove the Clear Summary logic here, the users requested toggle behavior
        # But specifically asked for 'Generate New Summary' to navigate back input.

        st.markdown("### 📘 Generated Summary")

        summary_text = st.session_state.current_summary
        summary_word_count = len(summary_text.split())

        st.markdown(f"""
        <div style="
            height:70vh;
            overflow-y:auto;
            padding:28px;
            border-radius:18px;
            background:white;
            border:1px solid rgba(0,0,0,0.05);
            box-shadow:0 10px 40px rgba(0,0,0,0.06);
            white-space: pre-wrap;
            line-height:1.8;
            font-size:16.5px;
        ">
        {summary_text}
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # 🔊 AUDIO
        audio_file = generate_audio(summary_text)
        audio_bytes = open(audio_file, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

        st.markdown("### 🔊 Listen to Summary")

        components.html(f"""
        <audio controls style="width:100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """, height=80)

        st.write("")

        # ACTION BUTTONS
        r1_c1, r1_c2 = st.columns(2)

        with r1_c1:
            st.download_button(
                "📥 Download",
                summary_text,
                file_name="summary.txt",
                use_container_width=True
            )

        with r1_c2:
            if st.button("💾 Save", use_container_width=True):
                payload = {
                    "user_id": st.session_state.get("user_id"),
                    "summary": summary_text,
                    "word_count": summary_word_count
                }
                requests.post(f"{API_BASE}/summaries/save", json=payload)
                st.toast("Summary saved!", icon="💾")

        r2_c1, r2_c2 = st.columns(2)

        with r2_c1:
            if st.button("📋 Copy", use_container_width=True):
                st.toast("Summary Copied!", icon="📋")
                
            

        with r2_c2:
            if st.button("🔄 Generate New Summary", use_container_width=True):
                st.session_state.current_summary = None
                st.rerun()
