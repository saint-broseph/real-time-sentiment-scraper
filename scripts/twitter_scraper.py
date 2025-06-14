import tweepy
import os
from dotenv import load_dotenv
import time

load_dotenv()

# ✅ Use API v2 authentication with only the Bearer Token
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
)

def get_tweets(keyword, count=10):
    try:
        response = client.search_recent_tweets(
            query=keyword,
            max_results=min(count, 10),
            tweet_fields=["created_at"]
        )
        return [t.text for t in response.data] if response.data else []
    except tweepy.TooManyRequests:
        print("⚠️ Twitter rate limit reached. Sleeping for 60 seconds...")
        time.sleep(60)
        return get_tweets(keyword, count)  # retry once
