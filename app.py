import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from scripts.twitter_scraper import get_tweets
from scripts.reddit_scraper import get_reddit_posts
from scripts.sentiment import analyze_sentiment

# --- Page Config ---
st.set_page_config(
    page_title="Sentilytics AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for 3D Dark UI ---
st.markdown("""
<style>
/* Dark background */
body {
    background-color: #121212;
    color: #eeeeee;
}

[data-testid="stAppViewContainer"] {
    background-color: #0f1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1c1c1c;
    box-shadow: 4px 0 8px rgba(0, 0, 0, 0.5);
}

/* Neon header */
.neon-text {
    font-size: 2.5rem;
    font-weight: 700;
    color: #00ffe7;
    text-shadow: 0 0 5px #00ffe7, 0 0 10px #00ffe7, 0 0 20px #00ffe7;
    padding-bottom: 0.3em;
}

/* Styled box/card */
.block-container {
    background-color: #1e1e1e;
    padding: 2em;
    border-radius: 1em;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    margin-top: 2em;
}

hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #00ffe7, transparent);
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="neon-text">🧠 Sentilytics: Real-Time Social Sentiment</div>', unsafe_allow_html=True)
st.markdown("Analyze live Twitter and Reddit sentiment for any stock, crypto or brand in seconds.")
st.markdown("<hr/>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
keyword = st.sidebar.text_input("Enter a stock/company/crypto keyword", "Adani")
count = st.sidebar.slider("Number of posts per platform", 10, 50, 20)

# --- Main Action ---
if st.button("🚀 Analyze Now"):
    with st.spinner("🔍 Gathering tweets and Reddit posts..."):
        tweets = get_tweets(keyword, count)
        reddit_posts = get_reddit_posts(keyword, count)

        data = []
        for text, ts in tweets:
            score = analyze_sentiment(text)
            data.append(["Twitter", ts, text, score])

        for text, ts in reddit_posts:
            score = analyze_sentiment(text)
            data.append(["Reddit", ts, text, score])

        df = pd.DataFrame(data, columns=["Platform", "Timestamp", "Text", "Sentiment"])
        df.sort_values("Timestamp", inplace=True)

    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    st.subheader("📊 Sentiment Table")

    def color_sentiment(val):
        if val > 0.2:
            return 'background-color: #153d2e; color: #80ffb2'  # green
        elif val < -0.2:
            return 'background-color: #3d1b1b; color: #ff9999'  # red
        else:
            return 'background-color: #3d3d1b; color: #ffff99'  # yellow

    st.dataframe(df.style.applymap(color_sentiment, subset=["Sentiment"]))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Plot ---
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    st.subheader("📈 Sentiment Over Time (Interactive)")
    fig = px.line(
        df, x="Timestamp", y="Sentiment",
        color="Platform", markers=True,
        template="plotly_dark",
        title=f"📉 {keyword} - Twitter vs Reddit Sentiment"
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
