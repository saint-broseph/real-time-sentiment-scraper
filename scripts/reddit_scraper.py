import praw
import os
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

load_dotenv()

# Initialize Reddit API using secrets
reddit = praw.Reddit(
    client_id=st.secrets["REDDIT_CLIENT_ID"],
    client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
    user_agent=st.secrets["REDDIT_USER_AGENT"]
)

def get_reddit_posts(keyword, limit=20):
    try:
        subreddits = [
            "stocks", "investing", "wallstreetbets", "finance", "economy", "StockMarket",
            "personalfinance", "ValueInvesting", "FinancialPlanning",
            "IndiaInvestments", "IndianEconomy", "business", "Entrepreneur",
            "startups", "macroeconomics", "cryptocurrency", "CryptoMarkets",
            "technology", "Futurology"
        ]

        results = []
        per_sub_limit = max(2, limit // len(subreddits))

        for sub in subreddits:
            try:
                posts = reddit.subreddit(sub).search(keyword, sort='new', limit=per_sub_limit)
                for post in posts:
                    text = f"[r/{sub}] {post.title} {post.selftext}"
                    timestamp = datetime.fromtimestamp(post.created_utc).replace(tzinfo=None)
                    results.append((text, timestamp))
            except Exception as sub_err:
                st.warning(f"⚠️ Skipped r/{sub}: {str(sub_err)}")

        return results

    except Exception as e:
        st.error("Reddit error: " + str(e))
        return []
