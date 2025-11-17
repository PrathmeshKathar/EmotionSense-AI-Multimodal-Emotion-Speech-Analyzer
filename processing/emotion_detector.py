from streamlit_webrtc import VideoProcessorBase
from deepface import DeepFace
import av
import cv2

class EmotionDetector(VideoProcessorBase):
    def __init__(self):
        self.emotion_counts = {e: 0 for e in ['happy', 'sad', 'angry', 'fear', 'surprise', 'disgust', 'neutral']}
        self.last_emotion = None
        self.counting_enabled = False

    def enable_emotion_counting(self, state: bool):
        self.counting_enabled = state

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']

            if self.counting_enabled and emotion in self.emotion_counts:
                self.emotion_counts[emotion] += 1

            label = emotion.upper() if self.counting_enabled else "Camera ON (No Detection)"
            cv2.rectangle(img, (20, 20), (450, 80), (42, 157, 244), -1)
            cv2.putText(img, label, (35, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        except Exception:
            cv2.putText(img, "No Face Detected", (35, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
