import streamlit as st
from utils.theme_manager import toggle_theme

def render_sidebar():
    if st.button(("🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"), use_container_width=True):
        toggle_theme()
        st.rerun()

    st.markdown("---")
    video_file = st.file_uploader("📤 Upload Video", type=["mp4", "mov", "avi"])
    st.markdown("🎨 Supported Emotions: 😊 😢 😠 😨 😲 🤢 😐")
    return video_file
