import streamlit as st
from scripts.twitter_scraper import get_tweets
from scripts.reddit_scraper import get_reddit_posts
from scripts.sentiment import analyze_sentiment
from scripts.plot_sentiment import plot_sentiment
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sentiment Scanner", layout="wide")

st.title("📈 Real-Time Social Sentiment Scanner")
keyword = st.text_input("Enter a stock/company name:", "Adani")

if st.button("Analyze Sentiment"):
    with st.spinner("Fetching tweets and Reddit posts..."):
        tweets = get_tweets(keyword, count=15)
        reddit_posts = get_reddit_posts(keyword, limit=15)

        data = []
        for t in tweets:
            data.append(["Twitter", datetime.now(), t, analyze_sentiment(t)])
        for r in reddit_posts:
            data.append(["Reddit", datetime.now(), r, analyze_sentiment(r)])

        df = pd.DataFrame(data, columns=["Platform", "Timestamp", "Text", "Sentiment"])
        filename = f"data/{keyword.lower()}_sentiment.csv"
        df.to_csv(filename, index=False)

    st.success("Done! Here's the sentiment plot:")
    st.pyplot(plot_sentiment(filename))
