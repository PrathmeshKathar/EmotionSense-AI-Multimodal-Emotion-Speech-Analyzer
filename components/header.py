import streamlit as st

def render_header():
    st.markdown("""
    <div class='header-container'>
        <h1>🎥 Emotion + Video Analyzer</h1>
        <p>Analyze real-time emotions while watching your video or webcam feed</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .header-container {
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
            margin-bottom: 2rem;
        }
        .header-container h1 {
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .header-container p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
    </style>
    """, unsafe_allow_html=True)
