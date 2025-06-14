import tweepy
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = tweepy.Client(
    bearer_token=st.secrets["TWITTER_BEARER_TOKEN"]
)

def get_tweets(keyword, count=10):
    try:
        query = f'"{keyword}" OR ${keyword} OR #{keyword}'  # broaden match
        response = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),
            tweet_fields=["created_at"]
        )
        return [(t.text, t.created_at) for t in response.data] if response.data else []
    except Exception as e:
        st.error("Twitter error: " + str(e))
        return []
