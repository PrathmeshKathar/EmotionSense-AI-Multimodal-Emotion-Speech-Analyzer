import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
import numpy as np

def show_emotion_dashboard(emotion_counts, transcript_text, ai_summary):
    st.markdown("<h3 style='color:#2a9df4;'>📊 Emotion Analytics Dashboard</h3>", unsafe_allow_html=True)
    

    col1, col2 = st.columns(2)

    # ---------- Emotion Distribution ----------
    with col1:
        st.subheader("🎭 Emotion Distribution")
        df = pd.DataFrame(list(emotion_counts.items()), columns=["Emotion", "Count"])
        fig = px.bar(df, x="Emotion", y="Count", color="Emotion", text="Count",
                     title="Emotion Frequency", color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    # ---------- Emotion Composition Pie ----------
    with col2:
        st.subheader("🧩 Emotion Composition")
        fig2 = px.pie(df, names="Emotion", values="Count", hole=0.4,
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------- Heatmap ----------
    st.subheader("🔥 Emotion Co-occurrence Heatmap (Demo)")
    emotion_labels = list(emotion_counts.keys())
    matrix = np.random.randint(0, 100, size=(len(emotion_labels), len(emotion_labels)))
    df_heatmap = pd.DataFrame(matrix, index=emotion_labels, columns=emotion_labels)
    fig3, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(df_heatmap, annot=True, cmap="coolwarm", fmt="d", ax=ax)
    st.pyplot(fig3, use_container_width=True)

    st.divider()

    # ---------- Word Cloud ----------
    st.subheader("☁️ Word Cloud (AI Summary)")
    try:
        wc = WordCloud(width=800, height=400, background_color="black", colormap="cool").generate(ai_summary)
        st.image(wc.to_array(), use_column_width=True)
    except Exception as e:
        st.warning(f"Word cloud generation failed: {e}")

    st.divider()

    # ---------- Insights ----------
    st.subheader("🧠 Emotion Insights Summary")
    df_sorted = df.sort_values("Count", ascending=False)
    dominant_emotion = df_sorted.iloc[0]["Emotion"]
    st.info(f"💬 **Dominant Emotion:** {dominant_emotion}")
    st.dataframe(df_sorted, use_container_width=True)
