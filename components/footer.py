import streamlit as st

def render_footer():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;color:gray;padding:1rem 0;'>
        Developed with ❤️ using <b>Streamlit + DeepFace + Plotly</b><br>
        <span style='font-size:13px;'>© 2025 Emotion Analyzer Project</span>
    </div>
    """, unsafe_allow_html=True)
