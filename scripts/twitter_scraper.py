import tweepy
import streamlit as st
import time

client = tweepy.Client(
    bearer_token=st.secrets["TWITTER_BEARER_TOKEN"]
)

def get_tweets(keyword, count=10):
    query = f'"{keyword}" OR ${keyword} OR #{keyword}'
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),
            tweet_fields=["created_at"]
        )
        if not response or not response.data:
            st.warning("⚠️ Twitter returned no data.")
            return []
        return [(tweet.text, tweet.created_at) for tweet in response.data]
    except tweepy.TooManyRequests:
        st.warning("⚠️ Rate limit hit. Skipping Twitter.")
        return []
    except Exception as e:
        st.error("❌ Twitter API error: " + str(e))
        return []

