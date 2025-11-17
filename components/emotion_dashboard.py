import streamlit as st
import plotly.graph_objects as go
from utils.emotion_data import emoji_map
import time

def render_dashboard(ctx):
    st.markdown("#### 📊 Emotion Dashboard")
    st.markdown("<hr style='margin-top:-5px;margin-bottom:15px;'>", unsafe_allow_html=True)

    chart_placeholder = st.empty()
    cards_placeholder = st.empty()

    # Initialize persistent storage for summary
    if "final_summary" not in st.session_state:
        st.session_state.final_summary = None

    # If webcam is playing (live)
    if ctx.state.playing and ctx.video_processor:
        processor = ctx.video_processor
        while ctx.state.playing:
            emotions = processor.emotion_counts

            # Save the current state as latest summary
            st.session_state.final_summary = emotions.copy()

            # Update live dashboard
            render_emotion_dashboard(chart_placeholder, cards_placeholder, emotions, title="Emotion Frequency (Live)")

            time.sleep(1)

    # If webcam stopped but we have saved summary
    elif st.session_state.final_summary:
        st.success("📊 Webcam stopped — showing final emotion summary below.")
        emotions = st.session_state.final_summary
        render_emotion_dashboard(chart_placeholder, cards_placeholder, emotions, title="Final Emotion Summary")

    else:
        st.info("🟠 Start your webcam to view live emotion analytics.")

# Helper function for chart + cards rendering
def render_emotion_dashboard(chart_placeholder, cards_placeholder, emotions, title):
    # --- Chart ---
    fig = go.Figure([
        go.Bar(
            x=list(emotions.keys()),
            y=list(emotions.values()),
            text=[emoji_map[e] for e in emotions.keys()],
            textposition="outside",
            marker_color=[
                "#FFD700", "#1E90FF", "#FF6347",
                "#9370DB", "#00CED1", "#32CD32", "#A9A9A9"
            ]
        )
    ])
    fig.update_layout(
        title=title,
        xaxis_title="Emotion Type",
        yaxis_title="Count",
        height=350,
        template="plotly_dark",
        margin=dict(t=40, b=20)
    )

    # Update chart
    with chart_placeholder:
        st.plotly_chart(fig, use_container_width=True)

    # --- Cards ---
    with cards_placeholder.container():
        cols = st.columns(7)
        for i, (emotion, count) in enumerate(emotions.items()):
            with cols[i]:
                st.markdown(f"""
                <div class='emotion-card'>
                    <h3>{emoji_map[emotion]}</h3>
                    <p><b>{emotion.capitalize()}</b></p>
                    <p class='count'>{count}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- CSS styling ---
    st.markdown("""
    <style>
        .emotion-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 0.8rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .emotion-card h3 {
            font-size: 28px;
            margin-bottom: 5px;
        }
        .emotion-card p {
            margin: 0;
            font-size: 14px;
            color: #9ca3af;
        }
        .emotion-card .count {
            font-size: 20px;
            color: #60a5fa;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
