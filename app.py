import streamlit as st
import pandas as pd
from datetime import datetime
from scripts.reddit_scraper import get_reddit_posts
from scripts.news_scraper import get_news_articles
from scripts.sentiment import analyze_sentiment
from scripts.twitter_scraper import get_tweets
from scripts.youtube_scraper import get_youtube_data
import plotly.express as px

# --- App Config ---
st.set_page_config(page_title="Sentilytics", layout="wide")

# --- UI Header ---
st.title("🧠 Sentilytics — Cross-Platform Sentiment Tracker")
st.markdown("Track what Twitter, Reddit, News, and YouTube say about any topic — from stocks to trends to public figures.")

# --- Keyword Input ---
keyword = st.text_input("Enter a topic, stock, person, or trend:")

# --- Main button ---
if st.button("Analyze Sentiment"):
    with st.spinner("🔍 Fetching data from Twitter, Reddit, News, and YouTube..."):

        tweets = get_tweets(keyword, count=10)
        reddit_posts = get_reddit_posts(keyword, limit=80)
        news_articles = get_news_articles(keyword, limit=80)
        youtube_data = get_youtube_data(keyword, video_limit=3, comments_per_video=3)

        st.write(f"✅ Tweets fetched: {len(tweets)}")
        st.write(f"✅ Reddit posts fetched: {len(reddit_posts)}")
        st.write(f"✅ News articles fetched: {len(news_articles)}")
        st.write(f"✅ YouTube entries fetched: {len(youtube_data)}")

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

        if news_articles:
            for text, ts in news_articles:
                score = analyze_sentiment(text)
                data.append(["News", ts, text, score])
        else:
            st.warning("⚠️ No News articles found.")

        if youtube_data:
            for text, ts in youtube_data:
                score = analyze_sentiment(text)
                data.append(["YouTube", ts, text, score])
        else:
            st.warning("⚠️ No YouTube data found.")

        if not data:
            st.info("⚠️ No live sentiment found. Showing demo data.")
            now = datetime.now()
            data = [
                ["Twitter", now, f"{keyword} is trending heavily today", 0.65],
                ["Reddit", now, f"People are debating about {keyword} everywhere", -0.72],
                ["News", now, f"{keyword} is making headlines", 0.10],
                ["YouTube", now, f"Discussions around {keyword} are emerging in videos", 0.20]
            ]

        for i in range(len(data)):
            data[i][1] = data[i][1].replace(tzinfo=None)

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

