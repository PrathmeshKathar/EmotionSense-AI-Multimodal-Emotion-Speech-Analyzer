from streamlit_webrtc import webrtc_streamer
from .emotion_detector import EmotionDetector

def start_webcam_stream(col):
    col.markdown("### 🎭 Webcam Emotion Detection")
    ctx = webrtc_streamer(
        key="emotion_detector",
        video_processor_factory=EmotionDetector,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    )
    return ctx
