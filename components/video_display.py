import streamlit as st

def render_video_section(col, video_file):
    with col.container():
        st.markdown("#### 🎬 Video Playback")
        st.markdown("<hr style='margin-top:-5px;margin-bottom:15px;'>", unsafe_allow_html=True)

        if video_file:
            st.video(video_file)
            st.success(f"✅ Now playing: {video_file.name}")
        else:
            st.info("📽️ No video uploaded — playing demo video")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

        st.caption("Supported formats: MP4, MOV, AVI")
