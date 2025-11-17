import streamlit as st
import os
import time
from datetime import timedelta
from streamlit_webrtc import webrtc_streamer
from streamlit_javascript import st_javascript
from processing.emotion_detector import EmotionDetector
from processing.audio_extractor import extract_audio
from processing.speech_to_text_vosk import convert_audio_to_text
from utils.llm_summary_gemini import generate_ai_summary_gemini
from utils.analytics_dashboard import show_emotion_dashboard

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Emotion + Audio + AI Analyzer", layout="wide", page_icon="🎭")

# ---------- STYLE ----------
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #fafafa; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        background-color: #2a9df4; color: white; border-radius: 8px; padding: 0.5rem 1rem;
        font-weight: 600; border: none; transition: 0.2s ease-in-out;
    }
    .stButton>button:hover { background-color: #1c86d1; }
    .section-box {
        border-radius: 10px; background-color: #11141c;
        padding: 1rem 1.5rem; margin-bottom: 1rem; border-left: 5px solid #2a9df4;
    }
    .header-title { font-size: 2rem; font-weight: 700; color: #2a9df4; }
    .timer { font-size: 1.3rem; font-weight: 600; color: #2a9df4; text-align: center; margin: 0.5rem 0; }

    /* Floating Fullscreen Buttons */
    .floating-btn {
        position: fixed;
        bottom: 40px;
        right: 40px;
        background-color: #2a9df4;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        cursor: pointer;
        z-index: 9999;
        transition: all 0.3s ease;
    }
    .floating-btn:hover {
        background-color: #1c86d1;
        transform: scale(1.05);
    }
    #stop-btn {
        background-color: #ff4b4b;
        right: 180px;
    }
    #stop-btn:hover {
        background-color: #d63c3c;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 class='header-title'>🎭 Emotion + Audio + AI Analyzer</h1>", unsafe_allow_html=True)

st.divider()

# ---------- SESSION STATE ----------
if "ctx" not in st.session_state:
    st.session_state.ctx = None
if "analyzing" not in st.session_state:
    st.session_state.analyzing = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "analyze_trigger" not in st.session_state:
    st.session_state.analyze_trigger = None
if "video_emotion_label" not in st.session_state:
    st.session_state.video_emotion_label = None

# ---------- VIDEO UPLOAD ----------
st.markdown("<div class='section-box'>📤 <b>Upload Video</b></div>", unsafe_allow_html=True)
video_file = st.file_uploader("", type=["mp4", "mov", "avi"], label_visibility="collapsed")

if video_file:
    # ---------- USER INPUT: Emotion Label ----------
    st.markdown("### 🎯 Category for Uploaded Video")
    emotion_label = st.selectbox(
        "Labeled video:",
        ["Happy 😊", "Sad 😢", "Angry 😠", "Fear 😨", "Surprise 😲", "Disgust 🤢", "Neutral 😐"],
        index=0
    )
    st.session_state.video_emotion_label = emotion_label
    st.success(f"Selected Labeled Category: {emotion_label}")

    # ---------- VIDEO & WEBCAM LAYOUT ----------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎬 Uploaded Video")
        st.video(video_file)
        

    with col2:
        st.markdown("### 📸 Webcam")
        ctx = webrtc_streamer(
            key="emotion_detector",
            video_processor_factory=EmotionDetector,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )
        st.session_state.ctx = ctx

    st.divider()

    # ---------- CONTROL PANEL ----------
    st.markdown("<div class='section-box'>🧠 <b>Step 2: Control Emotion Analysis</b></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    start_analyze = col_a.button("▶️ Start Analyze", use_container_width=True)
    stop_analyze = col_b.button("⏹ Stop Analyze", use_container_width=True)

    timer_placeholder = st.empty()

    # ---------- FLOATING BUTTONS ----------
    st.markdown("""
    <script>
    function triggerStreamlitEvent(eventType) {
        const streamlitEvent = new CustomEvent("streamlit_custom_event", { detail: eventType });
        window.parent.document.dispatchEvent(streamlitEvent);
    }
    </script>

    <button class="floating-btn" id="start-btn" onclick="triggerStreamlitEvent('start_analyze')">▶️ Start Analyze</button>
    <button class="floating-btn" id="stop-btn" onclick="triggerStreamlitEvent('stop_analyze')">⏹ Stop Analyze</button>
    """, unsafe_allow_html=True)

    # Listen for events
    event_type = st_javascript("""
    new Promise((resolve) => {
        document.addEventListener("streamlit_custom_event", (e) => {
            resolve(e.detail);
        });
    });
    """)

    if event_type == "start_analyze":
        st.session_state.analyze_trigger = "start"
    elif event_type == "stop_analyze":
        st.session_state.analyze_trigger = "stop"

    # ---------- START ANALYZE ----------
    if (start_analyze or st.session_state.analyze_trigger == "start") and st.session_state.ctx and not st.session_state.analyzing:
        st.session_state.analyzing = True
        st.session_state.start_time = time.time()
        st.success("✅ Started emotion counting.")
        st.session_state.ctx.video_processor.enable_emotion_counting(True)
        st.session_state.analyze_trigger = None

    # ---------- WHILE ANALYZING ----------
    if st.session_state.analyzing and st.session_state.ctx and st.session_state.ctx.state.playing:
        elapsed = int(time.time() - st.session_state.start_time)
        timer_placeholder.markdown(f"<div class='timer'>⏱️ Counting emotions: {str(timedelta(seconds=elapsed))}</div>", unsafe_allow_html=True)

    # ---------- STOP ANALYZE ----------
    if (stop_analyze or st.session_state.analyze_trigger == "stop") and st.session_state.analyzing:
        st.session_state.analyzing = False
        st.session_state.ctx.video_processor.enable_emotion_counting(False)
        elapsed = int(time.time() - st.session_state.start_time)
        st.markdown(f"<div class='timer'>✅ Final Duration: {str(timedelta(seconds=elapsed))}</div>", unsafe_allow_html=True)
        st.success("🧩 Stopped emotion counting. Starting full analysis...")
        st.session_state.analyze_trigger = None

        # ---------- EMOTION DATA ----------
        emotions = st.session_state.ctx.video_processor.emotion_counts
        selected_emotion = st.session_state.video_emotion_label or "Not specified"

        # ---------- FULL PIPELINE ----------
        with st.spinner("Processing full analysis..."):
            temp_video_path = f"temp_video_{int(time.time())}.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(video_file.getbuffer())

            
            audio_path = extract_audio(temp_video_path)


            transcript = convert_audio_to_text(audio_path)
            st.text_area("📝 Transcript", transcript, height=150)

        
            # Include user emotion label in prompt
            try:
                summary = generate_ai_summary_gemini(transcript, emotions, selected_emotion)
                
                st.markdown("### 🧠 Emotional Summary")
                st.markdown(f"<div class='section-box'>{summary}</div>", unsafe_allow_html=True)

                st.markdown("---")
                show_emotion_dashboard(emotions, transcript, summary)
            except Exception as e:
                st.error(f"❌ Gemini Summary failed: {e}")

            st.info(f"🕒 Total Analyze Duration: {str(timedelta(seconds=elapsed))}")
            os.remove(temp_video_path)

else:
    st.warning("Upload video First.")

st.divider()
st.markdown(
    "<center>Developed with ❤️ </center>",
    unsafe_allow_html=True
)
