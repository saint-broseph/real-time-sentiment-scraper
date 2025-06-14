import praw
import os
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

load_dotenv()

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
        per_sub_limit = max(2, limit // len(subreddits))  # ensure at least 1 per subreddit

        for sub in subreddits:
            posts = reddit.subreddit(sub).search(keyword, sort='new', limit=per_sub_limit)
            for post in posts:
                text = post.title + " " + post.selftext
                timestamp = datetime.fromtimestamp(post.created_utc).replace(tzinfo=None)
                results.append((text, timestamp))

        return results

    except Exception as e:
        st.error("Reddit error: " + str(e))
        return []
