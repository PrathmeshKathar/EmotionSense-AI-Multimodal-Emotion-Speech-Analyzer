from vosk import Model, KaldiRecognizer
import wave, json, os

def convert_audio_to_text(audio_path, model_path="vosk-model-small-en-us-0.15"):
    """
    Converts a WAV audio file into text using the offline Vosk model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please download it from https://alphacephei.com/vosk/models")

    wf = wave.open(audio_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
        raise ValueError("Audio file must be WAV format mono PCM with 8kHz or 16kHz sample rate.")

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    result_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = json.loads(rec.Result())
            result_text += part.get("text", "") + " "

    return result_text.strip()
