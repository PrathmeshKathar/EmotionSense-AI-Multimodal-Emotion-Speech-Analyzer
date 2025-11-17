import ffmpeg
import os

def extract_audio(video_path, output_dir="temp_audio"):
    """
    Extracts audio from a video file using ffmpeg-python and saves it as a .wav file.
    Works without moviepy and runs on CPU.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "audio.wav")

    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_path, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error extracting audio: {e}")
