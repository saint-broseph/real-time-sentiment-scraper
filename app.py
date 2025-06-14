import streamlit as st
import pandas as pd
from datetime import datetime
from scripts.twitter_scraper import get_tweets
from scripts.reddit_scraper import get_reddit_posts
from scripts.sentiment import analyze_sentiment
import plotly.express as px

# --- App Config ---
st.set_page_config(page_title="Sentilytics", layout="wide")

# --- UI Header ---
st.title("🧠 Sentilytics — Real-Time Social Sentiment")
st.markdown("Track what Twitter and Reddit think about any topic — from stocks to trends to public figures.")

# --- Keyword Input ---
col1, col2 = st.columns([3, 1])
with col1:
    keyword = st.text_input("Enter a topic, stock, person, or trend:", "Adani")
with col2:
    suggested = st.selectbox("Or try a popular one:", ["Adani", "Tesla", "Bitcoin", "Modi", "Israel", "Elon Musk"])

if not keyword:
    keyword = suggested

# --- Main button ---
if st.button("Analyze Sentiment"):
    with st.spinner("🔍 Fetching Twitter & Reddit data..."):

        # Fetch tweets and reddit posts (expecting list of (text, timestamp))
        tweets = get_tweets(keyword, count=15)
        reddit_posts = get_reddit_posts(keyword, limit=15)

        st.write(f"✅ Tweets fetched: {len(tweets)}")
        st.write(f"✅ Reddit posts fetched: {len(reddit_posts)}")

        data = []

        if tweets:
            for text, ts in tweets:
                score = analyze_sentiment(text)
                data.append(["Twitter", ts, text, score])
        else:
            st.warning("⚠️ No tweets found.")

        if reddit_posts:
            for text, ts in reddit_posts:
                score = analyze_sentiment(text)
                data.append(["Reddit", ts, text, score])
        else:
            st.warning("⚠️ No Reddit posts found.")

        if not data:
            st.info("⚠️ No live sentiment found. Showing demo data.")
            data.append(["Twitter", datetime.now(), f"{keyword} is trending heavily today", 0.65])
            data.append(["Reddit", datetime.now(), f"People are debating about {keyword} everywhere", -0.72])

        df = pd.DataFrame(data, columns=["Platform", "Timestamp", "Text", "Sentiment"])
        df.sort_values("Timestamp", inplace=True)

        st.success("✅ Analysis complete!")
        st.write("### Sentiment Data")
        st.dataframe(df)

        st.write("### 📈 Sentiment Over Time")
        fig = px.line(df, x="Timestamp", y="Sentiment", color="Platform",
                      markers=True, title=f"📊 Sentiment Trend for '{keyword}'",
                      template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
