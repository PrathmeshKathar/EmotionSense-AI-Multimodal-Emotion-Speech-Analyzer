def generate_ai_summary_gemini(transcript_text, emotion_counts, video_label):
    import google.generativeai as genai
    import os
    from dotenv import load_dotenv
    load_dotenv()

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an expert AI emotion summarizer.
    Summarize the emotional analysis of this video in **one short line only**.
    Use emojis and concise keywords for quick readability.

    Video Emotion Label: {video_label}
    Transcript snippet: {transcript_text[:400]}
    Detected Emotion Counts: {emotion_counts}

    Format strictly as:
    🎭 <Dominant Emotion> | <Tone: 🔵 Positive / 🔴 Negative / ⚪ Neutral> | Match: <High/Medium/Low> | Summary: <short 1-line insight>
    """

    response = model.generate_content(prompt)
    return response.text.strip()
