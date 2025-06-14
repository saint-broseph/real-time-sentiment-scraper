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
        subreddits = ["stocks", "wallstreetbets", "investing"]
        results = []
        per_sub_limit = limit // len(subreddits)

        for sub in subreddits:
            posts = reddit.subreddit(sub).search(keyword, sort='new', limit=per_sub_limit)
            results.extend((post.title + " " + post.selftext, datetime.fromtimestamp(post.created_utc).replace(tzinfo=None)))
        for post in posts
        return results
    except Exception as e:
        st.error("Reddit error: " + str(e))
        return []
